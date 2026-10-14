# 暂时停止呼吸

道士在荒坟里对抗僵尸、屏住呼吸撑到天亮的像素割草游戏。

- `public/index.html`：游戏本体（一个文件，由 `src` 生成）
- `netlify/functions/scores.mjs`：共享排行榜「功德簿」（Netlify Functions + Blobs）
- `src/`：源文件，改游戏改这里，说明见 `src/README.md`

更新流程：在 `src` 里改 → `python3 src/gen_assets.py` 生成新的 `public/index.html` → 提交到 GitHub → Netlify 自动部署。
