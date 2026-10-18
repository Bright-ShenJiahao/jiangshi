# 《守卫任家镇的中心的龙脉》修改指南

背景：民国。主线：守护中国龙脉——每一路妖邪都想夺、斩或吞任家镇底下的龙脉。共 20 波。

**改怪、改 BOSS、改剧情，基本只动 `defense_data.js`。** 每个怪/每个 BOSS/每一波都是一行（或两行），按名字搜就能找到。
改完运行 `python3 gen_defense.py` 重新打包。

想省 token 让 Claude 改，直接说「改哪个表、哪个键、哪个字段」，例如：
- 「`D_BOSSES.cixi.hp` 改成 5000」
- 「第 11 波 `say` 换成：……」
- 「`D_MOBS.waxZ` 加 `spd: 1.2`」
- 「第 15 波 `mobs` 里加 `feitou: 2`」

## 表在哪

| 表 | 是什么 | 一行的键 |
|---|---|---|
| `D_MOBS` | 小怪 | `ghost` `ghostW` `walk` `zP`紫僵 `zW`白僵 `zG`绿僵 `maoZ`毛僵 `feiZ`飞僵 `youZ`游尸 `fuZ`伏尸 `bugu`不化骨 `corpse`赶尸 `jump`跳尸 `tanG`谭家厉鬼 `bandit`马贼鬼魂 `jtZ`降头尸 `wolf`狼人 `vampM`吸血鬼仆从 `waxZ`血蜡尸 `qingbing`清兵僵尸 `tongZ`僵尸童 `feitou`飞头降 `madDog`疯狗 |
| `D_ELITES` | 精英（带词缀，掉宝箱） | `red`红衣厉鬼 `hairy`毛僵王 `oil`油炸鬼 `ronin`东洋浪人 `bride`吸血鬼新娘 `bugu`不化骨 |
| `D_BOSSES` | BOSS | 见下表 |
| `D_WAVES` | 第 1–20 波，数组下标 = 波数 − 1（每行前面有 `/* 波数 */`） | — |
| `D_FIELD` | 野外四个点的大怪 | `tomb` `church` `grave` `yz` |
| `D_ITEMS` | 杂货铺 | `heal` `core` `guard` `gun` `bell` `lv` |
| `D_TUNE` | 节奏和难度曲线 | 波间隔、刷怪数量、成长 |

## 小怪字段（`D_MOBS` / `D_ELITES` / `D_FIELD`）

| 字段 | 意思 |
|---|---|
| `n` | 名字 |
| `t` | 引擎类型：`ghost` 飘（穿墙过河）、`walker` 走、`zombie` 跳、`jumper` 跳尸（会扑） |
| `skin` / `skins` | 像素图（`skins` 随机一个）。新图在 `defense_sprites.py` 画，在 `gen_defense.py` 注册 |
| `church` | 用原游戏教堂的怪：`'wolf'` `'mob'` `'bride'` |
| `hp` `spd` `dmg` `xp` | 倍率 |
| `kbk` | 被击退程度（1 正常，0 推不动） |
| `r` | 体型 |
| `eh` | 精英的血量倍率 |
| `leaper` | 会扑跳 |
| `dr` | 法器伤害倍率（0.4 = 只吃四成；雷火光照样疼） |
| `ice` | 出场后几秒几乎打不动（降头尸） |
| `blink` | 隔几秒闪到别处（游尸） |
| `underground` | 不从鬼门关来，从镇里地下钻出来（伏尸） |
| `possess` | 去附身保安（马贼鬼魂） |
| `wax` | 走过留下蜡油，减速 |
| `fireWeak` | 怕火：雷火光伤害 ×2 |
| `dash` | 突然冲刺（浪人） |
| `charm` | 迷惑：方向颠倒（大罗金仙） |
| `noWisp` | 进镇不朝龙脉吐阴火 |
| `leak` | 踏进龙脉扣多少灵气（默认 2） |

## BOSS 字段（`D_BOSSES`）

基本：`n` 名字、`t` 类型、`skin`、`hp`（普通难度的血量）、`sc` 画多大、`summon` 召唤哪种小怪（`'mix'` = 随机）、`sumN` 一次几只、`sumCd` 几秒一次、`say` 出场台词、`dr`。

招式开关（写 `1` 就开）：

