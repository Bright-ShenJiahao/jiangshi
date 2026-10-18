import fs from 'node:fs';

const OLD1 = "    const t = mDense(220); const x = t ? t.x : P.x, y = t ? t.y : P.y;";
const NEW1 = [
  "    // 砸向「血量最多」的那一片：以每只怪为圆心，算范围内的总血量，取最高的一处",
  "    const Rr0 = lv >= 2 ? 120 : 90;",
  "    let best = null, bestV = -1;",
  "    for (const e of S.en) {",
  "      if (e.dead || e.audience) continue;",
  "      let v = 0;",
  "      for (const o of S.en) if (!o.dead && !o.audience && inEll(o, e.x, e.y, Rr0)) v += Math.max(1, o.hp || o.max || 1);",
  "      if (v > bestV) { bestV = v; best = e; }",
  "    }",
  "    const x = best ? best.x : P.x, y = best ? best.y : P.y;",
].join('\n');

const OLD2 = "  for (const f of S.food) {\n    const fd = Math.hypot(f.x - P.x, f.y - P.y);";
const NEW2 = "  for (const f of S.food) {\n    if (P.hp >= P.max) continue;   // 满血：不吸、不捡、不消耗，道具留在原地\n    const fd = Math.hypot(f.x - P.x, f.y - P.y);";

const files = ['src/game_template.html', 'public/index.html'];
let bad = 0;
for (const f of files) {
  let s = fs.readFileSync(f, 'utf8');
  const n1 = s.split(OLD1).length - 1;
  const n2 = s.split(OLD2).length - 1;
  console.log(`${f}: 大招目标 ${n1} 处, 食物拾取 ${n2} 处`);
  if (n1 !== 1 || n2 !== 1) { bad++; continue; }
  s = s.replace(OLD1, NEW1).replace(OLD2, NEW2);
  fs.writeFileSync(f, s);
  console.log(`  ✅ 已替换`);
}
process.exit(bad ? 1 : 0);
