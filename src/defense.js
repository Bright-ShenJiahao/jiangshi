
// =====================================================================
// 守卫任家镇的中心的龙脉 —— 防守模式
// 这一段接在原游戏脚本的最后：同名函数会覆盖前面的版本（刷怪、目标、结算、界面……），
// 角色、法器、大招、怪物行为都沿用原游戏。
// =====================================================================
const D_LANES = MAP.lanes, D_CORE = MAP.core, D_WAVES = 30, D_TOWN_Y = MAP.townY;
const D_SITE = SITE + 'longmai.html';
const dNum = n => cn(n);
// 每一波的怪：[从第几波起, 到第几波, 种类, 权重]
const D_MIX = [
  [1, 9, 'ghost', 5], [1, 6, 'walk', 4], [1, 4, 'zP', 4], [3, 12, 'zW', 3],
  [6, 14, 'corpse', 4], [6, 30, 'jump', 2], [11, 30, 'ghostW', 2], [11, 30, 'zG', 3], [11, 18, 'walk', 2],
  [16, 30, 'wolf', 3], [16, 30, 'vampM', 3], [16, 30, 'ghost', 2], [21, 30, 'corpse', 2], [21, 30, 'zW', 2], [26, 30, 'bride', 1],
];
// 每五波一个 BOSS
const D_BOSS = {
  5: { name: '尸变任老爷', type: 'zombie', skin: 'renZ', hp: 650, sc: 1.9, summon: 'zP', leaper: true,
    say: ['任老爷被老太爷咬了一口，伤口发黑……', '任老爷尸变了！直奔任家镇！'] },
  10: { name: '赶尸毛僵', type: 'jumper', skin: 'jumperM', hp: 1300, sc: 1.75, summon: 'corpse',
    say: ['四目道长赶尸路过，一阵阴风吹落了符咒……', '赶尸队里的毛僵挣脱了！'] },
  15: { name: '红衣女鬼', type: 'ghost', skin: 'ghostR', hp: 2000, sc: 1.6, summon: 'ghostW',
    say: ['秋生说，昨夜送了一位红衣姑娘回家……', '她根本不是人！红衣女鬼来了！'] },
  20: { name: '西洋吸血鬼', type: 'walker', skin: 'vampire', hp: 3000, sc: 1.6, summon: 'vampM', bats: true,
    say: ['教堂地下室那口洋棺材，棺盖从里面推开了……', '西洋吸血鬼！十字架、圣水……还有糯米！'] },
  25: { name: '吸血鬼新娘', type: 'walker', skin: 'bride', hp: 4000, sc: 1.55, summon: 'wolf',
    say: ['白纱新娘提着裙摆，从教堂一路飘了过来……', '吸血鬼新娘带着狼人来了！'] },
  30: { name: '尸王·任老太爷', type: 'zombie', skin: 'king', hp: 7000, sc: 2.1, summon: 'zG', leaper: true, final: true,
    say: ['七七四十九天，蜻蜓点水穴里的老太爷……', '炼成尸王了！守住龙脉，这是最后一战！'] },
};
// 每一波开始时的旁白（参考林正英僵尸片）
const D_SAY = {
  1: ['鬼门关开了！三路阴兵往任家镇来了', '守住镇中心的龙脉！'],
  3: ['白僵出现了——怕火、怕光'],
  4: ['精英怪带着词缀，打掉有机会掉宝箱'],
  6: ['四目道长的赶尸队……一具具都在往这边跳'],
  8: ['四目道长赶尸路过任家镇，留下来助阵！他守在龙脉旁扔符'],
  11: ['女鬼哭了一整夜……白衣女鬼出没'],
  12: ['绿僵出现了！会蓄力扑跳'],
  16: ['教堂的钟自己响了。洋人的东西也来了：狼人、吸血鬼仆从'],
  21: ['阴气越来越重，镇上的狗都不叫了……'],
  26: ['子时三刻，百鬼夜行！'],
  28: ['再撑三波！鸡鸣之前，绝不能让龙脉断了'],
};
const D_FIELD = {   // 野外 BOSS：打死掉大宝箱和铜钱，三波后复活，更强
  tomb: { name: '古墓毛僵', mob: () => ['jumper', { elite: true, skin: 'jumperM', eliteHp: 6 }] },
  church: { name: '教堂狼人', mob: () => ['jumper', { elite: true, skin: 'wolf', eliteHp: 6 }] },
  grave: { name: '乱葬岗厉鬼', mob: () => ['ghost', { elite: true, skin: 'ghostR', eliteHp: 15 }] },
  yz: { name: '义庄老尸', mob: () => ['zombie', { elite: true, skin: 'corpse', eliteHp: 6 }] },
};
const D_ITEMS = [
  { k: 'heal', seal: '药', n: () => '金创药', d: () => '阳气回满', p: W => 30 },
  { k: 'core', seal: '脉', n: () => '修补龙脉', d: () => '龙脉灵气 +15（最多 100）', p: W => 50 + 15 * W.buy.core },
  { k: 'guard', seal: '兵', n: () => '招募保安队', d: () => '镇里多一名保安守着（最多再招 4 名）', p: W => 90 + 45 * W.buy.guard, max: 4 },
  { k: 'gun', seal: '枪', n: () => '洋枪洋炮', d: () => '镇上所有守卫伤害 +30%', p: W => Math.round(80 * Math.pow(1.6, W.buy.gun)), max: 5 },
  { k: 'bell', seal: '钟', n: () => '镇龙铜钟', d: W => ['龙脉每隔几秒震出一圈金光，击退并伤害周围的怪', '铜钟二级：范围更大、更疼', '铜钟三级：范围最大、伤害翻倍'][Math.min(2, W.buy.bell)], p: W => [150, 300, 500][W.buy.bell] || 0, max: 3 },
  { k: 'lv', seal: '法', n: () => (S.hero === 'monk' ? '少林秘籍' : S.hero === 'priest' ? '古卷圣典' : '茅山秘籍'), d: () => '修为立刻精进一重（三选一）', p: W => 110 + 40 * W.buy.lv },
];

// ---------- 原游戏里用不上的东西：关掉 ----------
function monkUnlocked() { return true; }
function runStart() { S.run = { tok: '' }; }
function runTick() {}
function updateZoneMusic() {}
function updateElites() {}
function updateWaterGhost() {}
function updateMap() { dMinimap(); }
function dEffT() { return S && S.dw ? Math.min(600, Math.max(0, (S.dw.wave - 1) * 20)) : 0; }   // 怪的血量/速度/伤害按波数成长（原游戏按时间）

// ---------- 通行：堵住时绕路去龙脉 ----------
function updateFlow() {
  if (FLOW) return;
  const C = COLS, R = (GRID.length / C) | 0, N = C * R;
  FLOW = new Int32Array(N); FLOW.fill(-1);
  const q = new Int32Array(N); let h0 = 0, t0 = 0;
  const pc = Math.min(R - 1, ((D_CORE[1] - 24) / CELLSZ) | 0) * C + ((D_CORE[0] / CELLSZ) | 0);
  FLOW[pc] = 0; q[t0++] = pc;
  while (h0 < t0) {
    const i = q[h0++], cx = i % C, cy = (i / C) | 0, dd = FLOW[i] + 1;
    for (let k = 0; k < 4; k++) {
      const nx = cx + (k === 0) - (k === 1), ny = cy + (k === 2) - (k === 3);
      if (nx < 0 || ny < 0 || nx >= C || ny >= R) continue;
      const j = ny * C + nx; if (FLOW[j] >= 0 || GRID.charCodeAt(j) === 49) continue;
      FLOW[j] = dd; q[t0++] = j;
    }
  }
}

