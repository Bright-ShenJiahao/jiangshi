// =====================================================================
// 《守卫任家镇的中心的龙脉》数据表 —— 改怪、改 BOSS、改每一波的剧情，只改这个文件
// 字段说明见 src/DEFENSE.md。民国背景；主线：各路妖邪都想夺、斩、吞任家镇底下这条中国龙脉。
// =====================================================================

// ---------- 小怪 ----------
// n 名字 | t 引擎类型：ghost 飘（无视地形）、walker 走、zombie 跳、jumper 跳尸（会扑）| skin 像素图（skins 随机一个）
// hp 血量倍率 | spd 速度倍率 | dmg 伤害倍率 | xp 经验倍率 | kbk 被击退的程度（1 正常，0 推不动）| r 体型
// 特性：leaper 会扑跳 | dr 法器伤害倍率（雷火光照样疼）| ice 出场后几秒几乎打不动 | blink 隔几秒闪到别处 | underground 从镇里地下钻出来
//       possess 去附身保安 | wax 走过留下蜡油（减速）| fireWeak 怕火（雷火光伤害翻倍）| noWisp 进镇不吐阴火 | leak 踏进龙脉扣多少（默认 2）
const D_MOBS = {
  ghost:    { n: '游魂', t: 'ghost' },
  ghostW:   { n: '白衣女鬼', t: 'ghost', skin: 'ghostW', hp: 1.8, xp: 1.5 },
  walk:     { n: '行尸', t: 'walker', skins: ['walker', 'walkF', 'walkS'] },
  zP:       { n: '紫僵', t: 'zombie', skin: 'zP', hp: 0.8, spd: 0.85 },
  zW:       { n: '白僵', t: 'zombie', skin: 'zW' },
  zG:       { n: '绿僵', t: 'zombie', skin: 'zG', spd: 1.2, leaper: 1 },
  maoZ:     { n: '毛僵', t: 'jumper', skin: 'jumperM', hp: 1.5, spd: 1.25, kbk: 0.5, xp: 1.4 },
  feiZ:     { n: '飞僵', t: 'ghost', skin: 'feiZ', hp: 4, dmg: 1.6, spd: 0.9, xp: 2, noWisp: 1 },
  youZ:     { n: '游尸', t: 'walker', skin: 'youZ', hp: 2.2, xp: 1.6, blink: 1 },
  fuZ:      { n: '伏尸', t: 'zombie', skin: 'fuZ', hp: 2.4, spd: 0.8, kbk: 0.3, xp: 1.8, underground: 1 },
  bugu:     { n: '不化骨', t: 'zombie', skin: 'bugu', hp: 3, dmg: 1.6, kbk: 0.15, dr: 0.4, leak: 6, xp: 3 },
  corpse:   { n: '赶尸', t: 'zombie', skin: 'corpse', hp: 1.3, xp: 1.3 },
  jump:     { n: '跳尸', t: 'jumper' },
  tanG:     { n: '谭家厉鬼', t: 'ghost', skin: 'tanG', hp: 2.4, spd: 0.9, dmg: 1.3, xp: 1.6 },
  bandit:   { n: '马贼鬼魂', t: 'walker', skins: ['banditA', 'banditB'], hp: 1.4, spd: 1.25, possess: 1 },
  jtZ:      { n: '降头尸', t: 'walker', skin: 'jtZ', hp: 2, dmg: 1.4, spd: 0.9, kbk: 0.25, ice: 4, xp: 1.5 },
  wolf:     { n: '狼人', church: 'wolf' },
  vampM:    { n: '吸血鬼仆从', church: 'mob' },
  waxZ:     { n: '血蜡尸', t: 'zombie', skin: 'waxZ', hp: 2.2, spd: 0.85, fireWeak: 1, wax: 1, xp: 1.6 },
  qingbing: { n: '清兵僵尸', t: 'zombie', skin: 'qingbing', hp: 1.4, xp: 1.3 },
  tongZ:    { n: '僵尸童', t: 'zombie', skin: 'tongZ', spd: 1.5, hp: 0.8, r: 5 },
  feitou:   { n: '飞头降', t: 'ghost', skin: 'feitou', hp: 1.2, spd: 1.5, r: 5 },
  madDog:   { n: '疯狗', t: 'walker', skin: 'madDog', spd: 1.8, hp: 0.9, dmg: 0.8 },
};

