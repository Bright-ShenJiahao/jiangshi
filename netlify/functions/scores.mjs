// 功德簿：共享排行榜（Netlify Functions + Netlify Blobs）
import { getStore } from '@netlify/blobs';

const KEY = 'top';
const CHEAT_KEY = 'cheat';   // 作弊榜：逆天改命者
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

  const board = new URL(req.url).searchParams.get('board') === 'cheat' ? CHEAT_KEY : KEY;
  if (req.method === 'GET') return json((await read(board)).list.slice(0, SHOW));
  if (req.method !== 'POST') return json({ error: 'method not allowed' }, 405);

  let b;
  try { b = await req.json(); } catch { return json({ error: 'bad json' }, 400); }
  const rec = {
    name: clean(b.name) || '无名道士',
    kills: int(b.kills, 0, 20000),
    lv: int(b.lv, 1, 200),
    t: int(b.t, 0, 300),
    win: b.win === true,
    diff: b.diff === 'hard' ? 'hard' : 'normal',
    score: int(b.score, 0, 200000),
    at: int(b.at, 0, 4102444800000),
    ults: int(b.ults, 0, 9999),
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
  if (rec.lv > 45) why.push('lv');
  if (rec.t < 300 && rec.win) why.push('win');
  const target = why.length ? CHEAT_KEY : KEY;
  if (why.length) rec.why = why.join(',');

  for (let attempt = 0; attempt < 4; attempt++) {
    const { list, etag } = await read(target);
    const keyOf = (r) => r.name + '|' + r.diff;
    const prev = list.find((r) => keyOf(r) === keyOf(rec));
    let next = list;
    if (!prev || prev.score < rec.score) {
      next = list.filter((r) => keyOf(r) !== keyOf(rec)).concat(rec)
        .sort((a, b) => b.score - a.score).slice(0, KEEP);
    } else return target === KEY ? json(list.slice(0, SHOW)) : json((await read()).list.slice(0, SHOW));
    const res = await store.setJSON(target, next, etag ? { onlyIfMatch: etag } : { onlyIfNew: true });
    if (res?.modified !== false) return target === KEY ? json(next.slice(0, SHOW)) : json((await read()).list.slice(0, SHOW));
  }
  return json({ error: 'busy, try again' }, 503);
};

export const config = { path: '/api/scores' };