// ---------- 怪往哪走：沿路去龙脉；玩家靠近就扑过来 ----------
function dLaneOf(e) {
  let best = 0, bd = 1e12;
  D_LANES.forEach((L, li) => {
    for (let i = 0; i < L.length - 1; i++) {
      const [x0, y0] = L[i], [x1, y1] = L[i + 1], L2 = (x1 - x0) ** 2 + (y1 - y0) ** 2 || 1, t = Math.max(0, Math.min(1, ((e.x - x0) * (x1 - x0) + (e.y - y0) * (y1 - y0)) / L2));
      const d = (e.x - x0 - (x1 - x0) * t) ** 2 + (e.y - y0 - (y1 - y0) * t) ** 2; if (d < bd) { bd = d; best = li; }
    }
  });
  e.lane = best; e.wp = 1; e.lo = e.lo ?? rnd(-9, 9);
}
function dCoreHit(n, e) {
  const W = S.dw; if (W.over) return;
  W.core = Math.max(0, W.core - n); W.coreFx = 0.5; S.shake = Math.max(S.shake, n >= 4 ? 0.2 : 0.08);
  S.texts.push({ x: D_CORE[0] + rnd(-10, 10), y: D_CORE[1] - 64, v: '龙脉 -' + n, t: 1, c: '#ff7a6a', big: n >= 4 });
  for (let i = 0; i < 8; i++) S.parts.push({ x: e.x, y: e.y - 8, vx: rnd(-50, 50), vy: rnd(-90, -30), t: rnd(0.4, 0.7), c: i % 2 ? '#6af0a0' : '#2a8a5a' });
  if (S.t > (W.coreSayT || 0)) { W.coreSayT = S.t + 6; sfx('roar'); }
  for (const th of [50, 25]) if (W.core <= th && !W['warn' + th]) { W['warn' + th] = true; banner(th === 50 ? '龙脉灵气只剩一半了！' : '龙脉快断了！！', 2.4); sfx('gong'); }
  if (W.core <= 0) { W.over = true; setTimeout(() => { if (S && S.dw === W && S.state !== 'over') endGame(false); }, 1200); banner('龙脉……断了', 3); S.shake = 0.6; sfx('boss'); }
}
function dTarget(e) {
  if (e.god || e.type === 'wuchang' || e.audience) return null;
  const P = S.p, W = S.dw;
  const see = !P.down && !(P.breath > 0) && !(S.pr && S.pr.mist > 0);
  const d2 = (P.x - e.x) ** 2 + (P.y - e.y) ** 2;
  if (e.field) {   // 野外 BOSS：只在自己的地盘里追人，追出去就回家
    const H = e.home, dh = (P.x - H[0]) ** 2 + (P.y - H[1]) ** 2;
    if (see && dh < 170 * 170 && d2 < 150 * 150) return null;
    const hx = H[0] - e.x, hy = H[1] - e.y;
    if (hx * hx + hy * hy < 64) { if (e.hp < e.max) e.hp = Math.min(e.max, e.hp + e.max * 0.08 * DT); return [0, 0]; }
    if (e.skin === 'ghostR') e.dashCd = Math.max(e.dashCd || 0, 0.6);
    return [hx, hy];
  }
  const R = e.boss ? 92 : e.elite ? 80 : 62;
  if (see && (d2 < R * R || (e.aggro && d2 < (R + 55) ** 2))) { e.aggro = true; return null; }
  e.aggro = false;
  if (e.skin === 'ghostR') e.dashCd = Math.max(e.dashCd || 0, 0.6);
  const cx = D_CORE[0] - e.x, cy = D_CORE[1] - e.y;
  if ((cx / 66) ** 2 + (cy / 40) ** 2 < 1) {   // 踏进龙脉石台
    if (e.boss) { e.coreT = (e.coreT ?? 0.4) - DT; if (e.coreT <= 0) { e.coreT = 1.6; dCoreHit(e.bossCore || 5, e); } return [0, 0]; }
    e.gone = true; dCoreHit(e.leak || 2, e); dMobGone(e); return [0, 0];
  }
  if (e.lane == null) dLaneOf(e);
  const L = D_LANES[e.lane];
  while (e.wp < L.length - 1) {   // 走到这个路点附近、或者已经越过它（朝下一个路点的方向）就换下一个
    const a = L[e.wp], b = L[e.wp + 1], dx = e.x - a[0], dy = e.y - a[1];
    if (dx * dx + dy * dy < 20 * 20 || dx * (b[0] - a[0]) + dy * (b[1] - a[1]) > 0) e.wp++; else break;
  }
  const t = L[e.wp], last = e.wp >= L.length - 1, nearGate = t[1] > MAP.wall[0] - 40 && t[1] < D_TOWN_Y + 160;
  return [t[0] + (last || nearGate ? 0 : e.lo || 0) - e.x, t[1] - e.y];
}

