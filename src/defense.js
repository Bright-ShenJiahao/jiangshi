
// =====================================================================
// 守卫任家镇的中心的龙脉 —— 防守模式的逻辑
// 数据（怪、BOSS、每一波、剧情文字、数值）都在 defense_data.js；这里是怎么用这些数据。
// 这一段接在原游戏脚本的最后：同名函数会覆盖原游戏的版本。
// =====================================================================
const D_LANES = MAP.lanes, D_CORE = MAP.core, D_N = D_WAVES.length, D_TOWN_Y = MAP.townY;
const D_BOSS = D_BOSSES;
const D_SITE = SITE + 'longmai.html';
const dNum = n => cn(n);

// ---------- 原游戏里用不上的东西：关掉 ----------
function monkUnlocked() { return true; }
function runStart() { S.run = { tok: '' }; }
function runTick() {}
function updateZoneMusic() {}
function updateElites() {}
function updateWaterGhost() {}
function updateMap() { dMinimap(); }
function dEffT() { return S && S.dw ? D_TUNE.effT(Math.max(1, S.dw.wave)) : 0; }
const dHpK = w => D_TUNE.hpK(w) * (S.diff === 'hard' ? 0.85 : 1);

// ---------- 怪往哪走：沿路去龙脉；玩家靠近就扑过来 ----------
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
  if (e.dabao) return null;   // 被王婆控制的大宝：只追穿道袍的人
  const B = W.bait;
  if (B && B.hp > 0 && !e.boss) {   // 文才当诱饵：附近的鬼都去追他
    const bd = (B.x - e.x) ** 2 + (B.y - e.y) ** 2;
    if (bd < (e.type === 'ghost' ? 230 : 150) ** 2 && !(see && d2 < 50 * 50)) {
      if (bd < 14 * 14) { e.baitT = (e.baitT || 0) - DT; if (e.baitT <= 0) { e.baitT = 0.8; B.hp -= Math.max(2, e.dmg * 0.5); B.hitT = 0.2; } }
      return [B.x - e.x, B.y - e.y];
    }
  }
  if (e.follow) {   // 屠龙运尸队：跟着领头的屠龙排队跳
    const L = e.follow;
    if (L.dead || !S.en.includes(L)) e.follow = null;
    else { const tx = L.x - (L.face2 || 0) * 0, ty = L.y - 16 * (e.fi + 1); return [tx - e.x, ty - e.y]; }
  }
  if (e.bandit && !P.down) {   // 马贼鬼魂：先去找保安附身
    let best = null, bd = 170 * 170;
    for (const m of W.men) { if (m.k !== 'sold' && m.k !== 'cap' || m.pos > 0) continue; const dd = (m.x - e.x) ** 2 + (m.y - e.y) ** 2; if (dd < bd) { bd = dd; best = m; } }
    if (best) {
      if (bd < 16 * 16) { best.pos = 9; e.gone = true; dMobGone(e); sfx('scream'); S.texts.push({ x: best.x, y: best.y - 44, v: '马贼上身了！', t: 1.6, c: '#7af0d0', big: true }); return [0, 0]; }
      return [best.x - e.x, best.y - e.y];
    }
  }
  if (e.shisj && !(see && d2 < 70 * 70)) { const T = MAP.shop; return [T[0] + 30 - e.x, T[1] - e.y]; }   // 石少坚：直奔钱家
  const R = e.boss ? 92 : e.elite ? 80 : 62;
  if (see && (d2 < R * R || (e.aggro && d2 < (R + 55) ** 2))) { e.aggro = true; return null; }
  e.aggro = false;
  if (e.skin === 'ghostR') e.dashCd = Math.max(e.dashCd || 0, 0.6);
  const cx = D_CORE[0] - e.x, cy = D_CORE[1] - e.y;
  if (e.boss ? (cx / 100) ** 2 + (cy / 90) ** 2 < 1 : (cx / 66) ** 2 + (cy / 40) ** 2 < 1) {   // 踏进龙脉石台（BOSS 停在石碑外面）
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

// ---------- 按数据表造怪 ----------
function dMakeMob(def, x, y, elite) {
  if (!def) return null;
  let e;
  if (def.church) { e = church2Mob(def.church, x, y, !!elite); if (!e) return null; }
  else {
    const skin = def.skins ? def.skins[Math.floor(Math.random() * def.skins.length)] : def.skin;
    e = spawn(def.t, x, y, elite ? { elite: true, skin, eliteHp: def.eh || 5 } : skin ? { skin } : {}); if (!e) return null;
    if (skin === 'walker') delete e.skin;
  }
  if (def.hp) e.hp = e.max = e.max * def.hp;
  if (def.spd) e.spd *= def.spd;
  if (def.dmg) e.dmg = Math.round(e.dmg * def.dmg);
  if (def.xp) e.xp *= def.xp;
  if (def.kbk != null) e.kbk = def.kbk;
  if (def.r) e.r = def.r;
  if (def.leaper) { e.leaper = true; e.leapCd = rnd(1.5, 3.5); }
  if (def.dr) e.dr = def.dr;
  if (def.ice) e.ice = S.t + def.ice;
  if (def.blink) e.you = true;
  if (def.possess) e.bandit = true;
  if (def.wax) e.waxDrip = true;
  if (def.fireWeak) e.fireWeak = true;
  if (def.noWisp) e.noWisp = true;
  if (def.leak) e.leak = def.leak;
  if (def.dash) e.thug = true;
  if (def.charm) e.fcharm = true;
  if (e.type === 'walker') e.nopois = true;
  return e;
}
function dMob(kind, x, y) {
  if (kind === 'mix') kind = ['qingbing', 'feitou', 'tanG', 'jtZ', 'wolf', 'zG', 'tongZ', 'feiZ', 'bugu'][Math.floor(Math.random() * 9)];
  return dMakeMob(D_MOBS[kind], x, y, false);
}
function dPortal(lane) { const p = MAP.portals[lane]; return [p[0] + rnd(-16, 16), p[1] + rnd(6, 18)]; }
function dSpawnOne(q) {
  const W = S.dw, [x, y] = q.x != null ? [q.x, q.y] : dPortal(q.lane);
  let e;
  if (q.elite) {
    e = dMakeMob(D_ELITES[q.elite], x, y, true);
    if (e && !e.affix) { const ak = Object.keys(AFFIX)[Math.floor(Math.random() * 5)]; e.affix = ak; e.born = S.t; S.affSeen = S.affSeen || {}; e.lblT = S.affSeen[ak] ? 1.4 : 5; S.affSeen[ak] = 1; e.leak = e.leak || 6; }
  } else if (q.boss) e = dSpawnBoss(q.boss, x, y, q.lane);
  else e = dMob(q.kind, x, y);
  if (!e) return;
  e.lane = q.lane; e.wp = q.wp || 1; e.lo = rnd(-9, 9); e.wv = q.wv; e.dw = 1;
  if (!e.boss) { e.hp = e.max = e.max * dHpK(W.wave); e.xp *= Math.max(0.45, 1 - 0.03 * W.wave); if (e.elite) e.special = true; }
  if (q.fu) { e.rise = 1.8; e.lane = null; S.areas.push({ k: 'crack', x: e.x, y: e.y, r: 18, life: 2.5, seed: Math.random() * 1000 }); S.texts.push({ x: e.x, y: e.y - 30, v: q.door ? '作坊里冲出来了！' : '地下有东西！', t: 1.4, c: '#ffb070' }); sfx('thud'); }
  else if (q.x == null) { e.rise = 0.7; for (let i = 0; i < 6; i++) S.parts.push({ x: e.x + rnd(-6, 6), y: e.y - 2, vx: rnd(-40, 40), vy: rnd(-90, -30), t: rnd(0.3, 0.6), c: i % 2 ? '#ff5a6a' : '#5a1a2a' }); }
  W.alive[q.wv] = (W.alive[q.wv] || 0) + 1;
}
function dFuSpot() {   // 伏尸钻出来的地方：镇里的路上（离龙脉不太近）
  for (let k = 0; k < 30; k++) {
    const L = D_LANES[Math.floor(Math.random() * 3)], i = 7 + Math.floor(Math.random() * Math.max(1, L.length - 9)), a = L[Math.min(i, L.length - 2)], b = L[Math.min(i + 1, L.length - 1)], t = Math.random();
    const x = a[0] + (b[0] - a[0]) * t + rnd(-10, 10), y = a[1] + (b[1] - a[1]) * t;
    if (y > D_TOWN_Y + 10 && (x - D_CORE[0]) ** 2 + (y - D_CORE[1]) ** 2 > 130 * 130 && freeAt(x, y)) return [x, y];
  }
  return [MAP.gates[Math.floor(Math.random() * 3)], D_TOWN_Y + 30];
}
function dPick(m) { let s = 0; for (const k in m) s += m[k]; let x = Math.random() * s; for (const k in m) { x -= m[k]; if (x <= 0) return k; } return Object.keys(m)[0]; }

// ---------- 开一波 ----------
function dStartWave(w) {
  const W = S.dw, WD = D_WAVES[w - 1], B = WD.boss, D = DIFF[S.diff], T = D_TUNE;
  W.wave = w; W.waveT = S.t; W.nextT = w >= D_N ? 1e9 : S.t + (B || WD.long ? T.bossGap : T.waveGap);
  const n = Math.round(T.count(w) * (B ? 0.55 : 1) * D.spawn), dur = B ? T.bossSpawnDur : T.spawnDur;
  for (let i = 0; i < n; i++) {
    const kind = dPick(WD.mobs), q = { t: S.t + 1 + dur * i / n + rnd(-0.3, 0.3), kind, lane: i % 3, wv: w };
    if (D_MOBS[kind] && D_MOBS[kind].underground) { const p = dFuSpot(); q.x = p[0]; q.y = p[1]; q.fu = true; }
    if (kind === 'waxZ' && W.waxHouse && Math.random() < 0.7) { const p = MAP.lafang; q.x = p[0] + rnd(-8, 8); q.y = p[1] + rnd(0, 8); q.fu = true; q.door = true; }
    W.q.push(q);
  }
  (WD.elites || []).forEach((k, i, arr) => W.q.push({ t: S.t + 4 + dur * (i + 0.5) / arr.length, elite: k, lane: Math.floor(Math.random() * 3), wv: w }));
  if (B) W.q.push({ t: S.t + 3, boss: B, lane: 1, wv: w });
  W.q.sort((a, b) => a.t - b.t);
  W.spawnEnd = S.t + dur + 2;
  sfx('gong'); setTimeout(() => sfx('gong'), 380);
  banner(`第${dNum(w)}波 · ${B ? D_BOSSES[B].n : '《' + WD.film + '》'}`, 2.4);
  if (WD.tier) { rumor(['尸变·' + WD.tier], true); S.texts.push({ x: S.p.x, y: S.p.y - 60, v: '尸变：' + WD.tier.split('：')[0], t: 2.4, c: '#ff9a7a', big: true }); }
  if (WD.say) rumor(WD.say, w === 1);
  if (B) { rumor(D_BOSSES[B].say, true); sfx('boss'); S.shake = 0.3; }
  [].concat(WD.event || []).forEach(dEvent);
  if (MAP.watch) S.texts.push({ x: MAP.watch[0], y: MAP.watch[1] - 40, v: '咚——哐！第' + dNum(w) + '波！', t: 2, c: '#ffe070', big: true });
  W.callable = false;
}

// ---------- 剧情事件 ----------
function dEvent(k) {
  const W = S.dw, P = S.p;
  if (k === 'wencai') {   // 文才当诱饵：从城门沿正路走回鬼门关，把鬼魂引回阴间
    const L = D_LANES[1], path = L.slice(0, L.findIndex(p => p[1] >= D_TOWN_Y) + 1).reverse();
    W.bait = { x: path[0][0], y: path[0][1] + 10, path, i: 1, hp: 160, max: 160, t: 0 };
    rumor(['护送文才！他身上挂着引魂铃，鬼会去追他，别让他被缠死'], true);
  }
  if (k === 'pals') dPals(['dabao', 'xiaobao'], '明叔养的两只小鬼大宝、小宝来帮你！');
  if (k === 'nails') { W.nails = [5, 5, 5].map((wp, li) => { const p = D_LANES[li][wp]; return { x: p[0] + rnd(-30, 30), y: p[1] + rnd(-20, 20), pull: 0, tk: 4 }; }); }
  if (k === 'tulong') {
    const [x, y] = dPortal(1), L = dMakeMob({ t: 'walker', skin: 'tulong', eh: 6, spd: 0.9 }, x, y, true); if (!L) return;
    L.special = true; L.tulong = true; L.lane = 1; L.wp = 1; L.wv = W.wave; L.dw = 1; L.hp = L.max = L.max * dHpK(W.wave); W.alive[L.wv] = (W.alive[L.wv] || 0) + 1;
    for (let i = 0; i < 6; i++) { const c = dMob('corpse', x, y - 16 * (i + 1)); if (!c) continue; c.follow = L; c.fi = i; c.wv = W.wave; c.dw = 1; c.hp = c.max = c.max * dHpK(W.wave); c.rise = 0.5 + i * 0.2; W.alive[c.wv] = (W.alive[c.wv] || 0) + 1; }
  }
  if (k === 'wuPriest') {   // 中西合璧：你是道长/一休，吴神父来；你是神父，九叔来
    const pr = S.hero === 'priest', p = MAP.simu;
    W.men.push({ k: pr ? 'taoist' : 'wuPriest', x: p[0] + 40, y: D_TOWN_Y + 20, hx: p[0] + 40, hy: p[1] + 10, cd: 1, face: 1, walk: 0, helper: true });
    W.unionCd = 4; rumor([pr ? '九叔来了：「洋和尚，借你的十字架一用」' : '吴神父来了：「道长，我们联手吧！」', '中西合璧：每隔一阵，你的法器会沾上圣水/符力，伤害大增'], false);
  }
  if (k === 'waxHouse') { W.waxHouse = true; S.shake = 0.4; sfx('slam'); const p = MAP.lafang; for (let i = 0; i < 24; i++) S.parts.push({ x: p[0] + rnd(-20, 20), y: p[1] - rnd(0, 30), vx: rnd(-80, 80), vy: rnd(-120, -30), t: rnd(0.4, 0.9), c: i % 2 ? '#8a2a2a' : '#4a2a20' }); }
  if (k === 'shisj') {
    const g = MAP.gates[Math.floor(Math.random() * 3)], e = dMakeMob({ t: 'walker', skin: 'shisj', eh: 6, spd: 1.6 }, g, D_TOWN_Y + 10, true); if (!e) return;
    e.shisj = true; e.special = true; e.hp = e.max = e.max * dHpK(W.wave) * 0.8; e.wv = W.wave; e.dw = 1; W.alive[e.wv] = (W.alive[e.wv] || 0) + 1;
    S.texts.push({ x: e.x, y: e.y - 40, v: '石少坚溜进镇了！', t: 2, c: '#ff8a9a', big: true });
  }
  if (k === 'mushroom') W.mush = ['grave', 'tomb', 'church'].map(f => { const h = MAP.fields[f].home; return { x: h[0] + rnd(-30, 30), y: h[1] + 30 + rnd(-6, 6) }; });
  if (k === 'mirrors') W.mirrors = [[152, 1290], [480, 1290], [808, 1290]].map(([x, y]) => ({ x, y }));
}
function dPals(list, msg) {
  const W = S.dw, P = S.p; W.pals = W.pals || [];
  for (const k of list) if (!W.pals.some(q => q.k === k)) W.pals.push({ k, x: P.x + rnd(-20, 20), y: P.y, cd: 1, ok: true, life: null });
  if (msg) rumor([msg], false);
}
function dHelpers(e) {   // 皇族僵尸打到一半：四目道长和一休大师赶来（你是一休就只来四目）
  const W = S.dw, P = S.p; W.pals = W.pals || [];
  const ks = S.hero === 'monk' ? ['simu'] : ['simu', 'monk'];
  for (const k of ks) W.pals.push({ k, x: e.x + rnd(-40, 40), y: e.y + 30, cd: 0.5, ok: true, life: 30, strong: true });
  banner(S.hero === 'monk' ? '四目道长赶来助阵！' : '四目道长、一休大师赶来助阵！', 2.2); sfx('gong');
}

// ---------- BOSS ----------
function dSpawnBoss(key, x, y, lane) {
  const B = D_BOSSES[key], D = DIFF[S.diff], W = S.dw;
  const e = spawn(B.t, x, y, { elite: true, skin: B.skin, eliteHp: 6 }); if (!e) return null;
  e.hp = e.max = B.hp * D.hp; e.boss = key; e.bw = W.wave; e.special = true; e.bsc = B.sc; e.r = 9; e.leak = 0;
  e.bossCore = B.final ? 3 : 1; e.sumT = S.t + 6; e.xp = 40; e.nopois = true; e.kbk = 0.2;
  if (B.leaper) { e.leaper = true; e.leapCd = rnd(2, 3); }
  if (B.t === 'walker') e.spd *= 1.15;
  if (B.t === 'ghost') e.spd *= 0.75;
  if (B.dr) e.dr = B.dr;
  if (B.blood) e.affix = 'vamp';
  if (B.thunder) e.boltVuln = true;
  if (B.bolts) e.boltVuln = true;
  if (B.undying) e.onHurt = q => { if (q.hp <= 0 && !q.bombed) { q.hp = 1; if (S.t > (q.nodieT || 0)) { q.nodieT = S.t + 3; S.texts.push({ x: q.x, y: q.y - 60, v: '打不死！', t: 1, c: '#ff8a7a', big: true }); } } };
  if (B.call) e.callT = S.t + 7;
  if (B.tame) W.zunT = S.t + 8;
  e.dmg = Math.round(e.dmg * (B.final ? 1.5 : 1.2));
  W.boss = e; W.awFled = false;
  if (B.capture) dCapture(e);
  return e;
}
function dBossTick(e) {   // BOSS 的招式（开关在 defense_data.js 的 D_BOSSES）
  const B = D_BOSSES[e.boss]; if (!B || e.dead || e.rise > 0) return;
  const P = S.p, W = S.dw, d = Math.hypot(P.x - e.x, P.y - e.y), near = !P.down;
  if (S.t >= e.sumT) {   // 召唤
    e.sumT = S.t + (B.sumCd || (B.final ? 7 : 9));
    const n = (B.sumN || 2 + Math.floor(e.bw / 6)) + (S.diff === 'hard' ? 1 : 0);
    for (let i = 0; i < n; i++) {
      const a = i / n * 6.283, m = dMob(B.summon, e.x + Math.cos(a) * 18, e.y + Math.sin(a) * 12);
      if (m) { m.lane = e.lane; m.wp = e.wp; m.lo = rnd(-9, 9); m.wv = W.wave; m.dw = 1; m.rise = 0.6; m.xp *= 0.4; m.hp = m.max = m.max * dHpK(e.bw); W.alive[m.wv] = (W.alive[m.wv] || 0) + 1; }
    }
    S.texts.push({ x: e.x, y: e.y - 58, v: '召！', t: 1, c: '#ff7a6a', big: true }); sfx('roar');
    for (let i = 0; i < 14; i++) S.parts.push({ x: e.x + rnd(-14, 14), y: e.y - 4, vx: rnd(-60, 60), vy: rnd(-100, -30), t: rnd(0.4, 0.8), c: '#7a3a6a' });
  }
  const tick = (k, cd) => { e[k] = (e[k] ?? cd * 0.6) - DT; if (e[k] > 0) return false; e[k] = cd; return true; };
  const D = DIFF[S.diff], dmg = n => Math.round(n * D.dmg * (1 + e.bw / 20));
  if (B.helpers && !e.helped && e.hp < e.max * 0.6) { e.helped = true; dHelpers(e); }
  if (B.call && e.callT && S.t >= e.callT) { e.callT = 0; const n = dSpawnBoss(B.call, e.x + 30, e.y, e.lane); if (n) { n.wp = e.wp; n.wv = e.wv; n.dw = 1; n.rise = 1.2; W.alive[n.wv] = (W.alive[n.wv] || 0) + 1; rumor(D_BOSSES[B.call].say, true); sfx('boss'); } }
  if (B.bats && near && d < 220 && tick('batCd', 4.2)) {
    const a0 = Math.atan2(P.y - 10 - (e.y - 20), P.x - e.x); sfx('wisp');
    for (let i = -1; i <= 1; i++) { const a = a0 + i * 0.28; S.eshots.push({ k: 'bat', x: e.x, y: e.y - 20, vx: Math.cos(a) * 80, vy: Math.sin(a) * 80, life: 3, a, ph: 0, dmg: dmg(7) }); }
  }
  if (B.batShift) {
    if (e.batT > 0) { e.batT -= DT; if (e.batT <= 0) { e.spd = e.spd0; S.texts.push({ x: e.x, y: e.y - 50, v: '现形！', t: 0.8, c: '#ff8a9a' }); } }
    else if (tick('shiftCd', 9)) { e.batT = 1.4; e.spd0 = e.spd; e.spd *= 3.2; sfx('wisp'); S.texts.push({ x: e.x, y: e.y - 50, v: '化蝠！', t: 0.9, c: '#ff8a9a', big: true }); }
  }
  if (B.jiuju) {
    const demon = e.hp < e.max * 0.5;
    if (demon && !e.demon) { e.demon = true; e.skin = 'jiujuD'; e.spd *= 1.3; banner('女教主魔化了！', 2); sfx('roar'); S.shake = 0.3; }
    const k = demon ? 0.65 : 1;
    if (near && d < 200 && tick('mudCd', 6 * k)) {
      for (let i = 0; i < (demon ? 3 : 1); i++) S.areas.push({ k: 'poison', sha: true, x: P.x + rnd(-24, 24) * (i > 0), y: P.y + rnd(-14, 14) * (i > 0), r: 20, life: 5, tk: 0, seed: Math.random() * 1000 });
      S.texts.push({ x: P.x, y: P.y - 40, v: '黑泥！', t: 0.9, c: '#c08aff' });
    }
    if (near && d < 230 && tick('limeCd', 3.5 * k)) {
      const a0 = Math.atan2(P.y - 10 - (e.y - 18), P.x - e.x); sfx('throw');
      for (let i = -1; i <= 1; i++) { const a = a0 + i * 0.2; S.eshots.push({ k: 'lime', x: e.x, y: e.y - 18, vx: Math.cos(a) * 110, vy: Math.sin(a) * 110, life: 2.2, a, dmg: dmg(6) }); }
    }
    if (near && d < 280 && d > 70 && tick('blinkCd', 10 * k)) {
      for (let i = 0; i < 16; i++) S.parts.push({ x: e.x + rnd(-8, 8), y: e.y - rnd(0, 30), vx: rnd(-40, 40), vy: rnd(-60, 0), t: 0.5, c: '#c08aff' });
      const a = Math.random() * 6.283; for (let k2 = 0; k2 < 8; k2++) { const nx = P.x + Math.cos(a + k2) * 60, ny = P.y + Math.sin(a + k2) * 40; if (freeAt(nx, ny)) { e.x = nx; e.y = ny; break; } }
      S.texts.push({ x: e.x, y: e.y - 56, v: '隔空斗法！', t: 1, c: '#c08aff', big: true }); sfx('whoosh');
    }
    if (tick('nailCd', 18)) { W.nails = W.nails || []; W.nails.push({ x: e.x + rnd(-20, 20), y: e.y + 10, pull: 0, tk: 4 }); S.texts.push({ x: e.x, y: e.y - 60, v: '镇龙钉！', t: 1.2, c: '#c08aff', big: true }); }
  }
  if (B.charm && near && d < 170 && tick('charmCd', 10)) dDoCharm();
  if (B.blood && tick('poolCd', 1.6)) S.areas.push({ k: 'poison', sha: true, x: e.x, y: e.y + 2, r: 14, life: 6, tk: 0, seed: Math.random() * 1000 });
  if (B.pearl) {
    if (e.pearlT > 0) { e.pearlT -= DT; if (e.pearlT <= 0) e.dr = B.dr || 1; }
    else if (tick('pearlCd', 13)) { e.pearlT = 3; e.dr = 0.05; S.texts.push({ x: e.x, y: e.y - 60, v: '定东珠护体！', t: 1.4, c: '#ffe070', big: true }); sfx('bell'); }
  }
  if (B.curse && near && d < 210 && tick('curseCd', 8)) { P.slowT = Math.max(P.slowT || 0, 2.2); S.texts.push({ x: P.x, y: P.y - 44, v: '罗盘锁魂！', t: 1.2, c: '#7af0a0', big: true }); sfx('chain'); }
  if (B.revive && !e.revived && e.hp < e.max * 0.25) { e.revived = true; e.hp = e.max * 0.7; banner(B.n + '：逆天改命！', 2.2); sfx('gong'); S.shake = 0.3; for (let i = 0; i < 30; i++) S.parts.push({ x: e.x, y: e.y - 20, vx: rnd(-90, 90), vy: rnd(-120, 20), t: 0.7, c: '#7a4ac0' }); }
  if (B.immune && !(e.tameT > S.t)) { e.stun = 0; e.slow = 0; e.pslow = 0; e.cageT = 0; }
  if (B.stomp && near && d < 90 && tick('stompCd', 5)) {
    S.fx.push({ k: 'pulse', x: e.x, y: e.y, r: 10, R: 90, t: 0, c: '#ff4a3a' }); sfx('slam'); S.shake = 0.35;
    if (d < 75 && P.inv <= 0) hurtPlayer(dmg(16));
  }
  if (B.bolts && near && d < 260 && tick('boltCd', 3.6)) {   // 妖尸：落雷砸你
    for (let i = 0; i < 3; i++) dBolt(P.x + (i ? rnd(-40, 40) : 0), P.y + (i ? rnd(-26, 26) : 0), 24, dmg(10));
    S.texts.push({ x: e.x, y: e.y - 60, v: '雷来！', t: 0.8, c: '#bfe8ff', big: true });
  }
  if (B.thunder && near && d < 300 && tick('boltCd', 2.6)) {   // 石坚：掌心雷，劈到他自己也会反噬
    dBolt(P.x, P.y, 30, dmg(12)); dBolt(P.x + rnd(-50, 50), P.y + rnd(-30, 30), 30, dmg(12));
    if (!e.thunderTip) { e.thunderTip = true; showTip('站在石坚身边，等天雷落下前一刻跑开——雷会劈到他自己！', false, 5); }
  }
  if (B.undying && !W.bomb && e.hp < e.max * 0.35) dBombPlace(e);
}
function dDoCharm() { S.dw.charmT = 3; S.texts.push({ x: S.p.x, y: S.p.y - 46, v: '被迷住了！方向颠倒', t: 1.8, c: '#ffd090', big: true }); sfx('suck'); }
function dDR(e, tag) {   // 伤害倍率：dr 法器打折（雷火光照样疼）、怕火、刚出场打不动、中西合璧、落雷反噬
  if (tag === 'bolt') return 1;
  let k = 1;
  const fire = tag === 'light' || tag === 'burn';
  if (e.dr != null && e.dr !== 1) k *= fire && e.dr > 0.2 ? Math.min(1, e.dr * 1.8) : e.dr;
  if (e.fireWeak && fire) k *= 2;
  if (e.ice && S.t < e.ice) k *= 0.25;
  if (S.dw && S.dw.unionT > 0) k *= 1.5;
  return k;
}

// ---------- 落雷（妖尸、石坚）----------
function dBolt(x, y, r, dmg) { S.dw.bolts.push({ x, y, r, dmg, t: 0 }); }
function dBoltTick() {
  const W = S.dw, P = S.p;
  for (const b of W.bolts) {
    b.t += DT; if (b.t < 0.95 || b.done) continue;
    b.done = true; sfx('thunder'); S.flash = Math.max(S.flash, 0.04);
    for (let i = 0; i < 10; i++) S.parts.push({ x: b.x + rnd(-8, 8), y: b.y - rnd(0, 10), vx: rnd(-70, 70), vy: rnd(-90, -20), t: 0.4, c: '#bfe8ff' });
    if (!P.down && P.inv <= 0 && (P.x - b.x) ** 2 + ((P.y - b.y) * 1.3) ** 2 < b.r * b.r) hurtPlayer(b.dmg);
    for (const e of S.en) if (e.boltVuln && !e.dead && (e.x - b.x) ** 2 + ((e.y - b.y) * 1.3) ** 2 < (b.r + 8) ** 2) {
      hurt(e, e.max * 0.09, 0, b.x, b.y, 'bolt'); S.texts.push({ x: e.x, y: e.y - 64, v: '天雷反噬！', t: 1.2, c: '#bfe8ff', big: true });
    }
  }
  W.bolts = W.bolts.filter(b => b.t < 1.3);
}
// ---------- 炸药（千年僵尸王）----------
function dBombPlace(e) {
  const W = S.dw, L = D_LANES[e.lane ?? 1], t = L[Math.min(L.length - 2, (e.wp || 1) + 1)];
  let x = t[0], y = t[1];
  if (y < e.y) { x = e.x + rnd(-20, 20); y = e.y + 60; }
  W.bomb = { x, y, fuse: 0, moveT: 0, boss: e };
  banner('茅山宗师埋好了炸药！把千年僵尸王引过去！', 2.6); sfx('gong');
}
function dBombTick() {
  const W = S.dw, B = W.bomb; if (!B) return;
  const e = B.boss;
  if (!e || e.dead || !S.en.includes(e)) { W.bomb = null; return; }
  const d = Math.hypot(e.x - B.x, e.y - B.y);
  if (d < 40) B.fuse += DT; else { B.fuse = Math.max(0, B.fuse - DT); B.moveT += d > 220 ? DT : 0; }
  if (B.moveT > 10) { B.moveT = 0; B.x = e.x + rnd(-30, 30); B.y = e.y + 70; S.texts.push({ x: B.x, y: B.y - 30, v: '宗师把炸药挪过来了', t: 1.4, c: '#ffd090' }); }
  if (B.fuse >= 0.8) {
    W.bomb = null; e.bombed = true; S.shake = 0.8; S.flash = 0.2; sfx('slam'); sfx('boss');
    for (let i = 0; i < 4; i++) S.fx.push({ k: 'pulse', x: B.x, y: B.y, r: 8 + i * 6, R: 100 + i * 20, t: 0, c: i % 2 ? '#ff9a3a' : '#ffe070' });
    for (let i = 0; i < 60; i++) S.parts.push({ x: B.x + rnd(-10, 10), y: B.y - rnd(0, 20), vx: rnd(-160, 160), vy: rnd(-220, -40), t: rnd(0.5, 1.1), c: ['#ff9a3a', '#ffe070', '#3a3040'][i % 3] });
    for (const q of S.en) if (!q.dead && !q.god && (q.x - B.x) ** 2 + (q.y - B.y) ** 2 < 110 * 110) hurt(q, q === e ? q.max * 3 : q.max, 200, B.x, B.y, 'bolt');
    const P = S.p; if (!P.down && P.inv <= 0 && Math.hypot(P.x - B.x, P.y - B.y) < 60) hurtPlayer(25);
    rumor(['茅山宗师抱着炸药冲了上去……与千年僵尸王同归于尽'], true);
  }
}
// ---------- 文才护送 ----------
function dBaitTick() {
  const W = S.dw, B = W.bait; if (!B) return;
  B.hitT = Math.max(0, (B.hitT || 0) - DT);
  if (B.hp <= 0) {
    W.bait = null; banner('文才被鬼缠住了！秋生把他拖了回来', 2.4); sfx('scream');
    setTimeout(() => S && S.dw && dPals(['xiaofeng'], '女鬼王小凤念着文才、秋生放过她的情，来帮你了'), 2500); return;
  }
  const t = B.path[B.i]; if (!t) { dBaitDone(); return; }
  const dx = t[0] - B.x, dy = t[1] - B.y, l = Math.hypot(dx, dy);
  if (l < 4) B.i++; else { const sp = 24 * DT; B.x += dx / l * Math.min(l, sp); B.y += dy / l * Math.min(l, sp); B.walk = (B.walk || 0) + DT; B.face = dx < 0 ? -1 : 1; }
  if (Math.random() < DT * 2) sfx('pick');
}
function dBaitDone() {
  const W = S.dw, B = W.bait; W.bait = null;
  let n = 0;
  for (const e of S.en) if (!e.dead && !e.boss && !e.field && e.type === 'ghost' && e.dw) { e.gone = true; dMobGone(e); n++; for (let i = 0; i < 4; i++) S.parts.push({ x: e.x, y: e.y - 10, vx: rnd(-20, 20), vy: rnd(-90, -50), t: 0.8, c: '#bfe8ff', g: -40 }); }
  W.gold += 60; S.chests.push({ x: D_CORE[0] + 30, y: D_CORE[1] - 60, big: true, t: 0 });
  banner(`文才把 ${n} 只鬼引回阴间了！`, 2.4); sfx('ultcard');
  setTimeout(() => S && S.dw && dPals(['xiaofeng'], '文才、秋生一念之仁放过的女鬼王小凤，留在人间来帮你'), 2500);
}
// ---------- 镇龙钉（九菊一派）----------
function dNailTick() {
  const W = S.dw, P = S.p; if (!W.nails || !W.nails.length) return;
  for (const n of W.nails) {
    n.tk -= DT; if (n.tk <= 0) { n.tk = 5; dCoreHit(1, n); }
    const near = !P.down && (P.x - n.x) ** 2 + (P.y - n.y) ** 2 < 20 * 20;
    n.pull = near ? n.pull + DT : Math.max(0, n.pull - DT * 0.5);
    if (n.pull >= 1.5) { n.gone = true; W.gold += 20; S.texts.push({ x: n.x, y: n.y - 30, v: '拔掉镇龙钉！+20文', t: 1.4, c: '#7af0a0', big: true }); sfx('ultcard'); }
  }
  W.nails = W.nails.filter(n => !n.gone);
}
// ---------- 血蜡尸的蜡油 ----------
function dWaxTick() {
  const W = S.dw, P = S.p;
  for (const e of S.en) if (e.waxDrip && !e.dead && !(e.rise > 0)) { e.waxT = (e.waxT ?? rnd(0, 2)) - DT; if (e.waxT <= 0) { e.waxT = 3; W.wax.push({ x: e.x, y: e.y + 1, life: 5 }); } }
  for (const w of W.wax) { w.life -= DT; if (!P.down && (P.x - w.x) ** 2 + ((P.y - w.y) * 1.5) ** 2 < 11 * 11) P.slowT = Math.max(P.slowT || 0, 0.35); }
  W.wax = W.wax.filter(w => w.life > 0);
  if (W.wax.length > 60) W.wax.splice(0, W.wax.length - 60);
}
// ---------- 棺材菌、定东珠 ----------
function dPickTick() {
  const W = S.dw, P = S.p; if (P.down) return;
  for (const m of W.mush || []) if (!m.got && (P.x - m.x) ** 2 + (P.y - m.y) ** 2 < 14 * 14) {
    m.got = true; W.gold += 40; for (let i = 0; i < 3; i++) S.orbs.push({ x: m.x, y: m.y, v: 5, du: true }); sfx('pickbig');
    S.texts.push({ x: m.x, y: m.y - 30, v: '采到棺材菌 +40文', t: 1.4, c: '#ffe070', big: true });
  }
  if (W.mush) W.mush = W.mush.filter(m => !m.got);
  if (W.pearl && (P.x - W.pearl.x) ** 2 + (P.y - W.pearl.y) ** 2 < 16 * 16) {
    W.pearl = null; W.core = Math.min(100, W.core + 25); sfx('ultcard'); banner('定东珠送回龙脉：灵气 +25', 2.2);
  }
}
// ---------- 八卦镜反射日光（告鲁斯伯爵怕）----------
function dMirrorTick() {
  const W = S.dw; if (!W.mirrors) return;
  for (const e of S.en) {
    if (e.dead || !(D_BOSSES[e.boss] && D_BOSSES[e.boss].sunWeak)) continue;
    const inSun = W.mirrors.some(m => (e.x - m.x) ** 2 + ((e.y - m.y) * 1.2) ** 2 < 38 * 38);
    if (!inSun) continue;
    e.sunT = (e.sunT || 0) - DT; e.slow = S.t + 0.5;
    if (e.sunT <= 0) { e.sunT = 0.5; e.batT = 0; hurt(e, e.max * 0.025, 0, e.x, e.y, 'bolt'); S.texts.push({ x: e.x, y: e.y - 60, v: '被日光照到了！', t: 0.6, c: '#ffe070' }); for (let i = 0; i < 6; i++) S.parts.push({ x: e.x + rnd(-8, 8), y: e.y - rnd(0, 30), vx: rnd(-20, 20), vy: -40, t: 0.6, c: '#ffcf70', g: -30 }); }
  }
}
// ---------- 小尊（让玄魁乖乖站住）----------
function dZunTick() {
  const W = S.dw; if (!W.zunT || S.t < W.zunT) return;
  const K = S.en.find(e => e.boss && D_BOSSES[e.boss].tame && !e.dead);
  if (!K) { W.zun = null; W.zunT = 0; return; }
  if (!W.zun) { W.zun = { x: D_CORE[0], y: D_CORE[1] - 60, cd: 0 }; rumor(['小尊来了！玄魁最听他的话'], false); }
  const Z = W.zun, dx = K.x - Z.x, dy = K.y - Z.y, d = Math.hypot(dx, dy);
  Z.cd -= DT;
  if (d > 26) { Z.x += dx / d * 70 * DT; Z.y += dy / d * 70 * DT; Z.face = dx < 0 ? -1 : 1; }
  else if (Z.cd <= 0) { Z.cd = 14; K.tameT = S.t + 4; K.stun = 4; S.texts.push({ x: Z.x, y: Z.y - 30, v: '小尊：不许咬人！', t: 2, c: '#ffffff', big: true }); S.texts.push({ x: K.x, y: K.y - 60, v: '玄魁乖乖站住了', t: 2, c: '#ffe070', big: true }); sfx('bell'); }
}
// ---------- 中西合璧 ----------
function dUnionTick() {
  const W = S.dw; if (W.unionCd == null) return;
  if (W.unionT > 0) W.unionT -= DT;
  W.unionCd -= DT;
  if (W.unionCd <= 0) { W.unionCd = 18; W.unionT = 6; banner('中西合璧！', 1.4); sfx('ult'); S.texts.push({ x: S.p.x, y: S.p.y - 50, v: S.hero === 'priest' ? '符力加身 · 伤害 ×1.5' : '圣水加身 · 伤害 ×1.5', t: 1.6, c: '#ffe070', big: true }); }
}

// ---------- 友军：大宝小宝、王小凤、小尊、四目、一休 ----------
const D_PAL = { dabao: { dmg: 1.4, kb: 60, cd: 1.2 }, xiaobao: { dmg: 0.8, kb: 10, cd: 0.8 }, xiaofeng: { dmg: 1.0, kb: 20, cd: 0.9, slow: 1 }, simu: { dmg: 2.5, kb: 40, cd: 0.7 }, monk: { dmg: 2.5, kb: 80, cd: 0.8 } };
function dPalTick() {
  const W = S.dw, P = S.p; if (!W.pals) return;
  W.pals.forEach((a, i) => {
    if (a.life != null) { a.life -= DT; if (a.life <= 0) { a.gone = true; return; } }
    if (!a.ok) return;
    const C = D_PAL[a.k] || D_PAL.xiaobao, side = i % 2 ? 1 : -1, ring = 22 + Math.floor(i / 2) * 14;
    const tx = P.down ? D_CORE[0] + side * ring : P.x + side * ring, ty = (P.down ? D_CORE[1] - 50 : P.y) - 4 + Math.sin(S.t * 3 + i) * 3;
    a.x += (tx - a.x) * Math.min(1, DT * 4); a.y += (ty - a.y) * Math.min(1, DT * 4);
    a.cd -= DT; if (a.cd > 0) return;
    let tg = null, bd = (a.strong ? 130 : 80) ** 2;
    for (const e of S.en) { if (e.dead || e.rise > 0 || e.god || e.dabao || e.batT > 0) continue; const d = (e.x - a.x) ** 2 + (e.y - a.y) ** 2; if (d < bd) { bd = d; tg = e; } }
    if (!tg) { a.cd = 0.3; return; }
    a.cd = C.cd; a.hitT = 0.15; a.tx = tg.x; a.ty = tg.y - 10; a.face = tg.x < a.x ? -1 : 1;
    hurt(tg, (6 + 1.6 * W.wave) * C.dmg, C.kb, a.x, a.y);
    if (C.slow) tg.slow = S.t + 1.2;
  });
  W.pals = W.pals.filter(a => !a.gone);
}

// ---------- 进了镇的游魂、女鬼会远远朝龙脉吐阴火 ----------
function dWispTick() {
  const W = S.dw, cx = D_CORE[0], cy = D_CORE[1] - 30;
  for (const e of S.en) {
    if (e.dead || e.rise > 0 || e.type !== 'ghost' || e.god || e.field || e.boss || e.dabao || e.noWisp || e.y < D_TOWN_Y) continue;
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
  const g = e.boss ? 120 + e.bw * 6 : e.field ? 45 + 6 * W.wave : e.elite ? 8 : e.type === 'ghost' ? 1 : 2;
  W.gold += g; W.goldT = 0.4;
  if (g >= 5) { S.texts.push({ x: e.x, y: e.y - 44, v: '+' + g + '文', t: 1.2, c: '#ffd040', big: g >= 40 }); sfx('coin'); }
  const B = e.boss && D_BOSSES[e.boss];
  if (B && B.next) {   // 死了变成下一个 BOSS（王婆→鬼王，尸王→邪神）
    const NB = D_BOSSES[B.next];
    banner(`${B.n} 倒下了……`, 1.6); rumor(NB.say, true);
    W.alive[e.wv] = (W.alive[e.wv] || 0) + 1;
    setTimeout(() => { if (!S || !S.dw || S.dw.over) return; S.dw.alive[e.wv] = Math.max(0, (S.dw.alive[e.wv] || 0) - 1); const n = dSpawnBoss(B.next, e.x, e.y, e.lane); if (n) { n.wp = e.wp; n.wv = e.wv; n.dw = 1; n.rise = 1; S.dw.alive[n.wv] = (S.dw.alive[n.wv] || 0) + 1; sfx('boss'); S.shake = 0.4; } }, 900);
    return;
  }
  if (B) {
    if (e.boss === 'wangpoG' && W.pals) { const a = W.pals.find(q => q.k === 'dabao'); if (a && !a.ok) { a.ok = true; S.en.forEach(q => { if (q.dabao) q.gone = true; }); rumor(['王婆一死，大宝身上的法也解了，他又回来帮你了'], false); } }
    if (B.dropPearl) { W.pearl = { x: e.x, y: e.y }; rumor(['慈禧口中的定东珠掉出来了！捡起来，送回龙脉'], false); }
    if (B.undying) W.bomb = null;
    S.chests.push({ x: e.x, y: e.y, big: true, t: 0 }); S.chests.push({ x: e.x + 18, y: e.y + 6, big: false, t: 0 });
    banner(`${B.n} 伏诛！`, 2.6); S.shake = 0.4; sfx('boss');
    for (let i = 0; i < 6; i++) S.orbs.push({ x: e.x + rnd(-12, 12), y: e.y + rnd(-8, 8), v: 5, du: true });
    if (B.final) W.bossDead = true;
  }
  if (e.tulong) { W.gold += 60; S.texts.push({ x: e.x, y: e.y - 56, v: '缴获龙脉镇物 +60文', t: 1.8, c: '#ffe070', big: true }); rumor(['屠龙倒了，运尸队散了'], false); }
  if (e.shisj) {   // 石少坚：尸体被镇上的狗撕烂
    rumor(['石少坚倒下了……镇上的狗冲出来，把他的尸体撕烂了'], true);
    for (let i = 0; i < 3; i++) { const d = dMob('madDog', e.x + rnd(-20, 20), e.y + rnd(-10, 10)); if (d) { d.wv = W.wave; d.dw = 1; d.rise = 0.4; d.hp = d.max = d.max * dHpK(W.wave); W.alive[d.wv] = (W.alive[d.wv] || 0) + 1; } }
  }
  if (e.elite && e.dw && !e.boss && Math.random() < 0.2) S.chests.push({ x: e.x, y: e.y, big: false, t: 0 });
  if (e.field) {
    const F = W.field[e.field]; F.e = null; F.back = W.wave + 3; F.kills++;
    S.chests.push({ x: e.x, y: e.y, big: true, t: 0 });
    banner(`斩了${D_FIELD[e.field].n}！`, 2); sfx('ultcard');
  }
}
// ---------- 野外 BOSS ----------
function dFieldTick() {
  const W = S.dw, P = S.p;
  for (const k in W.field) {
    const F = W.field[k];
    if (F.e && (F.e.dead || !S.en.includes(F.e))) F.e = null;
    if (F.e) {
      if (F.e.fcharm && !P.down && Math.hypot(P.x - F.e.x, P.y - F.e.y) < 150) { F.e.charmCd = (F.e.charmCd ?? 3) - DT; if (F.e.charmCd <= 0) { F.e.charmCd = 10; dDoCharm(); } }
      continue;
    }
    if (W.wave < F.back) continue;
    const H = MAP.fields[k].home, e = dMakeMob(D_FIELD[k], H[0], H[1], true); if (!e) continue;
    e.hp = e.max = (200 + 90 * Math.max(1, W.wave)) * DIFF[S.diff].hp * (1 + 0.25 * F.kills); e.field = k; e.home = H; e.special = true; e.rise = 1.2; e.xp = 12;
    e.dmg = Math.round(e.dmg * 1.1); if (e.skin === 'wolf') e.spd *= 1.2;
    F.e = e; F.back = 1e9;
    if (F.kills) S.texts.push({ x: H[0], y: H[1] - 50, v: D_FIELD[k].n + '又回来了', t: 2, c: '#ff8a6a', big: true });
  }
}
// ---------- 守卫：阿威队长、保安队、四目、吴神父 ----------
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
    if (m.pos > 0) {   // 被马贼附身：朝你开枪；走过去一巴掌拍醒
      m.pos -= DT; const P = S.p, dp = Math.hypot(P.x - m.x, P.y - m.y);
      if (!P.down && dp < 24) { m.pos = 0; S.texts.push({ x: m.x, y: m.y - 44, v: '醒醒！', t: 1.2, c: '#ffe070', big: true }); sfx('hit'); for (let i = 0; i < 12; i++) S.parts.push({ x: m.x, y: m.y - 16, vx: rnd(-50, 50), vy: rnd(-90, -20), t: 0.6, c: '#7af0d0' }); continue; }
      if (m.pos <= 0) { S.texts.push({ x: m.x, y: m.y - 40, v: '我……刚才怎么了？', t: 1.6, c: '#ffffff' }); continue; }
      m.cd -= DT; if (m.cd > 0 || P.down || dp > 140) continue;
      m.cd = 1.4; m.face = P.x < m.x ? -1 : 1; sfx('gun');
      m.tr = { x1: m.x + m.face * 12, y1: m.y - 14, x2: P.x, y2: P.y - 10 }; m.trT = 0.07;
      if (P.inv <= 0) { S.hitFrom = m; hurtPlayer(Math.round((5 + 0.6 * W.wave) * DIFF[S.diff].dmg)); S.hitFrom = null; }
      continue;
    }
    m.cd -= DT; if (m.cd > 0) continue;
    const thrower = m.k === 'simu' || m.helper, R = thrower ? 150 : 135;
    let tg = null, bd = R * R;
    for (const e of S.en) { if (e.dead || e.rise > 0 || e.god || e.batT > 0 || e.dabao) continue; const d = (e.x - m.x) ** 2 + (e.y - m.y) ** 2; if (d < bd) { bd = d; tg = e; } }
    if (!tg) { m.cd = 0.2; continue; }
    m.face = tg.x < m.x ? -1 : 1;
    const base = (7 + 2 * W.wave) * mul;
    if (thrower) {
      m.cd = 1.0; const a = Math.atan2(tg.y - 10 - (m.y - 14), tg.x - m.x); sfx('throw');
      S.shots.push({ k: 'fu', x: m.x, y: m.y - 14, vx: Math.cos(a) * 170, vy: Math.sin(a) * 170, life: 1.2, dmg: base * 1.3, pierce: 2, chance: 0.35, spin: 0, hit: new Set() });
    } else {
      m.cd = m.k === 'cap' ? 0.9 : 1.15; sfx('gun');
      m.tr = { x1: m.x + m.face * 12, y1: m.y - (m.k === 'cap' ? 17 : 14), x2: tg.x, y2: tg.y - 10 }; m.trT = 0.07;
      hurt(tg, base * (m.k === 'cap' ? 1.2 : 1), 25, m.x, m.y);
    }
  }
}
function dSimuJoin() {}

