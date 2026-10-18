// 功德簿：共享排行榜（Netlify Functions + Netlify Blobs）
import { getStore } from '@netlify/blobs';
import { createHmac, randomBytes } from 'node:crypto';
import HASHES from './hashes.mjs';   // 官方各版本页面脚本的 SHA-256（构建时自动追加）

const KEY = 'top';
const CHEAT_KEY = 'cheat';   // 旧的作弊榜（只读）：读取时并入功德簿并标注作弊
const CHEAT_CAP = 20;       // 功德簿里最多保留多少条作弊成绩
const CLEARED_KEY = 'cleared';   // 通关过的名字（不受排行榜 100 名限制），用来给一休解锁
const KEEP = 100;          // stored entries
const EPOCH = '2026-10-17-reset1';   // 改这个值 = 下次有人访问时清空功德簿的排名（top / cheat）；通关名单 cleared 保留，已解锁一休的人不受影响
const PURGE = { id: '2026-10-17-purge1', hit: (n) => /^test果/i.test(String(n).replace(/\s/g, '')) };   // 改 id = 下次访问时按 hit 规则从功德簿删除成绩（一次性）；这次删掉「Test果汁」
const NOCHEAT = '2026-10-18-nocheat1';   // 改这个值 = 下次访问时把功德簿里所有成绩的作弊标记清掉（成绩保留），旧作弊榜并回功德簿（一次性）
const PAUSEFIX = '2026-10-18-pause1';   // 一次性：只因暂停太久凭证过期（notoken / nocp）被判作弊的成绩，恢复为正常
const SHOW = 100;          // entries returned to the game (排行榜分普通/困难两列显示)

const clean = (v) => String(v ?? '').replace(/[\u0000-\u001f\u007f<>]/g, '').trim().slice(0, 10);
const int = (v, lo, hi) => { const n = Math.round(Number(v)); return Number.isFinite(n) ? Math.min(hi, Math.max(lo, n)) : lo; };
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});

const KILL_CAP = { normal: 2300, hard: 2700 };   // 完美击杀模拟：普通约 2085、困难约 2470，留一点余量
const LV_CAP = 90;
const TOK_TTL = 24 * 60 * 60 * 1000;   // 凭证有效期 24 小时：暂停很久、切后台很久都不算作弊