// ---------- 刷怪 ----------
function dMob(kind, x, y) {
  let e = null;
  if (kind === 'ghost') e = spawn('ghost', x, y);
  else if (kind === 'ghostW') { e = spawn('ghost', x, y, { skin: 'ghostW' }); if (e) { e.hp = e.max = e.max * 1.8; e.xp *= 1.5; } }
  else if (kind === 'walk') { e = spawn('walker', x, y); if (e) { const r = Math.random(); if (r < 0.3) e.skin = 'walkF'; else if (r < 0.55) e.skin = 'walkS'; } }
  else if (kind === 'zP' || kind === 'zW' || kind === 'zG') {
    e = spawn('zombie', x, y); if (e) { e.skin = kind; if (kind === 'zP') { e.hp = e.max = e.max * 0.8; e.spd *= 0.85; } if (kind === 'zG') { e.spd *= 1.2; e.leaper = true; e.leapCd = rnd(1.5, 3.5); } }
  } else if (kind === 'corpse') { e = spawn('zombie', x, y, { skin: 'corpse' }); if (e) { e.hp = e.max = e.max * 1.3; e.xp *= 1.3; } }
  else if (kind === 'jump') e = spawn('jumper', x, y);
  else if (kind === 'wolf' || kind === 'vampM' || kind === 'bride') e = church2Mob(kind === 'vampM' ? 'mob' : kind, x, y, false);
  return e;
}
function dPortal(lane) { const p = MAP.portals[lane]; return [p[0] + rnd(-16, 16), p[1] + rnd(6, 18)]; }
function dSpawnOne(q) {
  const W = S.dw, [x, y] = q.x != null ? [q.x, q.y] : dPortal(q.lane);
  let e;
  if (q.elite) {
    const red = q.elite === 'red';
    e = spawn(red ? 'ghost' : 'jumper', x, y, { elite: true, skin: red ? 'ghostR' : 'jumperM', eliteHp: red ? 15 : 6 });
    if (e) { const ak = Object.keys(AFFIX)[Math.floor(Math.random() * 5)]; e.affix = ak; e.born = S.t; S.affSeen = S.affSeen || {}; e.lblT = S.affSeen[ak] ? 1.4 : 5; S.affSeen[ak] = 1; e.leak = 6; }
  } else if (q.boss) e = dSpawnBoss(q.boss, x, y, q.lane);
  else e = dMob(q.kind, x, y);
  if (!e) return;
  e.lane = q.lane; e.wp = q.wp || 1; e.lo = rnd(-9, 9); e.wv = q.wv; e.dw = 1;
  if (!e.boss) { e.hp = e.max = e.max * dHpK(W.wave); e.xp *= Math.max(0.45, 1 - 0.02 * W.wave); if (e.elite) e.special = true; }
  if (q.x == null) { e.rise = 0.7; for (let i = 0; i < 6; i++) S.parts.push({ x: e.x + rnd(-6, 6), y: e.y - 2, vx: rnd(-40, 40), vy: rnd(-90, -30), t: rnd(0.3, 0.6), c: i % 2 ? '#ff5a6a' : '#5a1a2a' }); }
  W.alive[q.wv] = (W.alive[q.wv] || 0) + 1;
}
const dHpK = w => (1 + 0.1 * w + 0.004 * w * w) * (S.diff === 'hard' ? 0.85 : 1);   // 每波额外的血量倍率（原游戏的成长之外；困难本身已经 ×1.5）
function dMixFor(w) { const m = D_MIX.filter(r => w >= r[0] && w <= r[1]); return m; }
function dPick(m) { let s = 0; for (const r of m) s += r[3]; let x = Math.random() * s; for (const r of m) { x -= r[3]; if (x <= 0) return r[2]; } return m[0][2]; }
function dStartWave(w) {
  const W = S.dw, B = D_BOSS[w], D = DIFF[S.diff];
  W.wave = w; W.waveT = S.t; W.nextT = w >= D_WAVES ? 1e9 : S.t + (B ? 44 : 31);
  const n = Math.round((8 + w * 2.5) * (B ? 0.55 : 1) * D.spawn), dur = B ? 18 : 15, mix = dMixFor(w);
  for (let i = 0; i < n; i++) W.q.push({ t: S.t + 1 + dur * i / n + rnd(-0.3, 0.3), kind: dPick(mix), lane: i % 3, wv: w });
  const ne = w >= 4 ? Math.floor((w - 1) / 4) : 0;
  for (let i = 0; i < ne; i++) W.q.push({ t: S.t + 4 + dur * (i + 0.5) / ne, elite: i % 2 ? 'red' : 'hairy', lane: Math.floor(Math.random() * 3), wv: w });
  if (B) W.q.push({ t: S.t + 3, boss: w, lane: 1, wv: w });
  W.q.sort((a, b) => a.t - b.t);
  W.spawnEnd = S.t + dur + 2;
  sfx('gong'); setTimeout(() => sfx('gong'), 380);
  banner(B ? `第${dNum(w)}波 · ${B.name}` : `第${dNum(w)}波`, 2.2);
  if (D_SAY[w]) rumor(D_SAY[w], w === 1 || w === 26);
  if (B) { rumor(B.say, true); sfx('boss'); S.shake = 0.3; }
  if (w === 8) dSimuJoin();
  if (MAP.watch) S.texts.push({ x: MAP.watch[0], y: MAP.watch[1] - 40, v: '咚——哐！第' + dNum(w) + '波！', t: 2, c: '#ffe070', big: true });
  W.callable = false;
}
function dSpawnBoss(w, x, y, lane) {
  const B = D_BOSS[w], D = DIFF[S.diff];
  const e = spawn(B.type, x, y, { elite: true, skin: B.skin, eliteHp: 6 }); if (!e) return null;
  e.hp = e.max = B.hp * (1 + 0.06 * w) * D.hp; e.boss = w; e.special = true; e.bsc = B.sc; e.r = 9; e.leak = 0;
  e.bossCore = B.final ? 6 : 3; e.sumT = S.t + 7; e.xp = 40; e.nopois = true;
  if (B.leaper) { e.leaper = true; e.leapCd = rnd(2, 3); }
  if (B.type === 'walker') e.spd *= 1.15;
  e.dmg = Math.round(e.dmg * (B.final ? 1.4 : 1.15));
  S.dw.boss = e; S.dw.awFled = false;
  return e;
}
function dBossTick(e) {   // BOSS 定时召唤小怪；吸血鬼放蝙蝠
  const B = D_BOSS[e.boss]; if (!B || e.dead || e.rise > 0) return;
  if (S.t >= e.sumT) {
    e.sumT = S.t + (B.final ? 7 : 9);
    const n = 2 + Math.floor(e.boss / 10) + (S.diff === 'hard' ? 1 : 0);
    for (let i = 0; i < n; i++) {
      const a = i / n * 6.283, m = dMob(B.summon, e.x + Math.cos(a) * 18, e.y + Math.sin(a) * 12);
      if (m) { m.lane = e.lane; m.wp = e.wp; m.lo = rnd(-9, 9); m.wv = S.dw.wave; m.dw = 1; m.rise = 0.6; m.xp *= 0.4; m.hp = m.max = m.max * dHpK(e.boss); S.dw.alive[m.wv] = (S.dw.alive[m.wv] || 0) + 1; }
    }
    S.texts.push({ x: e.x, y: e.y - 58, v: '召！', t: 1, c: '#ff7a6a', big: true }); sfx('roar');
    for (let i = 0; i < 14; i++) S.parts.push({ x: e.x + rnd(-14, 14), y: e.y - 4, vx: rnd(-60, 60), vy: rnd(-100, -30), t: rnd(0.4, 0.8), c: '#7a3a6a' });
  }
  if (B.bats) {
    const P = S.p, d = Math.hypot(P.x - e.x, P.y - e.y);
    e.batCd = (e.batCd ?? 3) - DT;
    if (e.batCd <= 0 && d < 220 && !P.down) {
      e.batCd = rnd(3.5, 5); const a0 = Math.atan2(P.y - 10 - (e.y - 20), P.x - e.x); sfx('wisp');
      for (let i = -1; i <= 1; i++) { const a = a0 + i * 0.28; S.eshots.push({ k: 'bat', x: e.x, y: e.y - 20, vx: Math.cos(a) * 80, vy: Math.sin(a) * 80, life: 3, a, ph: 0, dmg: Math.round(8 * DIFF[S.diff].dmg) }); }
    }
  }
}
function dWispTick() {   // 进了镇的游魂、女鬼会远远朝龙脉吐阴火
  const W = S.dw, cx = D_CORE[0], cy = D_CORE[1] - 30;
  for (const e of S.en) {
    if (e.dead || e.rise > 0 || e.type !== 'ghost' || e.god || e.field || e.y < D_TOWN_Y) continue;
    if ((e.x - cx) ** 2 + (e.y - cy) ** 2 > 150 * 150) continue;
    e.wispT = (e.wispT ?? rnd(1, 3)) - DT;
    if (e.wispT > 0) continue;
    e.wispT = rnd(4, 6);
    W.wisps.push({ x: e.x, y: e.y - 14, t: 0, T: Math.hypot(e.x - cx, e.y - 14 - cy) / 90 });
    sfx('wisp');
  }
  for (const w of W.wisps) { w.t += DT; if (w.t >= w.T && !w.hit) { w.hit = true; dCoreHit(1, { x: cx, y: cy + 20 }); } }
  W.wisps = W.wisps.filter(w => !w.hit);
}
function dMobGone(e) { const W = S.dw; if (e.dw && e.wv) W.alive[e.wv] = Math.max(0, (W.alive[e.wv] || 0) - 1); if (W.boss === e) W.boss = null; }
function dKill(e) {   // 原游戏 hurt() 里怪死的时候调用
  const W = S.dw; if (!W) return;
  dMobGone(e);
  const g = e.boss ? 120 + e.boss * 4 : e.field ? 45 + 4 * W.wave : e.elite ? 8 : e.type === 'ghost' ? 1 : 2;
  W.gold += g; W.goldT = 0.4;
  if (g >= 5) { S.texts.push({ x: e.x, y: e.y - 44, v: '+' + g + '文', t: 1.2, c: '#ffd040', big: g >= 40 }); sfx('coin'); }
  if (e.boss) {
    const B = D_BOSS[e.boss];
    S.chests.push({ x: e.x, y: e.y, big: true, t: 0 }); S.chests.push({ x: e.x + 18, y: e.y + 6, big: false, t: 0 });
    banner(`${B.name} 伏诛！`, 2.6); S.shake = 0.4; sfx('boss');
    for (let i = 0; i < 6; i++) S.orbs.push({ x: e.x + rnd(-12, 12), y: e.y + rnd(-8, 8), v: 5, du: true });
    if (B.final) W.bossDead = true;
  }
  if (e.elite && e.dw && !e.boss && Math.random() < 0.2) S.chests.push({ x: e.x, y: e.y, big: false, t: 0 });
  if (e.field) {
    const F = W.field[e.field]; F.e = null; F.back = W.wave + 3; F.kills++;
    S.chests.push({ x: e.x, y: e.y, big: true, t: 0 });
    banner(`斩了${D_FIELD[e.field].name}！`, 2); sfx('ultcard');
  }
}
// ---------- 野外 BOSS ----------
function dFieldTick() {
  const W = S.dw;
  for (const k in W.field) {
    const F = W.field[k];
    if (F.e && (F.e.dead || !S.en.includes(F.e))) F.e = null;
    if (F.e || W.wave < F.back) continue;
    const [type, opt] = D_FIELD[k].mob(), H = MAP.fields[k].home;
    const e = spawn(type, H[0], H[1], opt); if (!e) continue;
    const D = DIFF[S.diff];
    e.hp = e.max = (200 + 60 * Math.max(1, W.wave)) * D.hp * (1 + 0.25 * F.kills); e.field = k; e.home = H; e.special = true; e.rise = 1.2; e.xp = 12;
    e.dmg = Math.round(e.dmg * 1.1); if (e.skin === 'wolf') e.spd *= 1.2;
    F.e = e; F.back = 1e9;
    if (F.kills) S.texts.push({ x: H[0], y: H[1] - 50, v: D_FIELD[k].name + '又回来了', t: 2, c: '#ff8a6a', big: true });
  }
}
// ---------- 守卫：阿威队长、保安队、四目道长 ----------
function dGuardsInit() {
  const W = S.dw; W.men = [];
  MAP.guards.forEach((p, i) => W.men.push({ k: i ? 'sold' : 'cap', x: p[0], y: p[1], hx: p[0], hy: p[1], cd: rnd(0.2, 1), face: 1 }));
}
function dAddGuard() { const W = S.dw, p = MAP.guardsX[W.buy.guard - 1]; if (p) W.men.push({ k: 'sold', x: p[0], y: p[1] + 30, hx: p[0], hy: p[1], cd: 1, face: 1, walk: 0 }); }
function dSimuJoin() {
  const W = S.dw; if (W.men.some(m => m.k === 'simu')) return;
  const p = MAP.simu; W.men.push({ k: 'simu', x: p[0], y: D_TOWN_Y + 20, hx: p[0], hy: p[1], cd: 1, face: 1, walk: 0 });
  window.sayKey && window.sayKey('simu1', 0.9);
}
function dGuardTick() {
  const W = S.dw, mul = Math.pow(1.3, W.buy.gun);
  for (const m of W.men) {
    if (m.trT > 0) m.trT -= DT;
    let tx = m.hx, ty = m.hy;
    if (m.k === 'cap' && m.flee > 0) { m.flee -= DT; tx = 378; ty = 1294; if (m.flee <= 0) S.texts.push({ x: m.x, y: m.y - 40, v: '咳……刚才是战术撤退！', t: 2, c: '#ffffff' }); }
    const dx = tx - m.x, dy = ty - m.y, dd = Math.hypot(dx, dy);
    if (dd > 1.5) { const sp = m.flee > 0 ? 75 : 40; m.x += dx / dd * Math.min(dd, sp * DT); m.y += dy / dd * Math.min(dd, sp * DT); m.walk = (m.walk || 0) + DT; if (Math.abs(dx) > 1) m.face = Math.sign(dx); continue; }
    if (m.k === 'cap' && !W.awFled && W.boss && !W.boss.dead && (W.boss.x - m.x) ** 2 + (W.boss.y - m.y) ** 2 < 90 * 90) {   // 阿威：见了大鬼先跑
      W.awFled = true; m.flee = 7; sfx('scream'); window.sayKey && window.sayKey('cap2', 1);
      S.texts.push({ x: m.x, y: m.y - 44, v: '鬼……鬼啊！', t: 2, c: '#ffffff', big: true }); continue;
    }
    m.cd -= DT; if (m.cd > 0) continue;
    const R = m.k === 'simu' ? 150 : 135;
    let tg = null, bd = R * R;
    for (const e of S.en) { if (e.dead || e.rise > 0 || e.god || e.batT > 0) continue; const d = (e.x - m.x) ** 2 + (e.y - m.y) ** 2; if (d < bd) { bd = d; tg = e; } }
    if (!tg) { m.cd = 0.2; continue; }
    m.face = tg.x < m.x ? -1 : 1;
    const base = (7 + 1.3 * W.wave) * mul;
    if (m.k === 'simu') {
      m.cd = 1.0; const a = Math.atan2(tg.y - 10 - (m.y - 14), tg.x - m.x); sfx('throw');
      S.shots.push({ k: 'fu', x: m.x, y: m.y - 14, vx: Math.cos(a) * 170, vy: Math.sin(a) * 170, life: 1.2, dmg: base * 1.3, pierce: 2, chance: 0.35, spin: 0, hit: new Set() });
    } else {
      m.cd = m.k === 'cap' ? 0.9 : 1.15; sfx('gun');
      m.tr = { x1: m.x + m.face * 12, y1: m.y - (m.k === 'cap' ? 17 : 14), x2: tg.x, y2: tg.y - 10 }; m.trT = 0.07;
      hurt(tg, base * (m.k === 'cap' ? 1.2 : 1), 25, m.x, m.y);
    }
  }
}
function dBellTick() {
  const W = S.dw, lv = W.buy.bell; if (!lv) return;
  W.bellT = (W.bellT ?? 2) - DT; if (W.bellT > 0) return;
  W.bellT = [0, 4, 3.5, 3][lv];
  const R = [0, 80, 100, 120][lv], dmg = (18 + 3 * W.wave) * [0, 1, 1.4, 2][lv], cy = D_CORE[1] - 10;
  S.fx.push({ k: 'pulse', x: D_CORE[0], y: cy, r: 8, R, t: 0, c: '#8af0b0' }); sfx('bell');
  for (const e of S.en) if (!e.dead && !e.god && (e.x - D_CORE[0]) ** 2 + ((e.y - cy) / 0.75) ** 2 < R * R) hurt(e, dmg, e.boss ? 40 : 160, D_CORE[0], cy, 'light');
}
// ---------- 重伤回镇 ----------
function offerRevive() {
  const P = S.p, W = S.dw; if (P.down || !W) return;
  if (window.sayDeath) sayDeath();
  W.deaths++; P.down = true; P.hp = 0; P.inv = 99; P.downT = Math.min(20, 5 + W.deaths * 3); P.breath = 0;
  for (let i = 0; i < 24; i++) { const an = i / 24 * 6.283; S.parts.push({ x: P.x, y: P.y - 12, vx: Math.cos(an) * 90, vy: Math.sin(an) * 90, t: 0.6, c: i % 2 ? '#c8302c' : '#f0c020' }); }
  S.shots.length = 0; S.sweeps.length = 0;
  P.x = D_CORE[0]; P.y = D_CORE[1] - 52;
  banner((S.hero === 'monk' ? '大师' : S.hero === 'priest' ? '神父' : '道长') + '重伤，回镇调息……', 2.2); sfx('hurt');
}
function dDownTick() {
  const P = S.p; if (!P.down) return;
  P.inv = 99; P.downT -= DT;
  if (P.downT <= 0) {
    P.down = false; P.hp = P.max; P.inv = 2; P.x = D_CORE[0]; P.y = D_CORE[1] - 52; sfx('ult'); banner('重返战场！', 1.4);
    for (let i = 0; i < 30; i++) { const an = i / 30 * 6.283; S.parts.push({ x: P.x, y: P.y - 12, vx: Math.cos(an) * 110, vy: Math.sin(an) * 110, t: 0.6, c: i % 2 ? '#ffd060' : '#fff6c0' }); }
  }
}

