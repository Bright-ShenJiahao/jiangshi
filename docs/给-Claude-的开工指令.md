# 给 Claude 的开工指令（每次复制粘贴）

> 用法：每次让 Claude 改游戏之前，把下面整段贴在对话最前面。
> 目的：让它先对齐线上最新版，别拿旧版本重画。
>
> 背景：这个仓库已经用 **Git 自动部署**——线上就是 `origin/main` 的 `public/index.html`。
> 所以「对齐线上」= 「确认你手上的版本 = `origin/main` 的版本」。

---

开工前请先做这几步，不要跳过：

1. **先同步仓库**，别在旧版本上改：
   ```
   git fetch origin
   git checkout main && git pull --ff-only
   git log --oneline -5
   ```
   如果 `git pull` 不干净（有本地未提交改动），先停下来问我，不要 `reset --hard`、不要强推。

2. **确认版本一致**：
   ```
   node scripts/version.js check
   ```
   期望看到 `✅ 本地 = origin/main = 线上`。
   如果显示「线上 ≠ origin/main」，说明有人刚推了但还没部署完，或者部署失败了——先告诉我，不要动手。

3. **改哪里**：只改 `src/`（`game_template.html`、`map_*.py`、`*_sprites.py` 等），
   然后跑 `python3 src/gen_assets.py` 重新生成 `public/index.html`。
   **不要直接手改 `public/index.html`**——它是生成产物，手改会在下次生成时被覆盖。

4. **改完跑一遍**：
   ```
   node scripts/version.js bump     # 把页面里的 const BUILD 更新成当前时间 YYMMDDHHmm
   node scripts/live-check.js       # 线上健康检查（可选，push 之后跑）
   ```

5. **提交走分支 + PR，不要直接推 main**：
   ```
   git checkout -b claude/xxx
   git add -A && git commit -m "一句话说明改了什么"
   git push -u origin claude/xxx
   ```
   然后在 GitHub 上开 PR，等我 review 合并。合并后 Netlify 自动部署。

6. **最后告诉我**：改了什么、`BUILD` 新旧值、`public/index.html` 从多少 MB 变成多少 MB、改了哪些文件。

---

补充：如果确实拿不到仓库（比如只有一份 HTML 文件），那就**以 https://jiangshidaozhang.netlify.app/ 的实际页面为准**，
把页面里 `const BUILD = '...'` 的值报给我，对不上就不要动手。