// ---------- 每帧：原游戏 update() 里调用的 updateEvents ----------
function updateEvents() {
  const W = S.dw, P = S.p;
  updateRumor();
  if (S.godNext && S.t >= S.godNext.t) { const k = S.godNext.k; S.godNext = null; spawnGod(k, Math.random() * 6.283); }
  updateGodFx();
  dDownTick();
  if (W.over) return;
  if (W.wave < D_N && S.t >= W.nextT) dStartWave(W.wave + 1);
  while (W.q.length && W.q[0].t <= S.t) dSpawnOne(W.q.shift());
  W.callable = W.wave >= 1 && W.wave < D_N && !W.q.length && S.t > W.spawnEnd && W.nextT - S.t > 3 && !W.bait;
  for (let w = W.cleared + 1; w <= W.wave; w++) {   // 一波清干净：奖励
    if (W.q.some(q => q.wv === w) || (W.alive[w] || 0) > 0) break;
    W.cleared = w; const bonus = 15 + 4 * w; W.gold += bonus; W.goldT = 0.6;
    if (w < D_N) { rumor([`第${dNum(w)}波守住了！赏钱 ${bonus} 文` + (P.y >= D_TOWN_Y ? '' : '（回镇里可以去杂货铺买东西）')], false); sfx('coin'); }
    if (D_WAVES[w - 1].event === 'waxHouse' || [].concat(D_WAVES[w - 1].event || []).includes('waxHouse')) W.waxHouse = false;
  }
  for (const e of S.en) if (e.boss && !e.dead) dBossTick(e);
  dWispTick(); dFieldTick(); dGuardTick(); dBellTick(); dPalTick();
  dBaitTick(); dNailTick(); dWaxTick(); dPickTick(); dMirrorTick(); dZunTick(); dUnionTick(); dBoltTick(); dBombTick();
  if (W.charmT > 0) W.charmT -= DT;
  for (const e of S.en) if (e.you && !e.dead && !(e.rise > 0)) {   // 游尸：隔几秒闪到别处
    e.blinkT = (e.blinkT ?? rnd(3, 6)) - DT;
    if (e.blinkT <= 0) {
      e.blinkT = rnd(4, 7);
      const ox = e.x, oy = e.y, a = rnd(0.3, 2.8);
      for (let k = 0; k < 8; k++) { const nx = e.x + Math.cos(a + k * 0.7) * rnd(50, 90), ny = e.y + Math.abs(Math.sin(a + k * 0.7)) * rnd(30, 70); if (nx > 30 && nx < WORLD.w - 30 && freeAt(nx, ny)) { e.x = nx; e.y = ny; break; } }
      for (const [x, y] of [[ox, oy], [e.x, e.y]]) for (let i = 0; i < 10; i++) S.parts.push({ x: x + rnd(-6, 6), y: y - rnd(0, 26), vx: rnd(-30, 30), vy: rnd(-50, -10), t: 0.5, c: '#8a8aa0', g: -20 });
    }
  }
  for (const e of S.en) if (e.thug && !e.dead && !(e.rise > 0) && !P.down) {   // 浪人：突然冲过来
    e.dashCd = (e.dashCd ?? rnd(1, 3)) - DT; const dx = P.x - e.x, dy = P.y - e.y, dd = Math.hypot(dx, dy) || 1;
    if (e.dashCd <= 0 && dd < 110) { e.dashCd = rnd(2.4, 3.6); e.kx += dx / dd * 260; e.ky += dy / dd * 260; S.texts.push({ x: e.x, y: e.y - 40, v: '喝！', t: 0.6, c: '#c08aff' }); sfx('whoosh'); }
  }
  for (const o of S.orbs) if ((o.age || 0) >= 2 && !P.down) o.pull = true;   // 阴德散在各路，过两秒自己飞回来
  W.coreFx = Math.max(0, (W.coreFx || 0) - DT); W.goldT = Math.max(0, (W.goldT || 0) - DT);
  if (W.wave >= D_N && W.bossDead && !W.q.length && !S.en.some(e => !e.dead && e.dw)) dWin();
}
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
function dGuardsInit() {
  const W = S.dw; W.men = [];
  MAP.guards.forEach((p, i) => W.men.push({ k: i ? 'sold' : 'cap', x: p[0], y: p[1], hx: p[0], hy: p[1], cd: rnd(0.2, 1), face: 1 }));
}
function dAddGuard() { const W = S.dw, p = MAP.guardsX[W.buy.guard - 1]; if (p) W.men.push({ k: 'sold', x: p[0], y: p[1] + 30, hx: p[0], hy: p[1], cd: 1, face: 1, walk: 0 }); }
function dBellTick() {
  const W = S.dw, lv = W.buy.bell; if (!lv) return;
  W.bellT = (W.bellT ?? 2) - DT; if (W.bellT > 0) return;
  W.bellT = [0, 4, 3.5, 3][lv];
  const R = [0, 80, 100, 120][lv], dmg = (18 + 3 * W.wave) * [0, 1, 1.4, 2][lv], cy = D_CORE[1] - 10;
  S.fx.push({ k: 'pulse', x: D_CORE[0], y: cy, r: 8, R, t: 0, c: '#8af0b0' }); sfx('bell');
  for (const e of S.en) if (!e.dead && !e.god && (e.x - D_CORE[0]) ** 2 + ((e.y - cy) / 0.75) ** 2 < R * R) hurt(e, dmg, e.boss ? 40 : 160, D_CORE[0], cy, 'light');
}
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
function dCharm() { return S && S.dw && S.dw.charmT > 0; }
function dCapture(boss) {   // 王婆抓走大宝，大宝变成敌人，专打穿道袍的人
  const W = S.dw, a = W.pals && W.pals.find(q => q.k === 'dabao' && q.ok); if (!a) return;
  a.ok = false;
  const e = spawn('ghost', boss.x + 20, boss.y, { skin: 'dabao' }); if (!e) return;
  e.dabao = true; e.hp = e.max = 300 * (1 + W.wave / 10); e.spd = 46; e.dmg = Math.round(10 * DIFF[S.diff].dmg); e.special = true; e.xp = 0;
  e.onHurt = q => { if (q.hp <= 0) { q.hp = 1; q.gone = true; a.ok = true; a.x = q.x; a.y = q.y; S.texts.push({ x: q.x, y: q.y - 40, v: '大宝醒了！', t: 1.8, c: '#7ef0a0', big: true }); sfx('ultcard'); } };
}
function dWin() {
  const W = S.dw; if (W.over) return; W.over = true; W.cleared = D_N; W.win = true;
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
    dw: { wisps: [], pals: null, charmT: 0, wave: 0, cleared: 0, nextT: D_TUNE.firstWave, q: [], bolts: [], wax: [], nails: null, bait: null, mush: null, pearl: null, mirrors: null, zun: null, bomb: null, unionT: 0, unionCd: null, alive: {}, core: 100, gold: 40, deaths: 0, buy: { core: 0, guard: 0, gun: 0, bell: 0, lv: 0, heal: 0 }, men: [], field: {}, spawnEnd: 0, boss: null },
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
    const key = (m.k === 'cap' ? (m.flee > 0 ? 'capN' : 'cap') : m.k) + (m.pos > 0 ? 'P' : ''), im = m.face < 0 ? flipped(key) : IMG[key];
    if (!im || !im.width) return;
    g.fillStyle = 'rgba(14,8,24,.45)'; g.beginPath(); g.ellipse(m.x, m.y, 7, 2, 0, 0, 7); g.fill();
    g.drawImage(im, Math.round(m.x - im.width / 2), Math.round(m.y - im.height + 2 - Math.abs(Math.sin((m.walk || 0) * 10)) * 1.2));
    if (m.trT > 0 && m.tr) { g.strokeStyle = '#fff6c0'; g.lineWidth = 1; g.beginPath(); g.moveTo(m.tr.x1, m.tr.y1); g.lineTo(m.tr.x2, m.tr.y2); g.stroke(); px(m.tr.x1 - 1, m.tr.y1 - 1, 3, 3, '#ffd040'); }
  } });
  if (W.pals) for (const q of W.pals) if (q.ok) list.push({ y: q.y + 0.4, f: () => {
    const im = (q.face || 1) < 0 ? flipped(q.k) : IMG[q.k]; if (!im || !im.width) return;
    g.globalAlpha = 0.85; g.drawImage(im, Math.round(q.x - im.width / 2), Math.round(q.y - im.height - 4)); g.globalAlpha = 1;
    if (q.hitT > 0) { q.hitT -= DT; g.strokeStyle = '#bff0ff'; g.lineWidth = 1; g.beginPath(); g.moveTo(q.x, q.y - 14); g.lineTo(q.tx, q.ty); g.stroke(); }
  } });
  for (const e of S.en) if (e.pearlT > 0 && !e.dead) list.push({ y: e.y + 0.8, f: () => { g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.25 + 0.1 * Math.sin(S.t * 12); g.fillStyle = '#ffd860'; g.beginPath(); g.ellipse(e.x, e.y - 30, 30, 40, 0, 0, 7); g.fill(); g.restore(); } });
  for (const e of S.en) if (e.ice > S.t && !e.dead) list.push({ y: e.y + 0.8, f: () => { g.globalAlpha = 0.35; g.fillStyle = '#c8f0ff'; g.fillRect(Math.round(e.x - 8), Math.round(e.y - 34), 16, 34); g.globalAlpha = 1; } });
  if (MAP.watch) list.push({ y: MAP.watch[1], f: () => { const im = IMG.watch; if (im && im.width) g.drawImage(im, Math.round(MAP.watch[0] - im.width / 2), Math.round(MAP.watch[1] - im.height + 2)); } });
  if (MAP.shop) list.push({ y: MAP.shop[1], f: () => {
    const im = IMG.villager, [x, y] = MAP.shop; if (im && im.width) g.drawImage(im, Math.round(x - im.width / 2), Math.round(y - im.height + 2));
    if (dInTown() && Math.floor(S.t * 2) % 2) { g.font = 'bold 8px monospace'; g.textAlign = 'center'; g.fillStyle = '#1a0e1e'; g.fillText('杂货铺', x + 1, y - 33); g.fillStyle = '#ffe070'; g.fillText('杂货铺', x, y - 34); }
  } });
  for (const e of S.en) if ((e.boss || e.field) && !e.dead && !(e.rise > 0)) list.push({ y: e.y + 0.7, f: () => {
    const im0 = IMG[e.skin], h = im0 ? im0.height * (e.bsc || 1.35) : 40, y = Math.round(e.y - h - 6), w = e.boss ? 40 : 28;
    px(e.x - w / 2 - 1, y - 1, w + 2, 4, '#1a0e1e'); px(e.x - w / 2, y, w * Math.max(0, e.hp / e.max), 2, e.boss ? '#ff4a3a' : '#ff9a3a');
    const nm = e.boss ? D_BOSS[e.boss].n : D_FIELD[e.field].n;
    g.font = 'bold 8px monospace'; g.textAlign = 'center'; g.fillStyle = '#1a0e1e'; g.fillText(nm, e.x + 1, y - 2); g.fillStyle = e.boss ? '#ff8a7a' : '#ffd090'; g.fillText(nm, e.x, y - 3);
  } });

  // ---------- 剧情道具：文才、镇龙钉、蜡油、棺材菌、定东珠、八卦镜、小尊、落雷、炸药 ----------
  const spr2 = (key, x, y, face, a) => { const im = (face || 1) < 0 ? flipped(key) : IMG[key]; if (!im || !im.width) return; if (a != null) g.globalAlpha = a; g.drawImage(im, Math.round(x - im.width / 2), Math.round(y - im.height + 2)); g.globalAlpha = 1; };
  const lbl = (s, x, y, c) => { g.font = 'bold 8px monospace'; g.textAlign = 'center'; g.fillStyle = '#1a0e1e'; g.fillText(s, x + 1, y + 1); g.fillStyle = c; g.fillText(s, x, y); };
  for (const w of W.wax) list.push({ y: -99997, f: () => { g.globalAlpha = Math.min(1, w.life) * 0.8; g.fillStyle = '#7a1a1a'; g.beginPath(); g.ellipse(w.x, w.y, 9, 4, 0, 0, 7); g.fill(); g.fillStyle = '#b04030'; g.beginPath(); g.ellipse(w.x - 1, w.y - 1, 5, 2, 0, 0, 7); g.fill(); g.globalAlpha = 1; } });
  if (W.mirrors) for (const m of W.mirrors) list.push({ y: -99996, f: () => {
    g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.18 + 0.06 * Math.sin(S.t * 4); g.fillStyle = '#ffe890'; g.beginPath(); g.ellipse(m.x, m.y, 38, 32, 0, 0, 7); g.fill(); g.restore();
    px(m.x - 4, m.y - 30, 8, 8, '#1a0e1e'); px(m.x - 3, m.y - 29, 6, 6, '#ffe070'); px(m.x - 1, m.y - 27, 2, 2, '#ffffff'); px(m.x, m.y - 22, 1, 22, '#4a3a2a');
    if (S.t < W.waveT + 12) lbl('八卦镜', m.x, m.y - 34, '#ffe070');
  } });
  if (W.nails) for (const n of W.nails) list.push({ y: n.y, f: () => {
    px(n.x - 1, n.y - 22, 3, 22, '#1a0e1e'); px(n.x, n.y - 21, 1, 20, '#c08aff'); px(n.x - 4, n.y - 24, 9, 3, '#1a0e1e'); px(n.x - 3, n.y - 23, 7, 1, '#e0c8ff');
    g.globalAlpha = 0.3 + 0.2 * Math.sin(S.t * 8); g.fillStyle = '#9a4ae0'; g.beginPath(); g.ellipse(n.x, n.y, 14, 5, 0, 0, 7); g.fill(); g.globalAlpha = 1;
    lbl('镇龙钉', n.x, n.y - 28, '#d8a8ff');
    if (n.pull > 0) { px(n.x - 11, n.y + 4, 22, 3, '#1a0e1e'); px(n.x - 10, n.y + 5, 20 * Math.min(1, n.pull / 1.5), 1, '#7af0a0'); }
  } });
  if (W.mush) for (const m of W.mush) list.push({ y: m.y, f: () => { px(m.x - 1, m.y - 5, 2, 5, '#e8e0c8'); px(m.x - 4, m.y - 8, 8, 3, '#1a0e1e'); px(m.x - 3, m.y - 8, 6, 2, Math.floor(S.t * 3) % 2 ? '#c8a060' : '#e8c080'); lbl('棺材菌', m.x, m.y - 12, '#ffe070'); } });
  if (W.pearl) { const p = W.pearl; list.push({ y: p.y, f: () => { g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.5; g.fillStyle = '#ffe890'; g.beginPath(); g.arc(p.x, p.y - 8, 8 + Math.sin(S.t * 6), 0, 7); g.fill(); g.restore(); px(p.x - 2, p.y - 10, 4, 4, '#ffffff'); lbl('定东珠', p.x, p.y - 20, '#ffe070'); } }); }
  if (W.bait) { const B = W.bait; list.push({ y: B.y, f: () => {
    spr2('wencai', B.x, B.y - Math.abs(Math.sin((B.walk || 0) * 10)) * 1.2, B.face, B.hitT > 0 ? 0.6 : null);
    px(B.x - 13, B.y - 40, 26, 4, '#1a0e1e'); px(B.x - 12, B.y - 39, 24 * B.hp / B.max, 2, '#7af0a0'); lbl('文才', B.x, B.y - 43, '#ffffff');
  } }); }
  if (W.zun) { const Z = W.zun; list.push({ y: Z.y, f: () => spr2('xiaozun', Z.x, Z.y, Z.face) }); }
  if (W.bomb) { const B = W.bomb; list.push({ y: B.y, f: () => {
    px(B.x - 6, B.y - 8, 12, 8, '#1a0e1e'); px(B.x - 5, B.y - 7, 10, 6, '#c8302c'); px(B.x - 5, B.y - 5, 10, 1, '#f0c020');
    if (Math.floor(S.t * 4) % 2) px(B.x + 3, B.y - 12, 2, 3, '#ffe070');
    g.globalAlpha = 0.25; g.strokeStyle = '#ff9a3a'; g.beginPath(); g.ellipse(B.x, B.y, 40, 26, 0, 0, 7); g.stroke(); g.globalAlpha = 1;
    lbl('炸药', B.x, B.y - 16, '#ffb070');
  } }); }
  for (const b of W.bolts) list.push({ y: 99991, f: () => {
    if (b.t < 0.95) { g.globalAlpha = 0.2 + 0.3 * (b.t / 0.95); g.strokeStyle = '#bfe8ff'; g.lineWidth = 1; g.beginPath(); g.ellipse(b.x, b.y, b.r, b.r / 1.3, 0, 0, 7); g.stroke(); g.fillStyle = '#bfe8ff'; g.globalAlpha *= 0.4; g.fill(); g.globalAlpha = 1; return; }
    g.globalAlpha = Math.max(0, 1 - (b.t - 0.95) / 0.35); g.strokeStyle = '#ffffff'; g.lineWidth = 2; g.beginPath(); let x = b.x, y = b.y - 200; g.moveTo(x, y); while (y < b.y) { x += rnd(-8, 8); y += 20; g.lineTo(x, Math.min(y, b.y)); } g.stroke(); g.globalAlpha = 1;
  } });
  if (W.unionT > 0) list.push({ y: S.p.y + 0.5, f: () => { g.save(); g.globalCompositeOperation = 'lighter'; g.globalAlpha = 0.25; g.fillStyle = '#ffe070'; g.beginPath(); g.ellipse(S.p.x, S.p.y - 14, 14, 20, 0, 0, 7); g.fill(); g.restore(); } });
  if (MAP.lafang && W.waxHouse) list.push({ y: -99995, f: () => { lbl('腊味坊出事了！', MAP.lafang[0], MAP.lafang[1] - 70, '#ff8a7a'); } });
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
  $('shichen').textContent = W.wave ? `第${W.wave}/${D_N}波` : '准备';
  const left = Math.max(0, W.nextT - S.t);
  $('till').textContent = W.charmT > 0 ? `方向颠倒 ${W.charmT.toFixed(1)} 秒` : P.down ? `调息中 ${Math.ceil(P.downT)} 秒` : W.wave >= D_N ? (W.over ? '' : '最后一战！') : `下一波 ${Math.floor(left / 60)}:${String(Math.floor(left % 60)).padStart(2, '0')}`;
  $('coreb').firstElementChild.style.transform = `scaleX(${W.core / 100})`;
  $('coreb').className = 'bar' + (W.core <= 25 ? ' low' : W.core <= 50 ? ' mid' : '');
  $('coreV').textContent = `龙脉 ${Math.ceil(W.core)}`;
  const bv = $('bossV'), bo = W.boss && !W.boss.dead ? W.boss : null; bv.hidden = !bo;
  if (bo) bv.textContent = `${D_BOSS[bo.boss].n} ${Math.ceil(bo.hp / bo.max * 100)}% · ${bo.y > D_TOWN_Y ? '已进镇！' : ['西路', '正路', '东路'][bo.lane] || ''}`;
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
  $('endP').textContent = (win ? `守住全部二十波！` : `守到第${dNum(Math.max(1, W.wave))}波，守住 ${W.cleared} 波。`) + `伏尸 ${S.kills} 具，修为 ${cn(S.lv)}重。（${DIFF[S.diff].name}）`;
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
  $('rankNote').textContent = (shared ? '' : '暂时连不上共享功德簿，以下是本机记录。 ') + (parts.length ? `你（${me}）：` + parts.join('，') : (me ? '你还没上榜，去守龙脉吧！' : '')) + '　☀ = 守住二十波　守N波 = 守住了几波';
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
  c.fillStyle = '#f0c020'; c.font = `22px ${F}`; c.fillText(S.win ? `${nm} 守住了二十波！` : `${nm} 守到了第${dNum(Math.max(1, W.wave))}波`, 180, 414);
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