// ---------- 每帧：原游戏 update() 里调用的 updateEvents ----------
function updateEvents() {
  const W = S.dw, P = S.p;
  updateRumor();
  if (S.godNext && S.t >= S.godNext.t) { const k = S.godNext.k; S.godNext = null; spawnGod(k, Math.random() * 6.283); }
  updateGodFx();
  dDownTick();
  if (W.over) return;
  if (W.wave < D_WAVES && S.t >= W.nextT) dStartWave(W.wave + 1);
  while (W.q.length && W.q[0].t <= S.t) dSpawnOne(W.q.shift());
  W.callable = W.wave >= 1 && W.wave < D_WAVES && !W.q.length && S.t > W.spawnEnd && W.nextT - S.t > 3;
  // 一波清干净：奖励
  for (let w = W.cleared + 1; w <= W.wave; w++) {
    if (W.q.some(q => q.wv === w) || (W.alive[w] || 0) > 0 || S.t < W.waveT - 1) break;
    W.cleared = w; const bonus = 15 + 3 * w; W.gold += bonus; W.goldT = 0.6;
    if (w < D_WAVES) { rumor([`第${dNum(w)}波守住了！赏钱 ${bonus} 文` + (P.y >= D_TOWN_Y ? '' : '（回镇里可以去杂货铺买东西）')], false); sfx('coin'); }
  }
  for (const e of S.en) if (e.boss && !e.dead) dBossTick(e);
  dWispTick();
  dFieldTick(); dGuardTick(); dBellTick();
  for (const o of S.orbs) if ((o.age || 0) >= 2 && !P.down) o.pull = true;   // 阴德散在各路，过两秒自己飞回来
  W.coreFx = Math.max(0, (W.coreFx || 0) - DT); W.goldT = Math.max(0, (W.goldT || 0) - DT);
  if (W.wave >= D_WAVES && W.bossDead && !W.q.length && !S.en.some(e => !e.dead && e.dw)) dWin();
}
function dWin() {
  const W = S.dw; if (W.over) return; W.over = true; W.cleared = D_WAVES; W.win = true;
  for (const e of S.en) if (!e.dead) { e.stun = 99; e.sinkD = 1.5; }
  sfx('rooster'); banner('鸡鸣天亮，龙脉保住了！', 3.2);
  setTimeout(() => { if (S && S.dw === W && S.state !== 'over') endGame(true); }, 2600);
}

