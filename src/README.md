# 源文件（用来重新生成 public/index.html）

| 文件 | 作用 |
|---|---|
| `sprites.py` | 道士、僵尸、跳尸、游魂、尸王的像素图 |
| `walker.py` | 行尸像素图 |
| `map_gen2.py` | 地图背景、树和房子等物件、碰撞数据、村民像素图 |
| `game_template.html` | 游戏逻辑和界面（素材位置留空，由脚本填入） |
| `gen_assets.py` | 把以上全部打包成一个 `game.html` |

## 重新生成

需要 Python 3 和 Pillow（`pip install pillow`），以及 Noto Sans CJK 字体（用于义庄牌匾和路标文字，路径写在 `map_gen2.py` 的 `FONT`）。

```bash
cd src
python3 gen_assets.py
```

会生成两个文件：`src/game.html`（Claude 网页版用）和 `public/index.html`（Netlify 上线用）。把改好的 `public/index.html` 提交到 GitHub，Netlify 会自动重新部署。

## 防守版《守卫任家镇的中心的龙脉》

| 文件 | 作用 |
|---|---|
| `map_defense.py` | 防守地图：鬼门关三路 → 河与三座桥 → 四个野外点 → 任家镇三道城门 → 龙脉 |
| `defense.js` | 防守玩法：30 波、龙脉、守卫、杂货铺、野外 BOSS、重伤回镇、龙脉功德簿 |
| `gen_defense.py` | 用 `game_template.html` + 上面两个文件打包成 `src/longmai.html` 和 `public/longmai.html` |

```bash
cd src
python3 gen_defense.py
```

原游戏的文件不用改：角色、法器、怪物都直接沿用 `game_template.html`。排行榜是单独的 `/api/longmai`（`netlify/functions/longmai.mjs`）。
