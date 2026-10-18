// 只读探测：确认 /api/scores 是什么（Function / Edge Function / 代理），迁移到 Git 时不能丢
const BASE = 'https://jiangshidaozhang.netlify.app';

async function probe(p, opts = {}) {
  try {
    const r = await fetch(BASE + p, { signal: AbortSignal.timeout(15000), ...opts });
    const t = await r.text();
    return { p, status: r.status, type: r.headers.get('content-type'), len: t.length, body: t.slice(0, 160).replace(/\s+/g, ' ') };
  } catch (e) {
    return { p, status: 'ERR', body: e.message };
  }
}

(async () => {
  const paths = [
    '/.netlify/functions/scores',
    '/.netlify/functions/api',
    '/.netlify/functions/',
    '/api/',
    '/api/scores/',
    '/api/scores?op=start',
  ];
  for (const p of paths) {
    const r = await probe(p);
    console.log(`${p.padEnd(28)} ${String(r.status).padEnd(4)} ${String(r.len).padEnd(7)} ${r.body}`);
  }

  // 看看最终解析到哪个主机 / 有没有 CORS
  const r = await fetch(BASE + '/api/scores', { method: 'HEAD', signal: AbortSignal.timeout(15000) }).catch((e) => ({ error: e.message }));
  console.log('\nHEAD /api/scores', r.status ?? r.error);
  if (r.headers) {
    const h = {};
    r.headers.forEach((v, k) => (h[k] = v));
    console.log(JSON.stringify(h, null, 1));
  }

  // OPTIONS 看预检
  try {
    const o = await fetch(BASE + '/api/scores', { method: 'OPTIONS', signal: AbortSignal.timeout(10000) });
    console.log('\nOPTIONS status', o.status, '| allow:', o.headers.get('allow'), '| acc:', o.headers.get('access-control-allow-origin'));
  } catch (e) { console.log('OPTIONS err', e.message); }
})();