// ---------- 开局 ----------
function begin(diff) {
  const nm = cleanName($('startName').value);
  if (!nm) { const el = $('startName'); el.classList.remove('bad'); void el.offsetWidth; el.classList.add('bad'); $('nameTip').textContent = '道长还没留下尊姓大名'; el.focus(); return; }
  PNAME = nm; try { localStorage.setItem('ztzh_name', nm); } catch (e) {}
  audioInit(); whenReady(() => newGame(diff));
}
function newGame(diff = 'normal') {
  stopZoneMusic(); setHero(HERO); FLOW = null;
  const c = D_CORE;
  S = {
    hero: HERO, mk: { fx: [], beads: [], seals: [], bowls: [], pest: [], waves: [], lz: [], ch: 0, jiaT: 6, rezT: -99 },
    diff, bossKilled: false, parade: true, state: 'play', t: 0, kills: 0, lv: 1, xp: 0, need: 5, bossSpawned: true, bossWarn: true, roosterShown: true, stW: true, stG: true, nightX: 1e9,
    p: { x: c[0], y: c[1] - 52, hp: 100, max: 100, face: 1, inv: 0, moving: false, walk: 0, breath: 0, breathCd: 0, sprint: 0, sprintCd: 0 },
    mods: { speed: 0, magnet: 0, cd: 0, hp: 0, dmg: 0, regen: 0 },
    w: HERO === 'monk' ? { zhang: 1, jia: 1 } : HERO === 'priest' ? { cross: 1 } : { sword: 1 }, timers: {}, swordAng: 0, pr: HERO === 'priest' ? prNew() : null,
    objs: (MAP.objs || []).map(o => ({ ...o, burnt: false, state: 'ok', fireT: 0, smoke: 0, tk: 0 })), ult: null, ultCd: 0, sweeps: [], taijis: [], palms: [], afterimgs: [], ev: {}, allies: [], decor: [], batFx: [], rumorQ: [], guas: [], shield: 0, shieldT: null, chests: [], lvQueue: 0, eliteT: 1e9, eliteN: 0, vampOut: true, wgCd: 8, eshots: [], npcs: [], npcT: 1e9, loot: [], aw: null, awDone: true, yamT: 0, gongVo: 0, dawnT: null, yz: [], yzT: 1e9, fish: [], fishT: 1e9, cam: { x: 0, y: 0 },
    food: [], foodT: 25, parts: [], combo: 0, comboT: 0, stop: 0, flash: 0, en: [], shots: [], areas: [], orbs: [], fx: [], texts: [], spawnAcc: 0, nextId: 1, shake: 0,
    dw: { wisps: [], wave: 0, cleared: 0, nextT: 14, q: [], alive: {}, core: 100, gold: 40, deaths: 0, buy: { core: 0, guard: 0, gun: 0, bell: 0, lv: 0, heal: 0 }, men: [], field: {}, spawnEnd: 0, boss: null },
  };
  for (const k in D_FIELD) S.dw.field[k] = { e: null, back: 1, kills: 0 };
  dGuardsInit(); wallsInit();
  GUARD.reset(); if (HERO === 'monk') GUARD.pickW();
  for (const k of ['title', 'end', 'levelup', 'pause', 'revive', 'brag', 'tip', 'tipArrow', 'evArrow', 'shop']) $(k).hidden = true;
  $('mm').hidden = false; setMap(true, true, ''); S.tips = false; tipT = 0; S.wx = null;
  let plays = 0; try { plays = (+localStorage.getItem('lmai_plays') || 0) + 1; localStorage.setItem('lmai_plays', plays); } catch (e) {}
  S.dTips = plays <= 3;
  setWeather(pickWeather(), true); S.wxNext = rnd(50, 90);
  startAmbient();
  $('nameForm').hidden = true; boardNote = ''; myEntry = null;
  $('hud').hidden = false; $('breath').hidden = false; $('sprint').hidden = false; $('ult').hidden = true; $('banner').hidden = true; $('shopBtn').hidden = false;
  rumor(['任家镇。二十年前，风水先生给任老太爷点了「蜻蜓点水穴」……', '今夜起棺迁葬，尸身不腐——尸变了！', '阴气冲开了北山的鬼门关，三路阴兵直扑任家镇的龙脉。'], false);
  if (HERO === 'priest') rumor(['Father 柴：Lord, give me strength!'], false);
  last = performance.now();
}
function updateTips() {
  if (tipT > 0) { tipT -= DT; if (tipT <= 0) { $('tip').hidden = true; $('tipArrow').hidden = true; } }
  if (!S.dTips) return;
  const T = [[2, TOUCH ? '手指按住屏幕拖动 = 走路' : 'WASD / 方向键 = 走路'], [7, '怪从北边鬼门关三路杀来，沿着路直奔镇中心的龙脉'],
    [13, '龙脉灵气掉光就输了。看右上角小地图，红点是怪'], [24, '杀怪得铜钱。回到镇里（牌坊以内）点「铺」买东西'], [36, '野外四个地方各守着一只大怪，打死掉宝箱'],
    [50, '一波刷完以后，可以点「战」提前开打，剩几秒就多拿几文']];
  S.tipI = S.tipI || 0;
  while (S.tipI < T.length && S.t >= T[S.tipI][0]) showTip(T[S.tipI++][1], false, 4.2);
  if (S.ult && !S.ultTipShown) { S.ultTipShown = true; showTip(TOUCH ? '右下角出现了大招按钮，点它释放！' : '获得大招！按 Q 或点右下角按钮释放', true, 4.5); }
}

// ---------- 商铺 ----------
function dInTown() { return S && S.p.y >= D_TOWN_Y && !S.p.down; }
function dShopOpen() {
  if (!S || S.state !== 'play') return;
  if (!dInTown()) { S.texts.push({ x: S.p.x, y: S.p.y - 40, v: S.p.down ? '先调息……' : '回到镇里才能买东西', t: 1.2, c: '#ffd040', big: true }); sfx('hurt'); return; }
  S.state = 'shop'; dShopRender(); $('shop').hidden = false; sfx('pick');
}
function dShopClose() { if (!S || S.state !== 'shop') return; $('shop').hidden = true; S.state = 'play'; last = performance.now(); tryLevel(); }
function dShopRender() {
  const W = S.dw, box = $('shopItems'); box.innerHTML = '';
  $('shopGold').textContent = W.gold;
  D_ITEMS.forEach(it => {
    const p = it.p(W), maxed = it.max && W.buy[it.k] >= it.max, full = (it.k === 'core' && W.core >= 100) || (it.k === 'heal' && S.p.hp >= S.p.max);
    const b = document.createElement('button'); b.className = 'opt'; b.disabled = maxed || full || W.gold < p;
    b.innerHTML = `<span class="seal">${it.seal}</span><span>${it.n()}<span class="d">${it.d(W)}</span></span><span class="lv">${maxed ? '已满' : full ? '不用买' : p + ' 文'}</span>`;
    b.onclick = () => dBuy(it); box.appendChild(b);
  });
}
function dBuy(it) {
  const W = S.dw, p = it.p(W); if (W.gold < p || (it.max && W.buy[it.k] >= it.max)) return;
  W.gold -= p; W.buy[it.k]++; sfx('coin'); sfx('pickbig');
  if (it.k === 'heal') S.p.hp = S.p.max;
  else if (it.k === 'core') W.core = Math.min(100, W.core + 15);
  else if (it.k === 'guard') dAddGuard();
  else if (it.k === 'lv') S.lvQueue++;
  dShopRender();
}
$('shopBtn').onclick = () => dShopOpen();
$('shopClose').onclick = () => dShopClose();
$('callBtn').onclick = () => dCall();
function dCall() {
  const W = S && S.dw; if (!W || S.state !== 'play' || !W.callable) return;
  const b = Math.max(0, Math.ceil(W.nextT - S.t)); W.gold += b; W.nextT = S.t; W.callable = false;
  if (b) S.texts.push({ x: S.p.x, y: S.p.y - 44, v: '提前开战 +' + b + '文', t: 1.4, c: '#ffd040', big: true });
}
addEventListener('keydown', e => {
  if (!S || (e.target && e.target.tagName === 'INPUT')) return;
  if (e.code === 'KeyB') { if (S.state === 'shop') dShopClose(); else dShopOpen(); }
  if (e.code === 'Escape' && S.state === 'shop') dShopClose();
  if (e.code === 'KeyN') dCall();
});