// ---------- 精英（带一个随机词缀；eh = 精英血量倍数；dash 会突然冲过来）----------
const D_ELITES = {
  red:   { n: '红衣厉鬼', t: 'ghost', skin: 'ghostR', eh: 15 },
  hairy: { n: '毛僵王', t: 'jumper', skin: 'jumperM', eh: 6 },
  oil:   { n: '油炸鬼', t: 'zombie', skin: 'oilG', eh: 5, dr: 0.6, kbk: 0.3 },
  ronin: { n: '东洋浪人', t: 'walker', skin: 'ronin', eh: 5, spd: 1.3, dmg: 1.5, kbk: 0.6, dash: 1 },
  bride: { n: '吸血鬼新娘', church: 'bride' },
  bugu:  { n: '不化骨', t: 'zombie', skin: 'bugu', eh: 5, dmg: 1.6, kbk: 0.1, dr: 0.4, leak: 8 },
};

// ---------- BOSS ----------
// hp 普通难度血量（困难 ×1.5）| sc 画面放大 | summon 召唤哪种小怪（'mix' 随机）| sumN 每次几只 | sumCd 几秒一次
// why 它为什么冲着龙脉来（出场时旁白）| say 出场旁白
// 招式开关：leaper 扑跳 | bats 放蝙蝠 | batShift 化蝠瞬移 | dr 法器伤害倍率 | fly 会飞 | immune 不怕定身减速
//   next 死后变成哪个 BOSS | capture 抓走大宝 | jiuju 黑泥石灰隔空斗法+魔化 | charm 迷惑（方向颠倒）| blood 吸血+血池
//   pearl 定东珠护体 | dropPearl 死后掉定东珠 | revive 逆天改命 | curse 罗盘锁魂 | call 出场后再叫一个 BOSS 来
//   sunWeak 怕八卦镜反射的日光 | tame 小尊来了会让它站住 | undying 打不死，要用炸药 | bolts 放雷 | thunder 石坚天雷（会反噬自己）
//   helpers 打到一半谁来助阵 | stomp 跺地 | final 最终 BOSS
const D_BOSSES = {
  renZ:    { n: '尸变任老爷', t: 'zombie', skin: 'renZ', hp: 600, sc: 1.9, summon: 'zP', leaper: 1,
             say: ['《僵尸先生》：任老爷被老太爷咬了一口……', '任老爷尸变了！直奔镇中心！'] },
  royal:   { n: '皇族僵尸', t: 'jumper', skin: 'royalZ', hp: 700, sc: 1.6, summon: 'corpse', dr: 0.7, helpers: 1,
             say: ['《僵尸叔叔》：千鹤道长护送金墨棺进京，路过任家镇', '一道雷劈开了棺木——皇族僵尸破棺而出！'] },
  wangpo:  { n: '马贼王婆', t: 'walker', skin: 'wangpo', hp: 1000, sc: 1.6, summon: 'bandit', dr: 0.5, next: 'wangpoG', capture: 1,
             say: ['《灵幻先生》：马贼帮的王婆刀枪不入，要拿龙脉养她的邪术', '她把大宝抓走了，施法让他专打穿道袍的人！'] },
  wangpoG: { n: '鬼王·王婆', t: 'ghost', skin: 'wangpoG', hp: 1000, sc: 1.6, summon: 'tanG', fly: 1,
             say: ['王婆掉进井里死了……', '死后化成了鬼王！'] },
  jiuju:   { n: '九菊女教主', t: 'walker', skin: 'jiuju', hp: 1200, sc: 1.55, summon: 'jtZ', jiuju: 1,
             say: ['九菊一派的女教主亲自来了：她要斩断中国龙脉！', '小心她的黑泥、石灰，还有隔空斗法！'] },
  oldPriest: { n: '吸血鬼老神父', t: 'walker', skin: 'oldPriestV', hp: 1800, sc: 1.6, summon: 'vampM', bats: 1,
             say: ['《驱魔道人》：修士在地窖里拔出了老神父身上的十字架……', '二十年前死去的老神父变成了吸血鬼！'] },
  qiannian: { n: '千年僵尸王', t: 'zombie', skin: 'qiannian', hp: 2600, sc: 1.5, summon: 'waxZ', leaper: 1, undying: 1,
             say: ['姜家腊味坊的地窖底下，封着一具千年僵尸王', '它要吸干龙脉！它打不死——茅山宗师已经去取炸药了'] },
  yaoshi:  { n: '妖尸·石少坚', t: 'walker', skin: 'yaoshi', hp: 3000, sc: 1.55, summon: 'madDog', bolts: 1,
             say: ['《僵尸至尊》：石坚用棺材菌补好了儿子的尸体……', '石少坚被邪术炼成了妖尸，浑身带着雷电！'] },
  cixi:    { n: '慈禧太后', t: 'zombie', skin: 'cixi', hp: 3600, sc: 1.5, summon: 'qingbing', pearl: 1, dropPearl: 1, sumN: 5, sumCd: 7,
             say: ['《僵尸道长》：盗墓贼黑玫瑰偷走了慈禧口中的定东珠', '慈禧复活了，要借龙脉复辟大清！'] },
  yangfy:  { n: '杨飞云', t: 'walker', skin: 'yangfy', hp: 3600, sc: 1.55, summon: 'tanG', revive: 1, curse: 1, call: 'gaolus',
             say: ['算命的杨飞云想夺龙脉的气运来逆天改命', '他还复活了西洋吸血鬼告鲁斯伯爵！'] },
  gaolus:  { n: '告鲁斯伯爵', t: 'walker', skin: 'vampire', hp: 2600, sc: 1.6, summon: 'vampM', bats: 1, batShift: 1, dr: 0.5, sunWeak: 1,
             say: ['告鲁斯伯爵：道家法术对他只有一半效果', '把他引到八卦镜反射的日光里！'] },
  xuemo:   { n: '罗平·血魔', t: 'walker', skin: 'xuemo', hp: 4200, sc: 1.6, summon: 'feitou', blood: 1,
             say: ['怨气与邪法，把罗平变成了血魔', '他打中你会吸血，走过的地方血流成池！'] },
  xuankui: { n: '僵尸王玄魁', t: 'ghost', skin: 'xuankui', hp: 4800, sc: 1.45, summon: 'tongZ', fly: 1, immune: 1, dr: 0.7, tame: 1,
             say: ['清朝亲王，僵尸之王玄魁：他要喝龙脉的血', '他会飞，不怕定身减速——等小尊来！'] },
  shijian: { n: '石坚', t: 'walker', skin: 'shijian', hp: 4400, sc: 1.6, summon: 'madDog', thunder: 1, dr: 0.2,
             say: ['《僵尸至尊》：九叔的大师兄石坚来报仇了，他要借龙脉练成雷法', '他几乎刀枪不入——让他的天雷劈到他自己身上！'] },
  king:    { n: '尸王·任老太爷', t: 'zombie', skin: 'king', hp: 5500, sc: 2.1, summon: 'zG', leaper: 1, next: 'xieshen',
             say: ['七七四十九天，蜻蜓点水穴里的老太爷……', '炼成尸王了！'] },
  xieshen: { n: '邪神降临', t: 'walker', skin: 'xieshen', hp: 8500, sc: 1.25, summon: 'mix', final: 1, stomp: 1, sumN: 6, sumCd: 7,
             say: ['尸王倒下的地方，天地变色……', '邪神真身降临，要把整条中国龙脉吞下去！守住它！'] },
};

