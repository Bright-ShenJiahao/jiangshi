import fs from 'node:fs';

const s = fs.readFileSync('public/index.html', 'utf8');

// 1) 整体语法检查
const blocks = [...s.matchAll(/<script(?![^>]*\bsrc=)[^>]*>([\s\S]*?)<\/script>/g)];
let ok = true;
blocks.forEach((b, i) => {
  try { new Function(b[1]); console.log(`  内联脚本 #${i} 语法 ✅ ${b[1].length} 字符`); }
  catch (e) { ok = false; console.log(`  内联脚本 #${i} 语法 ❌ ${e.message}`); }
});

// 2) 把补丁里的瞄准逻辑原样抽出来，用假数据跑一遍
const start = s.indexOf('    // 砸向「血量最多」的那一片');
const endMark = '    const x = best ? best.x : P.x, y = best ? best.y : P.y;';
const end = s.indexOf(endMark, start) + endMark.length;
const block = s.slice(start, end);
console.log('\n抽取代码长度:', block.length, block.startsWith('    // 砸向') ? '✅' : '❌');

const inEll = (e, x, y, R) => (e.x - x) ** 2 + ((e.y - y) / 0.75) ** 2 < R * R;
const aim = new Function('S', 'P', 'inEll', 'lv', block + '\nreturn { x, y };');

function run(name, en, lv) {
  const S = { en };
  const P = { x: 0, y: 0 };
  const r = aim(S, P, inEll, lv);
  console.log(`  ${name}: → (${r.x}, ${r.y})`);
  return r;
}

// A: 一堆软怪在左上，两只大怪在右下 → 应该砸右下
const zh = (x, y, hp) => ({ x, y, hp, max: hp, dead: false, audience: false });
let r = run('两坨：9 只弱怪 vs 2 只厚血', [
  ...Array.from({ length: 9 }, (_, i) => zh(-300 + i * 4, -300, 10)),
  zh(200, 200, 400), zh(206, 205, 400),
], 1);
const passA = Math.abs(r.x - 200) < 30 && Math.abs(r.y - 200) < 30;

// B: 全空 → 应该砸自己脚下
r = run('场上没有怪', [zh(500, 500, 50)].filter(() => false), 1);
const passB = r.x === 0 && r.y === 0;

// C: 死怪和观众不算数
r = run('唯一一坨是死怪+观众', [
  { ...zh(-200, -200, 999), dead: true },
  { ...zh(300, 300, 999), audience: true },
  zh(-40, 30, 5),
], 3);
const passC = Math.abs(r.x + 40) < 30 && Math.abs(r.y - 30) < 30;

// D: 大招 2 级范围更大，能罩住的更多
const spread = [zh(0, 0, 100), zh(100, 0, 60), zh(230, 0, 500)];
r = run('2 级更大范围', spread, 2);
console.log('\n结果:', [passA, passB, passC].every(Boolean) ? '✅ 全部符合预期' : '❌ 有不符合的');
process.exit(ok && passA && passB && passC ? 0 : 1);