// ---------- 画面：龙脉光、守卫、BOSS 名字、野外点名字 ----------
function drawEventSprites(list) {
  drawEventSprites0(list);
  const W = S.dw; if (!W) return;
  // 龙脉的光：灵气越少越红，越暗
  list.push({ y: D_CORE[1] - 0.5, f: () => {
    const k = W.core / 100, cx = D_CORE[0], cy = D_CORE[1] - 34, pul = 0.5 + 0.5 * Math.sin(S.t * 3);
    const col = k > 0.5 ? '120,240,170' : k > 0.25 ? '240,210,90' : '255,90,80';
    g.save(); g.globalCompositeOperation = 'lighter';
    g.globalAlpha = (0.12 + 0.1 * pul) * (0.4 + 0.6 * k) + (W.coreFx || 0) * 0.6; g.fillStyle = `rgb(${col})`;
    g.beginPath(); g.ellipse(cx, cy, 30 + pul * 4, 40 + pul * 4, 0, 0, 7); g.fill();
    g.globalAlpha = 0.5 * k; for (let i = 0; i < 4; i++) { const q = (S.t * 0.5 + i / 4) % 1; px(cx - 18 + i * 12 + Math.sin(S.t * 2 + i) * 3, cy + 26 - q * 60, 1, 2, `rgb(${col})`); }
    g.restore();
  } });
  if (W.coreFx > 0 || W.core < 100) list.push({ y: D_CORE[1] + 0.6, f: () => {
    const w = 46, x = D_CORE[0] - w / 2, y = D_CORE[1] - 92;
    px(x - 1, y - 1, w + 2, 5, '#1a0e1e'); px(x, y, w * W.core / 100, 3, W.core > 50 ? '#6af0a0' : W.core > 25 ? '#f0d060' : '#ff5a4a');
  } });
  for (const w of W.wisps) list.push({ y: 99990, f: () => {
    const k = Math.min(1, w.t / w.T), cx = D_CORE[0], cy = D_CORE[1] - 30, x = w.x + (cx - w.x) * k, y = w.y + (cy - w.y) * k - Math.sin(k * Math.PI) * 16, f = Math.sin(S.t * 30 + w.x) > 0;
    g.globalAlpha = 0.35; g.fillStyle = '#b06ae0'; g.beginPath(); g.arc(x, y, 6, 0, 7); g.fill(); g.globalAlpha = 1;
    px(x - 2, y - (f ? 4 : 3), 4, 6, '#1a0e1e'); px(x - 1, y - 2, 2, 4, '#d8a8ff'); px(x - 1, y - 1, 2, 2, '#ffffff');
  } });
  for (const m of W.men) list.push({ y: m.y, f: () => {
    const key = m.k === 'cap' ? (m.flee > 0 ? 'capN' : 'cap') : m.k, im = m.face < 0 ? flipped(key) : IMG[key];
    if (!im || !im.width) return;
    g.fillStyle = 'rgba(14,8,24,.45)'; g.beginPath(); g.ellipse(m.x, m.y, 7, 2, 0, 0, 7); g.fill();
    g.drawImage(im, Math.round(m.x - im.width / 2), Math.round(m.y - im.height + 2 - Math.abs(Math.sin((m.walk || 0) * 10)) * 1.2));
    if (m.trT > 0 && m.tr) { g.strokeStyle = '#fff6c0'; g.lineWidth = 1; g.beginPath(); g.moveTo(m.tr.x1, m.tr.y1); g.lineTo(m.tr.x2, m.tr.y2); g.stroke(); px(m.tr.x1 - 1, m.tr.y1 - 1, 3, 3, '#ffd040'); }
  } });
  if (MAP.watch) list.push({ y: MAP.watch[1], f: () => { const im = IMG.watch; if (im && im.width) g.drawImage(im, Math.round(MAP.watch[0] - im.width / 2), Math.round(MAP.watch[1] - im.height + 2)); } });
  if (MAP.shop) list.push({ y: MAP.shop[1], f: () => {
    const im = IMG.villager, [x, y] = MAP.shop; if (im && im.width) g.drawImage(im, Math.round(x - im.width / 2), Math.round(y - im.height + 2));
    if (dInTown() && Math.floor(S.t * 2) % 2) { g.font = 'bold 8px monospace'; g.textAlign = 'center'; g.fillStyle = '#1a0e1e'; g.fillText('杂货铺', x + 1, y - 33); g.fillStyle = '#ffe070'; g.fillText('杂货铺', x, y - 34); }
  } });
  for (const e of S.en) if ((e.boss || e.field) && !e.dead && !e.rise) list.push({ y: e.y + 0.7, f: () => {
    const im0 = IMG[e.skin], h = im0 ? im0.height * (e.bsc || 1.35) : 40, y = Math.round(e.y - h - 6), w = e.boss ? 40 : 28;
    px(e.x - w / 2 - 1, y - 1, w + 2, 4, '#1a0e1e'); px(e.x - w / 2, y, w * Math.max(0, e.hp / e.max), 2, e.boss ? '#ff4a3a' : '#ff9a3a');
    const nm = e.boss ? D_BOSS[e.boss].name : D_FIELD[e.field].name;
    g.font = 'bold 8px monospace'; g.textAlign = 'center'; g.fillStyle = '#1a0e1e'; g.fillText(nm, e.x + 1, y - 2); g.fillStyle = e.boss ? '#ff8a7a' : '#ffd090'; g.fillText(nm, e.x, y - 3);
  } });
  // 野外点名字（离得近才显示）
  for (const k in MAP.fields) { const F = MAP.fields[k], P = S.p; if ((P.x - F.c[0]) ** 2 + (P.y - F.c[1]) ** 2 > 200 * 200) continue;
    list.push({ y: -99998, f: () => { g.font = 'bold 9px monospace'; g.textAlign = 'center'; const y = F.c[1] - (k === 'church' ? 250 : 64); g.globalAlpha = 0.85; g.fillStyle = '#1a0e1e'; g.fillText(F.name, F.c[0] + 1, y + 1); g.fillStyle = '#e8d8ff'; g.fillText(F.name, F.c[0], y); g.globalAlpha = 1; } }); }
}

// ---------- 小地图：常开，显示三路的怪、龙脉、野外 BOSS ----------
function dMinimap() {
  if (!S || S.state === 'over') return;
  $('mmBtn').classList.remove('alert'); $('evArrow').hidden = true;
  if (!S.mmOpen) return;
  const cv2 = $('mmCv'), c = cv2.getContext('2d'), Wd = cv2.width, Hd = cv2.height, s = Math.min(Wd / WORLD.w, Hd / WORLD.h), ox = (Wd - WORLD.w * s) / 2;
  c.imageSmoothingEnabled = false; c.clearRect(0, 0, Wd, Hd);
  c.fillStyle = 'rgba(12,6,22,.75)'; c.fillRect(0, 0, Wd, Hd);
  if (IMG.bg && IMG.bg.complete) { c.globalAlpha = 0.9; c.drawImage(IMG.bg, 0, 0, WORLD.w, WORLD.h, ox, 0, WORLD.w * s, WORLD.h * s); c.globalAlpha = 1; }
  const C = S.cam; c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 1; c.strokeRect(Math.round(ox + C.x * s) + .5, Math.round(C.y * s) + .5, Math.round(VW * s), Math.round(VH * s));
  for (const e of S.en) { if (e.dead) continue; const big = e.boss || e.field || e.elite; c.fillStyle = e.boss ? '#ff3a2a' : e.field ? '#ffa040' : e.god ? '#ffffff' : '#e8584a'; const r = e.boss ? 3 : big ? 2 : 1; c.fillRect(Math.round(ox + e.x * s) - (r >> 1), Math.round(e.y * s) - (r >> 1), r, r); }
  const k = S.dw.core / 100; c.fillStyle = k > 0.5 ? '#6af0a0' : k > 0.25 ? '#f0d060' : '#ff5a4a'; c.beginPath(); c.arc(ox + D_CORE[0] * s, D_CORE[1] * s, 3 + Math.sin(S.t * 6), 0, 7); c.fill();
  c.fillStyle = '#ffe070'; c.beginPath(); c.arc(ox + S.p.x * s, S.p.y * s, 2.5, 0, 7); c.fill(); c.strokeStyle = '#1a0e1e'; c.stroke();
  for (const ch of S.chests) { if (ch.open) continue; c.fillStyle = '#ffe070'; c.fillRect(Math.round(ox + ch.x * s) - 1, Math.round(ch.y * s) - 1, 3, 3); }
  $('mmT').textContent = '';
}
$('mmBtn').onclick = () => { if (!S) return; sfx('pick'); setMap(!S.mmOpen, true, ''); };

