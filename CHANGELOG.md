# 变更记录

一行一次部署，按时间倒序。**部署前先在这里占一行**，说明谁在动哪块，避免两边同时改同一处。

| 时间 | 谁 | 改了什么 | 影响 |
|---|---|---|---|
| 2026-10-18 19:10 | DSH Agent | 加入版本闸门（`scripts/version.js`）、线上体检（`scripts/live-check.js`）、接口探测（`scripts/probe-api.js`）、每日烟雾测试、`docs/` 文档、netlify.toml 安全头与缓存头 | 无（不改游戏内容，只加工具与配置） |
| 2026-10-18 18:23 | 基线 | 抓取线上版本，建立基线（线上 sha256 `b160a9ea9f73…`，去 Netlify 注水后即 `origin/main` 的 `public/index.html`） | 无（只读） |
