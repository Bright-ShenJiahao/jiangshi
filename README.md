# 暂时停止呼吸

道士在荒坟里对抗僵尸、屏住呼吸撑到天亮的像素割草游戏。

- `public/index.html`：游戏本体（一个文件，由 `src` 生成）
- `netlify/functions/scores.mjs`：共享排行榜「功德簿」（Netlify Functions + Blobs）
- `src/`：源文件，改游戏改这里，说明见 `src/README.md`

更新流程：在 `src` 里改 → `python3 src/gen_assets.py` 生成新的 `public/index.html` → 提交到 GitHub → Netlify 自动部署。

---

## 版本闸门（两边同时改，靠这个不打架）

线上 = `origin/main` 的 `public/index.html` + Netlify 注入的一段 326 字节注释。
所以「线上有没有被别人改过」这个问题，等价于「本地和 origin/main 有没有差异」。

```bash
node scripts/version.js check   # 开工前/部署前：本地 / origin/main / 线上 三方对比
node scripts/version.js sync    # 本地落后了：把 public/index.html 恢复成 origin/main（拒绝覆盖未提交改动）
node scripts/version.js bump    # 改完：把 BUILD 时间戳更新为当前分钟（YYMMDDHHmm）
```

`check` 的退出码：`0` 干净；`2` 有漂移（本地落后 / 线上不是 origin/main 构建的）。
**退出码非 0 就不要部署**，先查是谁先动了。

### 常用命令

```bash
node scripts/live-check.js          # 线上健康检查（体积、/api/scores、响应头、章节文件）
node scripts/live-check.js --save   # 顺手存一份快照到 .snapshots/（不提交）
node scripts/probe-api.js           # 只读探测 /api/scores 的路由形态
```

### 协作约定

1. **一个主分支、小步提交**，部署前先看 `git diff`。
2. 改之前先在 `CHANGELOG.md` 占一行，说明谁在动哪块，避免两边同时改同一处。
3. 两边各自开分支（`claude/xxx`、`agent/xxx`），冲突在 PR 里暴露，不要等上线后才发现。
4. 单文件阶段仍建议**串行**改：同一天只让一方动 `public/index.html`。

---

## 文档

- [`docs/技术体检报告.md`](docs/技术体检报告.md)：性能、结构、待办的体检结论（P0-1 素材外置、P0-2 章节补齐等）
- [`docs/给-Claude-的开工指令.md`](docs/给-Claude-的开工指令.md)：给 Claude 的版本闸门使用说明，每次开工贴给它
- `.github/workflows/smoke.yml`：每天定时跑一次线上烟雾测试