function hud() {
  const P = S.p, W = S.dw;
  updateMap();
  $('hpb').firstElementChild.style.transform = `scaleX(${Math.max(0, P.hp / P.max)})`;
  $('xpb').firstElementChild.style.transform = `scaleX(${Math.min(1, S.xp / S.need)})`;
  $('lvl').textContent = `修为 ${cn(S.lv)}重`;
  $('shichen').textContent = W.wave ? `第${W.wave}/${D_WAVES}波` : '准备';
  const left = Math.max(0, W.nextT - S.t);
  $('till').textContent = P.down ? `调息中 ${Math.ceil(P.downT)} 秒` : W.wave >= D_WAVES ? (W.over ? '' : '最后一战！') : `下一波 ${Math.floor(left / 60)}:${String(Math.floor(left % 60)).padStart(2, '0')}`;
  $('coreb').firstElementChild.style.transform = `scaleX(${W.core / 100})`;
  $('coreb').className = 'bar' + (W.core <= 25 ? ' low' : W.core <= 50 ? ' mid' : '');
  $('coreV').textContent = `龙脉 ${Math.ceil(W.core)}`;
  const bv = $('bossV'), bo = W.boss && !W.boss.dead ? W.boss : null; bv.hidden = !bo;
  if (bo) bv.textContent = `${D_BOSS[bo.boss].name} ${Math.ceil(bo.hp / bo.max * 100)}% · ${bo.y > D_TOWN_Y ? '已进镇！' : ['西路', '正路', '东路'][bo.lane] || ''}`;
  $('kills').textContent = S.kills;
  const gv = $('gold'); gv.textContent = W.gold; gv.classList.toggle('pop', W.goldT > 0);
  $('combo').textContent = S.combo >= 5 ? (S.combo < 100 ? cn(S.combo) : S.combo) + '连斩' : '';
  const cb = $('callBtn'); cb.hidden = !W.callable || P.down; if (!cb.hidden) cb.textContent = `战 +${Math.ceil(left)}文`;
  $('shopBtn').classList.toggle('dim', !dInTown());
  if (S.ult) { const u = $('ult'); setCd(u, S.ultCd / 30); const h = `${ULTS[S.ult.k].seal}<small>Q</small>`; if (u.innerHTML !== h) u.innerHTML = h; }
  const sb = $('sprint'); setCd(sb, P.sprintCd / 60); sb.classList.toggle('on', P.sprint > 0);
  if (!sb.innerHTML.startsWith('神行')) sb.innerHTML = '神行<small>E</small>';
  const b = $('breath'); setCd(b, P.breathCd / 12);
  if (!b.innerHTML.startsWith('屏息')) b.innerHTML = '屏息<small>空格</small>';
}
function drawIdle(t) {
  g.fillStyle = '#140c22'; g.fillRect(0, 0, VW, VH);
  if (IMG.bg.complete) g.drawImage(IMG.bg, -Math.round(Math.max(0, (WORLD.w - VW) / 2) + Math.sin(t / 5000) * 40), -Math.round(Math.max(0, WORLD.h - VH - 60) - (Math.sin(t / 7000) + 1) * 200));
  g.fillStyle = 'rgba(8,4,16,.45)'; g.fillRect(0, 0, VW, VH);
  ctx.drawImage(low, 0, 0, VW * SCALE, VH * SCALE);
}

// ---------- 结算 ----------
function endGame(win) {
  if (S.state === 'over') return;
  if (!win && window.sayDeath) sayDeath();
  const W = S.dw; S.state = 'over'; for (const k of ['shop', 'levelup']) $(k).hidden = true;
  $('endT').textContent = win ? '鸡鸣天亮，龙脉保住了！' : '龙脉……断了';
  $('endP').textContent = (win ? `守住全部三十波！` : `守到第${dNum(Math.max(1, W.wave))}波，守住 ${W.cleared} 波。`) + `伏尸 ${S.kills} 具，修为 ${cn(S.lv)}重。（${DIFF[S.diff].name}）`;
  S.score = Math.round((W.cleared * 120 + S.kills + S.lv * 20 + (win ? 3000 + Math.round(W.core) * 20 : 0)) * DIFF[S.diff].mul);
  S.win = win; $('scoreV').textContent = S.score; stopZoneMusic();
  if (S.soulTaken) { $('endT').textContent = '阳寿已尽——逆天改命，被勾了魂'; }
  { const ec = $('endCheat'); ec.className = S.cheat ? 'bad' : 'ok'; ec.textContent = S.cheat ? '⚠ 本局判定：作弊（成绩会标注【作弊】）' : '✔ 本局判定：未作弊'; }
  renderBoard();
  $('end').hidden = false; $('breath').hidden = true; $('sprint').hidden = true; $('ult').hidden = true; $('shopBtn').hidden = true; $('callBtn').hidden = true;
  $('nameForm').hidden = true; $('brag').hidden = true; saveRecord(PNAME || '无名道士');
  setTimeout(() => $('againBtn').focus(), 50);
}

