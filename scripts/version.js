// 版本闸门：保证每次都在「线上最新版」的基础上改，两边不互相覆盖。
//
// 这个仓库已经改成 Git 自动部署：public/index.html 就是线上内容的源文件，
// Netlify 每次部署都会在 <head> 里注入一段 326 字节的注释（"This site is hosted on Netlify..."）。
// 所以比对线上时必须先把这段注释剥掉，否则永远是「不一致」。
//
//   node scripts/version.js check   三方对比：本地工作区 / origin/main / 线上
//   node scripts/version.js sync    把 public/index.html 恢复成 origin/main 的版本（会拒绝覆盖未提交的改动）
//   node scripts/version.js bump    改完后把 BUILD 时间戳更新为现在（YYMMDDHHmm）
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SITE = 'https://jiangshidaozhang.netlify.app';
const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const HTML = path.join(ROOT, 'public', 'index.html');
const REL = 'public/index.html';

const sha = (b) => crypto.createHash('sha256').update(b).digest('hex');
const short = (b) => (b ? sha(b).slice(0, 12) : '无');
const buildOf = (b) => (b ? ((b.toString('utf8').match(/const BUILD = '(\d+)'/) || [])[1] || '?') : '无');
const nowBuild = () => {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${String(d.getFullYear()).slice(2)}${p(d.getMonth() + 1)}${p(d.getDate())}${p(d.getHours())}${p(d.getMinutes())}`;
};

// Netlify 在 serve 时往 <head> 注入的注释，不属于源文件
const stripInjected = (s) => s.replace(/<!--[^]*?This site is hosted on Netlify[^]*?-->\r?\n?/, '');

async function fetchLive() {
  const r = await fetch(SITE + '/', { signal: AbortSignal.timeout(30000), headers: { 'cache-control': 'no-cache' } });
  if (!r.ok) throw new Error('线上返回 ' + r.status);
  const raw = Buffer.from(await r.arrayBuffer());
  const body = Buffer.from(stripInjected(raw.toString('utf8')), 'utf8');
  return { raw, body };
}

// 有些受限环境（沙箱 / CI 的管道限制）spawn git 会 EPERM，这时降级成「只比本地 vs 线上」
function readGit(ref) {
  try {
    return { buf: execFileSync('git', ['show', `${ref}:${REL}`], { cwd: ROOT, maxBuffer: 64 * 1024 * 1024 }), err: null };
  } catch (e) {
    return { buf: null, err: (e.message || '').split('\n')[0] };
  }
}

const readLocal = () => (fs.existsSync(HTML) ? fs.readFileSync(HTML) : null);

const cmd = process.argv[2] || 'check';
const local = readLocal();

if (cmd === 'sync') {
  const git = readGit('origin/main').buf;
  if (!git) { console.error('❌ 拿不到 origin/main 的 ' + REL + '，先 git fetch。'); process.exit(1); }
  if (local && !Buffer.from(local).equals(Buffer.from(git)) && !process.argv.includes('--force')) {
    console.error('❌ 本地版和 origin/main 不一致，直接覆盖会丢掉未提交的改动。');
    console.error(`   本地 ${short(local)}   origin/main ${short(git)}`);
    console.error('   确认要丢弃就加 --force。');
    process.exit(1);
  }
  fs.writeFileSync(HTML, git);
  console.log(`✅ 已恢复 ${REL} 到 origin/main：BUILD=${buildOf(git)}  sha=${short(git)}`);
} else if (cmd === 'check') {
  const g = readGit('origin/main');
  const git = g.buf;
  const live = (await fetchLive()).body;

  console.log(`本地工作区    BUILD=${buildOf(local)}  sha=${short(local)}  ${local ? local.length : 0} B`);
  console.log(`origin/main   BUILD=${buildOf(git)}  sha=${short(git)}  ${git ? git.length : 0} B`);
  console.log(`线上(去注水)  BUILD=${buildOf(live)}  sha=${short(live)}  ${live.length} B`);

  const localIsLive = local ? live.equals(local) : null;

  if (!git) {
    console.log(`\n（读不到 origin/main：${g.err || '未知原因'}；降级为只比 本地 vs 线上）`);
    if (localIsLive) console.log('✅ 本地 = 线上。');
    else {
      console.log('📝 本地和线上不一致：要么本地有没部署的改动，要么线上被别处改过。');
      console.log('   `git fetch && git log --oneline origin/main -5` 看看是不是对方先传了。');
      process.exitCode = 2;
    }
  } else if (!git.equals(live)) {
    console.log('\n⚠️ 线上 ≠ origin/main：线上不是这个提交构建出来的。');
    console.log('   要么部署失败/还在构建，要么有人绕开 Git 手动传了一份 —— 先查 Netlify 后台的 Deploys。');
    process.exitCode = 2;
  } else if (local && !local.equals(git)) {
    console.log('\n📝 本地和 origin/main 有差异（正常：你正在改，或还没 push）。');
    console.log('   提交前先看 `git diff -- ' + REL + '`，确认没有夹带别人的改动。');
  } else {
    console.log('\n✅ 本地 = origin/main = 线上，可以在上面改。');
  }
} else if (cmd === 'bump') {
  if (!local) { console.error('❌ 找不到 ' + REL); process.exit(1); }
  const cur = buildOf(local);
  const next = nowBuild();
  if (cur === next) {
    console.log('BUILD 已经是当前分钟：' + cur);
  } else {
    fs.writeFileSync(HTML, local.toString('utf8').replace(/const BUILD = '\d+'/, `const BUILD = '${next}'`));
    console.log(`✅ BUILD ${cur} → ${next}（记得跑 python3 src/gen_assets.py 重新生成正式产物）`);
  }
} else {
  console.error('用法: node scripts/version.js [check|sync|bump]');
  process.exit(1);
}