| 字段 | 效果 | 现在谁用 |
|---|---|---|
| `leaper` | 扑跳 | 任老爷、千年僵尸王、尸王 |
| `helpers` | 血掉到六成，四目道长 + 一休大师来帮忙（你是一休就只来四目） | 皇族僵尸 |
| `capture` | 出场抓走大宝，大宝变成敌人；王婆鬼王死了大宝回来 | 马贼王婆 |
| `next: '键'` | 死后变成另一个 BOSS | 王婆→`wangpoG`，尸王→`xieshen` |
| `jiuju` | 黑泥、石灰、瞬移，半血魔化，会打镇龙钉 | 九菊女教主 |
| `bats` | 放蝙蝠 | 老神父、告鲁斯 |
| `batShift` | 化成蝙蝠高速移动 | 告鲁斯 |
| `sunWeak` | 被八卦镜的日光照到掉血减速 | 告鲁斯 |
| `undying` | 打不死（血锁 1），血少于 35% 宗师埋炸药，把它引过去炸死 | 千年僵尸王 |
| `bolts` | 落雷砸你 | 妖尸·石少坚 |
| `thunder` | 掌心雷；雷劈到他自己掉 9% 最大血 | 石坚 |
| `pearl` | 定东珠护体（几秒几乎无敌） | 慈禧 |
| `dropPearl` | 死后掉定东珠，送回龙脉 +25 灵气 | 慈禧 |
| `revive` | 血少于 25% 逆天改命回到 70% | 杨飞云 |
| `curse` | 罗盘锁魂（你减速） | 杨飞云 |
| `call: '键'` | 出场几秒后叫来另一个 BOSS | 杨飞云→`gaolus` |
| `blood` | 走过留血池、吸血 | 血魔 |
| `immune` + `tame` | 定身控制无效；小尊来了能让它站住 4 秒 | 玄魁 |
| `charm` | 迷惑你（方向颠倒） | （可以给任何 BOSS 加） |
| `stomp` | 震地 | 邪神 |
| `final` | 最终 BOSS：打死就赢 | 邪神 |

## 每一波（`D_WAVES`）

```js
/* 11 */ { film: '僵尸大时代', mobs: { waxZ: 5, youZ: 2 }, elites: ['hairy'], boss: 'qiannian', event: 'waxHouse', tier: '…', say: ['…', '…'] },
```

| 字段 | 意思 |
|---|---|
| `film` | 出自哪部电影（波次横幅显示） |
| `mobs` | 小怪和比例（`D_MOBS` 的键：权重） |
| `elites` | 这一波出哪些精英 |
| `boss` | 这一波的 BOSS（`D_BOSSES` 的键），有 BOSS 的波更长 |
| `event` | 剧情事件，一个或数组 `['a', 'b']` |
| `tier` | 僵尸等级说明（第一次出现时弹出） |
| `say` | 开波剧情台词，一句一条 |
| `long` | 写 `1` 这一波时间加长 |

### 剧情事件（`event`）

| 键 | 剧情 | 代码（`defense.js`） |
|---|---|---|
| `wencai` | 文才当诱饵把鬼引回鬼门关；护送成功鬼全退、得赏；成没成王小凤都会来帮忙 | `dEvent` / `dBaitTick` / `dBaitDone` |
| `pals` | 大宝、小宝来帮忙 | `dPals` |
| `nails` | 九菊一派在三路打镇龙钉，一直漏龙脉灵气；站上去 1.5 秒拔掉 | `dNailTick` |
| `tulong` | 屠龙带 6 具赶尸偷运龙脉镇物；打掉屠龙，队伍散掉、缴获 60 文 | `dEvent` |
| `wuPriest` | 吴神父（你是神父就来九叔）来镇上帮守；中西合璧：每 18 秒伤害 ×1.5 持续 6 秒 | `dUnionTick` |
| `waxHouse` | 城内爆发：姜家腊味坊冲出血蜡尸（地图上 `MAP.lafang`） | `dStartWave` |
| `shisj` | 石少坚溜进镇找钱小姐；他死后疯狗冲出来 | `dEvent` / `dKill` |
| `mushroom` | 野外三处长出棺材菌，采一个 +40 文 | `dPickTick` |
| `mirrors` | 镇里三面八卦镜反射日光（克告鲁斯） | `dMirrorTick` |

## 数值（`D_TUNE`）

`waveGap` / `bossGap` 两波间隔秒数；`spawnDur` 一波刷多久；`count(w)` 一波多少只；`effT(w)` 怪的成长；`hpK(w)` 额外血量倍率；`firstWave` 开局几秒后第一波。

## 加一个新怪的三步

1. `defense_sprites.py` 里画一个函数（照着别的抄）。
2. `gen_defense.py` 里注册：搜 `('wencai', 'wencai')`，在那个列表里加 `('图名', '函数名')`。
3. `defense_data.js` 的 `D_MOBS` 加一行，然后在某一波的 `mobs` 里写上它。

新的 BOSS 招式、新的剧情事件需要写代码：BOSS 招式在 `defense.js` 的 `dBossTick`，事件在 `dEvent`（每帧要做的事加一个 `dXxxTick`，挂到 `updateEvents`），画面在 `drawEventSprites`。