// ---------- 排行榜：龙脉功德簿（独立于原游戏的功德簿） ----------
async function webGet() { const r = await fetch('/api/longmai', { cache: 'no-store' }); if (!r.ok) throw new Error('http ' + r.status); const j = await r.json(); if (!Array.isArray(j)) throw new Error('bad'); return j; }
async function webPost(rec) { const r = await fetch('/api/longmai', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(rec) }); if (!r.ok) throw new Error('http ' + r.status); const j = await r.json(); if (!Array.isArray(j)) throw new Error('bad'); return j; }
function localBoard() { try { return JSON.parse(localStorage.getItem('lmai_board') || '[]'); } catch (e) { return []; } }
const dHeroMark = r => (r.hero === 'monk' ? '卍 ' : r.hero === 'priest' ? '✝︎ ' : '☯︎ ');
async function loadRank() {
  let rows = null, shared = false;
  if (DB) { try { const snap = await DB.collection('longmai').orderBy('score', 'desc').limit(100).get(); rows = snap.docs.map(d => d.data()).filter(Boolean); shared = true; } catch (e) { rows = null; } }
  if (!rows && WEB) { try { rows = await webGet(); shared = true; } catch (e) { rows = null; } }
  if (!rows) rows = localBoard();
  return { rows, shared };
}
async function showRank() {
  $('title').hidden = true; $('rank').hidden = false; $('rankTitle').textContent = '龙脉功德簿';
  $('rankN').innerHTML = $('rankH').innerHTML = '<div class="empty">读取中……</div>'; $('rankNote').textContent = '';
  const { rows, shared } = await loadRank();
  let me = ''; try { me = localStorage.getItem('ztzh_name') || ''; } catch (e) {}
  const fill = (el, diff) => {
    const list = rows.filter(r => (r.diff === 'hard') === (diff === 'hard')).sort((a, b) => (b.score || 0) - (a.score || 0));
    el.textContent = '';
    if (!list.length) { el.innerHTML = '<div class="empty">还没有人上榜</div>'; return null; }
    const t = document.createElement('table');
    list.slice(0, 20).forEach((r, i) => {
      const tr = document.createElement('tr'); tr.className = (me && r.name === me ? 'me ' : '') + (r.cheat ? 'ch' : '');
      for (const v of [i + 1, dHeroMark(r) + String(r.name || '无名道士').slice(0, 10) + (r.win ? ' ☀' : ` 守${r.wave || 0}波`) + (r.cheat ? ' 【作弊】' : ''), Number(r.score) || 0]) { const td = document.createElement('td'); if (typeof v === 'string') { const sp = document.createElement('span'); sp.className = 'nm'; sp.textContent = v; td.appendChild(sp); } else td.textContent = v; tr.appendChild(td); }
      t.appendChild(tr);
    });
    el.appendChild(t);
    const idx = me ? list.findIndex(r => r.name === me && !r.cheat) : -1;
    return idx >= 0 ? { rank: idx + 1, score: list[idx].score } : null;
  };
  const a = fill($('rankN'), 'normal'), b = fill($('rankH'), 'hard'), parts = [];
  if (a) parts.push(`普通第 ${a.rank} 名（${a.score} 分）`); if (b) parts.push(`困难第 ${b.rank} 名（${b.score} 分）`);
  $('rankNote').textContent = (shared ? '' : '暂时连不上共享功德簿，以下是本机记录。 ') + (parts.length ? `你（${me}）：` + parts.join('，') : (me ? '你还没上榜，去守龙脉吧！' : '')) + '　☀ = 守住三十波　守N波 = 守住了几波';
}
$('rankBtn').onclick = () => showRank();
async function renderBoard() {
  const box = $('board'); const { rows, shared } = await loadRank();
  box.textContent = '';
  const h = document.createElement('h3'); h.textContent = shared ? '龙脉功德簿 · 所有道友' : '龙脉功德簿 · 本机'; box.appendChild(h);
  if (!rows.length) { const p = document.createElement('div'); p.className = 'empty'; p.textContent = boardNote || '还没有记录，留下你的道号做第一个。'; box.appendChild(p); return; }
  const t = document.createElement('table'), hr = document.createElement('tr');
  for (const c of ['名次', '道号', '积分', '难度', '战果']) { const th = document.createElement('th'); th.textContent = c; hr.appendChild(th); }
  t.appendChild(hr);
  rows.slice().sort((a, b) => (b.score || 0) - (a.score || 0)).slice(0, 10).forEach((r, i) => {
    const tr = document.createElement('tr');
    if (myEntry && r.at === myEntry.at && r.name === myEntry.name) tr.className = 'me';
    if (r.cheat) tr.className += ' ch';
    for (const v of [i + 1, dHeroMark(r) + String(r.name || '无名道士').slice(0, 10), Number(r.score) || 0, r.diff === 'hard' ? '困难' : '普通', (r.win ? '全守住' : `守住${r.wave || 0}波`) + (r.cheat ? ' · 作弊' : '')]) { const td = document.createElement('td'); td.textContent = v; tr.appendChild(td); }
    t.appendChild(tr);
  });
  box.appendChild(t);
  if (boardNote) { const n = document.createElement('div'); n.className = 'empty'; n.textContent = boardNote; box.appendChild(n); }
}
async function saveRecord(name) {
  if (!S || S.state !== 'over' || S.saved) return;
  S.saved = true; const W = S.dw;
  const rec = { name, score: S.score, kills: S.kills, lv: S.lv, wave: W.cleared, t: Math.floor(S.t), win: !!S.win, diff: S.diff, at: Date.now(), hero: S.hero, cheat: S.cheat || 0, dev: DEVTAG() };
  myEntry = rec;
  if (rec.cheat) boardNote = '这一局逆天改命，成绩已记入功德簿，并标注【作弊】。';
  try { const arr = localBoard(); arr.push(rec); arr.sort((a, b) => b.score - a.score); localStorage.setItem('lmai_board', JSON.stringify(arr.slice(0, 20))); } catch (e) {}
  if (!DB && WEB) { try { await webPost(rec); } catch (e) { boardNote = '这次成绩只记在本机：暂时连不上共享功德簿。'; } }
  if (DB && USER && !rec.cheat) {
    try { const uid = await USER.id(); if (!uid) throw new Error('no id'); const ref = DB.doc('longmai/' + uid), old = await ref.get(), od = old.data && old.data(); if (!od || (Number(od.score) || 0) < rec.score) await ref.set(rec); }
    catch (e) { boardNote = '这次成绩只记在本机。'; }
  }
  renderBoard(); $('bragNote').textContent = ''; $('brag').hidden = false;
}

// ---------- 分享 / 战绩海报 ----------
$('shareBtn').onclick = async () => {
  const r = await doShare('《守卫任家镇的中心的龙脉》鬼门关开，三路阴兵直扑任家镇，你能守几波？', '发给朋友吧，发完回来点任意处继续');
  shareToast(r === 'copied' || r === 'wechat' ? '已复制链接，去粘贴给朋友吧' : r === 'manual' ? '复制失败，请手动复制地址栏里的链接' : '');
};
function makePoster() {
  const Wp = 360, Hp = 572, k = 2, cv2 = document.createElement('canvas'); cv2.width = Wp * k; cv2.height = Hp * k;
  const c = cv2.getContext('2d'); c.imageSmoothingEnabled = false; c.scale(k, k);
  const F = '"ZCOOL QingKe HuangYou", "PingFang SC", "Microsoft YaHei", sans-serif', W = S.dw;
  c.fillStyle = '#140c22'; c.fillRect(0, 0, Wp, Hp);
  c.drawImage(IMG.bg, D_CORE[0] - 180, D_CORE[1] - 250, 360, 300, 0, 70, 360, 300);
  const gr = c.createLinearGradient(0, 70, 0, 370); gr.addColorStop(0, 'rgba(20,12,34,.85)'); gr.addColorStop(.35, 'rgba(20,12,34,.2)'); gr.addColorStop(1, 'rgba(20,12,34,.95)');
  c.fillStyle = gr; c.fillRect(0, 70, 360, 300);
  const spr = (key, x, by, s, flip) => { const im = flip ? flipped(key) : IMG[key]; if (im && im.width) c.drawImage(im, Math.round(x - im.width * s / 2), Math.round(by - im.height * s), Math.round(im.width * s), Math.round(im.height * s)); };
  spr('longmai', 180, 300, 1.4); spr('king', 290, 230, 2, true); spr('jumperM', 70, 250, 2); spr('cap', 60, 352, 2); spr('sold', 300, 352, 2, true);
  spr(HK(), 180, 360, 3, false);
  c.textAlign = 'center';
  c.font = `34px ${F}`; for (const [dx, col] of [[3, '#1a0e1e'], [2, '#c8302c'], [0, '#f4e4a8']]) { c.fillStyle = col; c.fillText('守卫任家镇的龙脉', 180 + dx, 50 + dx); }
  c.fillStyle = '#2a1d40'; c.fillRect(14, 384, 332, 100); c.strokeStyle = '#4a3866'; c.lineWidth = 2; c.strokeRect(14, 384, 332, 100);
  const nm = PNAME || '道长';
  c.fillStyle = '#f0c020'; c.font = `22px ${F}`; c.fillText(S.win ? `${nm} 守住了三十波！` : `${nm} 守到了第${dNum(Math.max(1, W.wave))}波`, 180, 414);
  c.fillStyle = '#ece4ff'; c.font = `16px ${F}`; c.fillText(`积分 ${S.score || 0} · 伏尸 ${S.kills} 具 · 修为${cn(S.lv)}重`, 180, 442);
  c.fillStyle = '#ff8a7a'; c.fillText('你的朋友一定守不住，不信试试', 180, 468);
  if (S.cheat) { c.save(); c.translate(272, 300); c.rotate(-0.3); c.strokeStyle = 'rgba(210,44,40,.9)'; c.lineWidth = 6; c.strokeRect(-72, -36, 144, 72); c.fillStyle = 'rgba(210,44,40,.9)'; c.font = `48px ${F}`; c.textBaseline = 'middle'; c.fillText('作弊', 0, 2); c.restore(); }
  const q = IMG.qr; c.fillStyle = '#140c22'; c.fillRect(0, 488, Wp, Hp - 488);
  const qsz = q.width * 2, qy = 494, qx = 22; c.fillStyle = '#ffffff'; c.fillRect(qx - 3, qy - 3, qsz + 6, qsz + 6); c.drawImage(q, qx, qy, qsz, qsz);
  c.textAlign = 'left'; c.fillStyle = '#f4e4a8'; c.font = `18px ${F}`; c.fillText('长按识别二维码', 98, 516);
  c.fillStyle = '#a99cc8'; c.font = `13px ${F}`; c.fillText('鬼门关开，三路阴兵，你能守几波', 98, 538);
  c.fillText(D_SITE.replace('https://', ''), 98, 554);
  return cv2;
}
renderHeroes();
