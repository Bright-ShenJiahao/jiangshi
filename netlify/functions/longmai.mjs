// 龙脉功德簿：《守卫任家镇的中心的龙脉》的共享排行榜（和原游戏的功德簿分开存）
import { getStore } from '@netlify/blobs';

const KEY = 'longmai';
const KEEP = 100;
const CHEAT_CAP = 20;
const WAVES = 20;

const clean = (v) => String(v ?? '').replace(/[\u0000-\u001f\u007f<>]/g, '').trim().slice(0, 10);
const int = (v, lo, hi) => { const n = Math.round(Number(v)); return Number.isFinite(n) ? Math.min(hi, Math.max(lo, n)) : lo; };
const json = (data, status = 200) => new Response(JSON.stringify(data), {
  status, headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
});

export default async (req) => {
  const store = getStore({ name: 'leaderboard', consistency: 'strong' });
  const read = async () => {
    const r = await store.getWithMetadata(KEY, { type: 'json' });
    return { list: Array.isArray(r?.data) ? r.data : [], etag: r?.etag };
  };
  // 同名同难度同角色，作弊和不作弊各占一行
  const keyOf = (r) => r.name + '|' + r.diff + '|' + (r.hero || 'tao') + '|' + (r.cheat ? 1 : 0);
  const shape = (list) => {
    const best = new Map();
    for (const r of list) { const k = keyOf(r); const o = best.get(k); if (!o || o.score < r.score) best.set(k, r); }
    let n = 0;
    return [...best.values()].sort((a, b) => b.score - a.score).filter((r) => !r.cheat || ++n <= CHEAT_CAP);
  };
  if (req.method === 'GET') return json(shape((await read()).list).slice(0, KEEP));
  if (req.method !== 'POST') return json({ error: 'method not allowed' }, 405);

  let b;
  try { b = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
  const rec = {
    name: clean(b.name) || '无名道士',
    score: int(b.score, 0, 200000),
    kills: int(b.kills, 0, 20000),
    lv: int(b.lv, 1, 200),
    wave: int(b.wave, 0, WAVES),
    t: int(b.t, 0, 7200),
    win: b.win === true,
    diff: b.diff === 'hard' ? 'hard' : 'normal',
    at: int(b.at, 0, 4102444800000),
    hero: b.hero === 'monk' || b.hero === 'priest' ? b.hero : 'tao',
    cheat: 0,
    dev: b.dev === 't' ? 't' : b.dev === 'k' ? 'k' : '',
  };
  // 合理性：积分不能超过游戏自己的公式；守住的波数要和时间、通关对得上
  const why = [];
  if (int(b.cheat, 0, 9999) > 0) why.push('client');
  const max = (rec.wave * 120 + rec.kills + rec.lv * 20 + (rec.win ? 3000 + 100 * 20 : 0)) * (rec.diff === 'hard' ? 1.5 : 1);
  if (rec.score > max + 5) why.push('score');
  if (rec.win && rec.wave < WAVES) why.push('win');
  if (rec.t < rec.wave * 14) why.push('speed');        // 每波刷怪至少十五秒
  if (rec.kills > (rec.wave + 1) * 140) why.push('kills');
  if (why.length) { rec.cheat = 1; rec.why = why.join(','); }

  for (let attempt = 0; attempt < 4; attempt++) {
    const { list, etag } = await read();
    const prev = list.find((r) => keyOf(r) === keyOf(rec));
    if (prev && prev.score >= rec.score) return json(shape(list).slice(0, KEEP));
    const next = shape(list.filter((r) => keyOf(r) !== keyOf(rec)).concat(rec)).slice(0, KEEP);
    const res = await store.setJSON(KEY, next, etag ? { onlyIfMatch: etag } : { onlyIfNew: true });
    if (res?.modified !== false) return json(next);
  }
  return json({ error: 'busy, try again' }, 503);
};

export const config = { path: '/api/longmai' };
