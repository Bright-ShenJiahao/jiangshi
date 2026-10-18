// 线上状态检查：抓一份线上 HTML，和上一次快照对比，顺带跑一遍健康检查
// 用法: node scripts/live-check.js [--save]
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const BASE = 'https://jiangshidaozhang.netlify.app';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SNAP_DIR = path.join(ROOT, '.snapshots');
const SAVE = process.argv.includes('--save');

fs.mkdirSync(SNAP_DIR, { recursive: true });

const sha = (buf) => crypto.createHash('sha256').update(buf).digest('hex');
const kb = (n) => (n / 1024).toFixed(0) + ' KB';

function latestSnapshot() {
  const files = fs.readdirSync(SNAP_DIR).filter((f) => f.endsWith('.html')).sort();
  return files.length ? path.join(SNAP_DIR, files[files.length - 1]) : null;
}

function stats(html) {
  const dataUris = [...html.matchAll(/data:([a-z0-9.+-]+\/[a-z0-9.+-]+);base64,([A-Za-z0-9+/=]+)/gi)];
  const b64 = dataUris.reduce((a, m) => a + m[2].length, 0);
  return {
    bytes: Buffer.byteLength(html),
    scripts: (html.match(/<script/gi) || []).length,
    dataUris: dataUris.length,
    base64KB: Math.round(b64 * 0.75 / 1024),
    title: ((html.match(/<title>([^<]*)<\/title>/i) || [])[1] || '').trim(),
    pngs: dataUris.filter((m) => /png/i.test(m[1])).length,
    mp3s: dataUris.filter((m) => /mpeg|mp3/i.test(m[1])).length,
  };
}

async function get(p, opts = {}) {
  const t0 = Date.now();
  const r = await fetch(BASE + p, { signal: AbortSignal.timeout(30000), ...opts });
  const body = await r.arrayBuffer();
  return { status: r.status, ms: Date.now() - t0, bytes: body.byteLength, body: Buffer.from(body), headers: r.headers };
}

(async () => {
  const now = new Date();
  const stamp = now.toISOString().replace(/[:T]/g, '-').slice(0, 16);
  const home = await get('/');
  const html = home.body.toString('utf8');
  const cur = stats(html);
  const hash = sha(home.body);

  console.log(`线上首页  ${home.status}  ${kb(home.bytes)}  ${home.ms} ms  sha256=${hash.slice(0, 12)}`);
  console.log(`  标题=${cur.title}  内联脚本=${cur.scripts}  data URI=${cur.dataUris} (PNG ${cur.pngs} / MP3 ${cur.mp3s})  base64≈${cur.base64KB} KB`);

  const prevPath = latestSnapshot();
  if (!prevPath) {
    console.log('  基线：无（首次运行）');
  } else {
    const prev = stats(fs.readFileSync(prevPath, 'utf8'));
    const same = sha(fs.readFileSync(prevPath)) === hash;
    console.log(`  对比基线：${path.basename(prevPath)}  ${same ? '未变化 ✅' : '已变化 ⚠'}`);
    if (!same) {
      const d = (k) => {
        const v = cur[k] - prev[k];
        return (v > 0 ? '+' : '') + v;
      };
      console.log(`    字节 ${d('bytes')}  |  data URI ${d('dataUris')}  |  base64 ${d('base64KB')} KB  |  脚本 ${d('scripts')}`);
    }
  }

  // 健康检查
  console.log('\n健康检查');
  const checks = [
    ['/api/scores', (r) => `${r.status}  ${kb(r.bytes)}  ${r.ms} ms`],
    ['/share.png', (r) => `${r.status}  ${kb(r.bytes)}`],
    ['/favicon.ico', (r) => `${r.status}`],
    ['/robots.txt', (r) => `${r.status}`],
    ['/ch/heian.js', (r) => `${r.status}`],
    ['/ch/qin.js', (r) => `${r.status}`],
  ];
  for (const [p, fmt] of checks) {
    try {
      const r = await get(p);
      const flag = [404, 500].includes(r.status) ? ' ❌' : r.status === 200 ? '' : ' ⚠';
      console.log(`  ${p.padEnd(14)} ${fmt(r)}${flag}`);
    } catch (e) {
      console.log(`  ${p.padEnd(14)} ERR ${e.message}`);
    }
  }

  const h = home.headers;
  console.log('\n关键响应头');
  for (const k of ['content-encoding', 'cache-control', 'strict-transport-security', 'content-security-policy', 'x-frame-options', 'referrer-policy', 'permissions-policy']) {
    console.log(`  ${k.padEnd(28)} ${h.get(k) ?? '（缺失）'}`);
  }

  if (SAVE) {
    const out = path.join(SNAP_DIR, `${stamp}.html`);
    fs.writeFileSync(out, home.body);
    console.log(`\n已保存快照：${path.relative(ROOT, out)}`);
  }
})().catch((e) => {
  console.error('检查失败：', e.message);
  process.exit(1);
});