// ---------- 20 波 ----------
// film 片名（显示在横幅上）| mobs 这一波的小怪和权重 | elites 这一波的精英（列几个出几个）| boss 这一波的 BOSS
// tier 尸变等级第一次出场的提示 | event 这一波开始时的剧情事件 | say 开场旁白 | long 波次更长（BOSS 波自动更长）
// 事件：wencai 护送文才 | pals 大宝小宝加入 | nails 九菊打镇龙钉 | tulong 屠龙运尸队 | wuPriest 吴神父来了（中西合璧）
//       waxHouse 姜家腊味坊爆发 | shisj 石少坚进镇 | mushroom 野外长棺材菌 | mirrors 架八卦镜
const D_WAVES = [
  /* 1 */ { film: '僵尸至尊', mobs: { ghost: 6, zP: 4, walk: 3 }, tier: '紫僵：刚起尸，血凝住了，皮肤发紫',
            say: ['文才、秋生偷用小茅山，犯了忌讳，鬼魂不散', '鬼门关开了！三路阴兵冲着镇中心的龙脉来了'] },
  /* 2 */ { film: '僵尸至尊', mobs: { ghost: 8, zP: 3, zW: 3 }, event: 'wencai', tier: '白僵：长出白毛，怕光怕火，走得慢',
            say: ['九叔和大师兄石坚想了个法子：用文才当诱饵，把鬼魂引回阴间'] },
  /* 3 */ { film: '僵尸先生', mobs: { zW: 3, zG: 3, walk: 3, ghost: 2 }, elites: ['red'], boss: 'renZ', tier: '绿僵：长出绿毛，会蓄力扑跳' },
  /* 4 */ { film: '僵尸叔叔', mobs: { corpse: 4, jump: 2, zG: 2, maoZ: 2 }, elites: ['hairy'], boss: 'royal', tier: '毛僵：浑身粗毛，动作快、皮更硬' },
  /* 5 */ { film: '灵幻先生', mobs: { tanG: 3, bandit: 3, ghost: 2, maoZ: 1 }, elites: ['oil'], event: 'pals',
            say: ['谭百万把房子建在坟头上，厉鬼一家出来作祟', '马贼的鬼魂会附身保安——走过去拍醒他！'] },
  /* 6 */ { film: '灵幻先生', mobs: { tanG: 2, bandit: 3, zG: 2 }, elites: ['oil', 'red'], boss: 'wangpo' },
  /* 7 */ { film: '九菊一派', mobs: { jtZ: 4, feiZ: 2, maoZ: 2 }, elites: ['ronin', 'ronin'], event: 'nails', tier: '飞僵：腾云驾雾，能飞过河、飞过城墙！',
            say: ['东洋九菊一派来了：他们要在地脉上打镇龙钉，斩断中国龙脉！', '看到镇龙钉就跑过去拔掉，不然龙脉一直漏灵气'] },
  /* 8 */ { film: '九菊一派', mobs: { jtZ: 3, feiZ: 2, zG: 2 }, elites: ['ronin', 'oil'], boss: 'jiuju' },
  /* 9 */ { film: '驱魔道人', mobs: { youZ: 2, corpse: 3, wolf: 2, vampM: 2 }, elites: ['bride'], event: 'tulong', tier: '游尸：四处游荡，来去无踪，会突然闪到别处',
            say: ['镇上的教堂封了二十年，洋神父要重开它', '九叔的师弟屠龙借赶尸偷运龙脉镇物——打掉领头的屠龙！'] },
  /* 10 */ { film: '驱魔道人', mobs: { wolf: 3, vampM: 3, youZ: 2 }, elites: ['bride', 'hairy'], event: 'wuPriest', boss: 'oldPriest' },
  /* 11 */ { film: '僵尸大时代', mobs: { waxZ: 5, youZ: 2, feiZ: 1 }, elites: ['hairy'], event: 'waxHouse',
            say: ['城里出事了！姜家腊味坊的门被撞开……', '一具具血蜡尸从作坊里冲出来，就在镇子里！血蜡尸怕火'] },
  /* 12 */ { film: '僵尸大时代', mobs: { waxZ: 3, fuZ: 2, feiZ: 2 }, elites: ['hairy', 'red'], boss: 'qiannian', tier: '伏尸：潜伏在地脉里，会直接从镇子里钻出来！' },
  /* 13 */ { film: '僵尸至尊', mobs: { madDog: 3, fuZ: 2, youZ: 2, tanG: 2 }, elites: ['red', 'oil'], event: ['shisj', 'mushroom'],
            say: ['石坚的儿子石少坚学了旁门左道，溜进镇里纠缠钱小姐', '野外的义庄、乱葬岗长出了棺材菌……石坚想要它'] },
  /* 14 */ { film: '僵尸至尊', mobs: { madDog: 3, fuZ: 2, feiZ: 2, zG: 2 }, elites: ['hairy', 'oil'], boss: 'yaoshi' },
  /* 15 */ { film: '僵尸道长', mobs: { qingbing: 5, tongZ: 2, fuZ: 1, bugu: 1 }, elites: ['bugu'], boss: 'cixi', tier: '不化骨：僵尸的最高境界，骨头硬如磐石，只怕雷火光' },
  /* 16 */ { film: '僵尸道长', mobs: { tanG: 2, vampM: 3, qingbing: 2, feiZ: 2 }, elites: ['bride', 'bugu'], event: 'mirrors', boss: 'yangfy' },
  /* 17 */ { film: '僵尸道长', mobs: { feitou: 4, tongZ: 3, youZ: 2 }, elites: ['red', 'bugu'], boss: 'xuemo',
            say: ['南洋降头术——飞降！只有一颗头在飞'] },
  /* 18 */ { film: '僵尸道长', mobs: { tongZ: 3, qingbing: 3, feiZ: 2, fuZ: 1 }, elites: ['bugu', 'hairy'], boss: 'xuankui' },
  /* 19 */ { film: '僵尸至尊', mobs: { madDog: 2, feiZ: 2, bugu: 1, jtZ: 2, waxZ: 2 }, elites: ['ronin', 'bugu', 'oil'], boss: 'shijian' },
  /* 20 */ { film: '终局', mobs: { zG: 2, maoZ: 2, feiZ: 2, youZ: 2, fuZ: 2, bugu: 1, qingbing: 2 }, elites: ['bugu', 'bugu', 'red', 'ronin'], boss: 'king',
            say: ['最后一战！鸡鸣之前，绝不能让龙脉断了'] },
];

