// 功德簿：共享排行榜（Netlify Functions + Netlify Blobs）
import { getStore } from '@netlify/blobs';

const KEY = 'top';
const CHEAT_KEY = 'cheat';   // 旧的作弊榜（只读）：读取时并入功德簿并标注作弊
const CHEAT_CAP = 20;       // 功德簿里最多保留多少条作弊成绩
const CLEARED_KEY = 'cleared';   // 通关过的名字（不受排行榜 100 名限制），用来给一休解锁
const KEEP = 100;          // stored entries
const SHOW = 100;          // entries returned to the game (排行榜分普通/困难两列显示)

const clean = (v) => String(v ?? '').replace(/[\u0000-\u001f\u007f<>]/g, '').trim().slice(0, 10);
const int = (v, lo, hi) => { const n = Math.round(Number(v)); return Number.isFinite(n) ? Math.min(hi, Math.max(lo, n)) : lo; };
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});

export default async (req) => {
  const store = getStore({ name: 'leaderboard', consistency: 'strong' });
  const read = async (key = KEY) => {
    const r = await store.getWithMetadata(key, { type: 'json' });
    return { list: Array.isArray(r?.data) ? r.data : [], etag: r?.etag };
  };

  const q = new URL(req.url).searchParams;
  if (req.method === 'GET' && q.has('cleared')) {   // 这个名字通关过吗？（排行榜里有通关记录也算）
    const nm = clean(q.get('cleared'));
    if (!nm) return json({ cleared: false });
    const names = (await read(CLEARED_KEY)).list;
    const onBoard = (await read()).list.some((r) => r.name === nm && r.win === true && !r.cheat);
    return json({ cleared: names.includes(nm) || onBoard });
  }
  // 功德簿 = 新记录 + 旧作弊榜（标注作弊）；同名同难度同角色，作弊和不作弊各占一行；作弊成绩最多 CHEAT_CAP 条
  const keyOf = (r) => r.name + '|' + r.diff + '|' + (r.hero || 'tao') + '|' + (r.cheat ? 1 : 0);
  const shape = (list) => {
    const best = new Map();
    for (const r of list) { const k = keyOf(r); const o = best.get(k); if (!o || o.score < r.score) best.set(k, r); }
    const all = [...best.values()].sort((a, b) => b.score - a.score);
    let n = 0;
    return all.filter((r) => !r.cheat || ++n <= CHEAT_CAP);
  };
  // 以前只因「等级超过 45」被误标作弊的成绩（why 只有 lv）：读取时恢复为正常成绩
  const fix = (r) => (r.cheat && r.why === 'lv' ? { ...r, cheat: 0, why: undefined } : r);
  const merged = async () => shape((await read()).list.map(fix).concat((await read(CHEAT_KEY)).list.map((r) => ({ ...r, cheat: 1 }))));
  if (req.method === 'GET') return json((await merged()).slice(0, SHOW));
  if (req.method !== 'POST') return json({ error: 'method not allowed' }, 405);

  let b;
  try { b = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
  const rec = {
    name: clean(b.name) || '无名道士',
    kills: int(b.kills, 0, 20000),
    lv: int(b.lv, 1, 200),
    t: int(b.t, 0, 320),
    win: b.win === true,
    diff: b.diff === 'hard' ? 'hard' : 'normal',
    score: int(b.score, 0, 200000),
    at: int(b.at, 0, 4102444800000),
    ults: int(b.ults, 0, 9999),
    hero: b.hero === 'monk' ? 'monk' : 'tao',
    cheat: 0,
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
  if (rec.lv > 120) why.push('lv2');   // 一局 5 分钟实测能升到 49 重，以前的 45 上限会误伤正常玩家
  if (rec.t < 300 && rec.win) why.push('win');   // 遮天蔽日最多推迟到 320 秒
  if (why.length) { rec.cheat = 1; rec.why = why.join(','); }

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