export default async (req) => {
  const store = getStore({ name: 'leaderboard', consistency: 'strong' });
  const read = async (key = KEY) => {
    const r = await store.getWithMetadata(key, { type: 'json' });
    return { list: Array.isArray(r?.data) ? r.data : [], etag: r?.etag };
  };

  if ((await store.get('epoch')) !== EPOCH) {   // 一次性清榜
    await store.setJSON(KEY, []); await store.setJSON(CHEAT_KEY, []); await store.set('epoch', EPOCH);
  }

  if ((await store.get('purge')) !== PURGE.id) {   // 一次性删除指定名字的成绩
    for (const k of [KEY, CHEAT_KEY]) { const { list } = await read(k); await store.setJSON(k, list.filter((r) => !PURGE.hit(r.name))); }
    await store.set('purge', PURGE.id);
  }

  // 同一个名字不分角色：同难度、同章节只留最高分那一条（记着那局用的角色）；作弊和不作弊仍各占一行
  const keyOf = (r) => r.name + '|' + r.diff + '|' + (r.cheat ? 1 : 0) + (r.ch && r.ch !== 'ren' ? '|' + r.ch : '');   // 章节不同各占一行；任家镇沿用旧键
  const shape = (list) => {
    const best = new Map();
    for (const r of list) { const k = keyOf(r); const o = best.get(k); if (!o || o.score < r.score) best.set(k, r); }
    const all = [...best.values()].sort((a, b) => b.score - a.score);
    let n = 0;
    return all.filter((r) => !r.cheat || ++n <= CHEAT_CAP);
  };

  if ((await store.get('nocheat')) !== NOCHEAT) {   // 一次性清掉作弊标记，成绩保留
    const unflag = (r) => { const o = { ...r, cheat: 0 }; delete o.why; return o; };
    const all = (await read()).list.concat((await read(CHEAT_KEY)).list).map(unflag);
    await store.setJSON(KEY, shape(all).slice(0, KEEP)); await store.setJSON(CHEAT_KEY, []); await store.set('nocheat', NOCHEAT);
  }

  if ((await store.get('pausefix')) !== PAUSEFIX) {
    const only = (r) => r.cheat && r.why && String(r.why).split(',').every((w) => w === 'notoken' || w === 'nocp');
    const list = (await read()).list.map((r) => { if (!only(r)) return r; const o = { ...r, cheat: 0 }; delete o.why; return o; });
    await store.setJSON(KEY, shape(list).slice(0, KEEP)); await store.set('pausefix', PAUSEFIX);
  }

  const q = new URL(req.url).searchParams;
  if (req.method === 'GET' && q.has('cleared')) {   // 这个名字通关过吗？（排行榜里有通关记录也算）
    const nm = clean(q.get('cleared'));
    if (!nm) return json({ cleared: false });
    const names = (await read(CLEARED_KEY)).list;
    const onBoard = (await read()).list.some((r) => r.name === nm && r.win === true && !r.cheat);
    return json({ cleared: names.includes(nm) || onBoard });
  }
  // 功德簿 = 新记录 + 旧作弊榜（标注作弊）；作弊成绩最多 CHEAT_CAP 条
  // 以前只因「等级超过 45」被误标作弊的成绩（why 只有 lv）：读取时恢复为正常成绩
  const fix = (r) => (r.cheat && r.why === 'lv' ? { ...r, cheat: 0, why: undefined } : r);
  const merged = async () => shape((await read()).list.map(fix).concat((await read(CHEAT_KEY)).list.map((r) => ({ ...r, cheat: 1 }))));
  if (req.method === 'GET') return json((await merged()).slice(0, SHOW));
  if (req.method !== 'POST') return json({ error: 'method not allowed' }, 405);

  let b;
  try { b = await req.json(); } catch { return json({ error: 'bad json' }, 400); }

  // ---- 凭证：开局领取，中途上报，结算核对 ----
  let secret = await store.get('secret');
  if (!secret) { await store.set('secret', randomBytes(24).toString('hex'), { onlyIfNew: true }); secret = await store.get('secret'); }
  const sign = (a) => createHmac('sha256', secret).update(a).digest('hex').slice(0, 24);
  const parseTok = (tok) => {
    const m = /^(\d{13})\.([0-9a-f]{16})\.([0-9a-f]{24})$/.exec(String(tok || ''));
    if (!m || sign(m[1] + '.' + m[2]) !== m[3]) return null;
    const ts = Number(m[1]); if (Date.now() - ts > TOK_TTL || ts > Date.now() + 5000) return null;
    return { ts, id: m[2] };
  };
  const op = q.get('op');
  if (op === 'start') {
    const ts = String(Date.now()), id = randomBytes(8).toString('hex');
    const run = { ts: Number(ts), diff: b.diff === 'hard' ? 'hard' : 'normal', dev: b.dev === 't' ? 't' : 'k', hash: typeof b.h === 'string' ? b.h : '', cps: [], why: [] };
    if (!run.hash) run.why.push('nohash'); else if (!HASHES.includes(run.hash)) run.why.push('codemod');
    await store.setJSON('run:' + id, run);
    return json({ tok: ts + '.' + id + '.' + sign(ts + '.' + id) });
  }
  if (op === 'cp') {
    const tk = parseTok(b.tok); if (!tk) return json({ ok: false });
    const run = await store.get('run:' + tk.id, { type: 'json' }); if (!run || run.done) return json({ ok: false });
    const t = int(b.t, 0, 420), kills = int(b.kills, 0, 20000), lv = int(b.lv, 1, 200);
    const prev = run.cps[run.cps.length - 1] || { t: 0, kills: 0, lv: 1 };
    const wall = (Date.now() - run.ts) / 1000;
    if (t > wall * 1.15 + 6 && !run.why.includes('speed')) run.why.push('speed');                       // 游戏时间比真实时间走得快
    if (t < prev.t || kills < prev.kills || lv < prev.lv) run.why.push('rewind');
    else if (kills - prev.kills > (t - prev.t) * 20 + 100 && !run.why.includes('burst')) run.why.push('burst');   // 一段时间内击杀暴涨
    run.cps.push({ t, kills, lv, w: Math.round(wall) });
    if (run.cps.length > 20) run.cps.shift();
    await store.setJSON('run:' + tk.id, run);
    return json({ ok: true });
  }

  const rec = {
    name: clean(b.name) || '无名道士',
    kills: int(b.kills, 0, 20000),
    lv: int(b.lv, 1, 200),
    t: int(b.t, 0, 420),
    win: b.win === true,
    diff: b.diff === 'hard' ? 'hard' : 'normal',
    score: int(b.score, 0, 200000),
    at: int(b.at, 0, 4102444800000),
    ults: int(b.ults, 0, 9999),
    hero: b.hero === 'monk' || b.hero === 'priest' || b.hero === 'jian' || b.hero === 'gan' ? b.hero : 'tao',
    ch: ['heian', 'london', 'nanyang', 'qin'].includes(b.ch) ? b.ch : 'ren',
    cheat: 0,
    dev: b.dev === 't' ? 't' : b.dev === 'k' ? 'k' : '',
  };
  const flagged = int(b.cheat, 0, 9999) > 0;
  // Plausibility: the score must not exceed what the game's own formula allows.
  const max = (rec.kills + rec.lv * 20 + rec.t * 2 + (rec.win ? 1000 : 0) + 500) * (rec.diff === 'hard' ? 1.5 : 1);
  // 服务器校验：数据不合常理的成绩一律进作弊榜
  const why = [];
  if (flagged) why.push('client');
  if (rec.score > max + 5) why.push('score');
  if (rec.ults > Math.floor(rec.t / 28) + 1) why.push('ult');
  if (rec.kills > rec.t * 6 + 200) why.push('kills');
  if (rec.kills > KILL_CAP[rec.diff]) why.push('cap');          // 刷怪总量决定的击杀上限
  if (rec.lv > LV_CAP) why.push('lv2');   // 实测最高 62 重
  if (rec.t < 360 && rec.win) why.push('win');   // 一局 6 分钟；遮天蔽日最多推迟到 380 秒
  {   // 凭证核对
    const tk = parseTok(b.tok);
    const run = tk ? await store.get('run:' + tk.id, { type: 'json' }) : null;
    if (!run) why.push('notoken');
    else if (run.done) why.push('reuse');
    else {
      run.why.forEach((w) => why.push(w));
      const wall = (Date.now() - run.ts) / 1000;
      if (rec.t > wall * 1.15 + 8) why.push('speed');
      const need = Math.floor(rec.t / 30) - 3;       // 允许丢几个上报包
      if (run.cps.length < need) why.push('nocp');
      const last = run.cps[run.cps.length - 1];
      if (last && (rec.kills < last.kills || rec.lv < last.lv || rec.kills - last.kills > Math.max(0, rec.t - last.t) * 20 + 100)) why.push('jump');
      if (run.diff !== rec.diff) why.push('diff');
      rec.dev = run.dev;   // 设备以服务器记录为准
      run.done = true; await store.setJSON('run:' + tk.id, run);
    }
  }
  if (why.length) { rec.cheat = 1; rec.why = [...new Set(why)].join(','); }

  if (rec.win && !why.length) {   // 只记正常通关的名字；撞车就重试几次，失败也不影响成绩提交
    for (let i = 0; i < 4; i++) {
      const { list, etag } = await read(CLEARED_KEY);
      if (list.includes(rec.name)) break;
      const res = await store.setJSON(CLEARED_KEY, list.concat(rec.name).slice(-5000), etag ? { onlyIfMatch: etag } : { onlyIfNew: true });
      if (res?.modified !== false) break;
    }
  }

  for (let attempt = 0; attempt < 4; attempt++) {
    const { list, etag } = await read(KEY);
    const prev = list.find((r) => keyOf(r) === keyOf(rec));
    if (prev && prev.score >= rec.score) return json((await merged()).slice(0, SHOW));
    const next = shape(list.filter((r) => keyOf(r) !== keyOf(rec)).concat(rec)).slice(0, KEEP);
    const res = await store.setJSON(KEY, next, etag ? { onlyIfMatch: etag } : { onlyIfNew: true });
    if (res?.modified !== false) return json((await merged()).slice(0, SHOW));
  }
  return json({ error: 'busy, try again' }, 503);
};

export const config = { path: '/api/scores' };