// ---------- 野外 BOSS（打死掉大宝箱和铜钱，三波后复活，更强）----------
const D_FIELD = {
  tomb:   { n: '古墓毛僵', t: 'jumper', skin: 'jumperM', eh: 6 },
  church: { n: '教堂狼人', t: 'jumper', skin: 'wolf', eh: 6 },
  grave:  { n: '乱葬岗厉鬼', t: 'ghost', skin: 'ghostR', eh: 15 },
  yz:     { n: '大罗金仙', t: 'ghost', skin: 'moth', eh: 15, charm: 1 },
};

// ---------- 杂货铺 ----------
const D_ITEMS = [
  { k: 'heal', seal: '药', n: () => '金创药', d: () => '阳气回满', p: W => 30 },
  { k: 'core', seal: '脉', n: () => '修补龙脉', d: () => '龙脉灵气 +15（最多 100）', p: W => 50 + 15 * W.buy.core },
  { k: 'guard', seal: '兵', n: () => '招募保安队', d: () => '镇里多一名保安守着（最多再招 4 名）', p: W => 90 + 45 * W.buy.guard, max: 4 },
  { k: 'gun', seal: '枪', n: () => '洋枪洋炮', d: () => '镇上所有守卫伤害 +30%', p: W => Math.round(80 * Math.pow(1.6, W.buy.gun)), max: 5 },
  { k: 'bell', seal: '钟', n: () => '镇龙铜钟', d: W => ['龙脉每隔几秒震出一圈金光，击退并伤害周围的怪', '铜钟二级：范围更大、更疼', '铜钟三级：范围最大、伤害翻倍'][Math.min(2, W.buy.bell)], p: W => [150, 300, 500][W.buy.bell] || 0, max: 3 },
  { k: 'lv', seal: '法', n: () => (S.hero === 'monk' ? '少林秘籍' : S.hero === 'priest' ? '古卷圣典' : '茅山秘籍'), d: () => '修为立刻精进一重（三选一）', p: W => 110 + 40 * W.buy.lv },
];

// ---------- 数值 ----------
const D_TUNE = {
  waveGap: 34, bossGap: 50,           // 两波之间隔几秒（BOSS 波更长）
  spawnDur: 16, bossSpawnDur: 20,     // 一波的怪在几秒内刷完
  count: w => 10 + 4 * w,             // 一波大约多少只（BOSS 波 ×0.55，困难 ×1.25）
  effT: w => Math.min(600, (w - 1) * 31.5),     // 怪的成长（相当于原游戏第几秒）
  hpK: w => 1 + 0.15 * w + 0.009 * w * w,       // 每波额外的血量倍率
  firstWave: 14,                      // 开局几秒后第一波
};
