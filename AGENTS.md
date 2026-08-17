# AGENTS.md — 给 grokbot / 后续 Agent

你在接手 **午夜霓虹 · 极速赛车**。这是一个已经上线的单页游戏，不是空项目。

## 现在能做什么

- 打开 https://racer.bhnuit.cn 就能玩
- 6 种玩家车、对向车（轿车/出租/货车/面包/警车/救护）、转向灯、加速带/护盾
- 排行榜（Netlify Functions + Blobs）
- 幻影伪联机：同屏最多 3 辆，按分数区段排队，遵守车道/间距/不重叠
- 发车有引擎声 + 垫底合成旋律；右上角 SVG 静音 / 转发

## 怎么改

1. 主逻辑几乎全在 `index.html` 的 IIFE 里。先读再改，不要拆成框架除非 Hans 明确要求。
2. 排行榜后端只动 `netlify/functions/leaderboard.js`。
3. 调试接口：`window.__game`（`player` / `cars` / `ghostCars` / `setLeaderboard` / `setScore`）。测试依赖它，不要删。
4. 改完按 [DEPLOY.md](DEPLOY.md) 部署到**已有站点**，再 `npm test`。
5. 不要提交 token、`.netlify/` 缓存、`node_modules`。

## 硬约束

- **禁止** `netlify deploy` 时不带 siteId——会静默新建站。先写 `.netlify/state.json`。
- **禁止** 把 `*.netlify.app` 当对外交付链接（微信拦截）。
- **禁止** 把 Netlify / GitHub token 写进仓库或聊天记录存档。
- 交互改动必须 Playwright 验证，curl 200 不算验收。
- 玩家车保持可识别的蓝色系（默认「疾风」），方便 e2e。
- 幻影：同屏 ≤ 3，按昵称去重，分数追平下场，下一辆符合「分数仍领先玩家」才补位。
- 车与车、车与道具不能重叠；变道前要亮转向灯。
- 不要加独立 BGM 文件；当前是 WebAudio 现场合成。Hans 说过游戏要有背景音，指的是合成垫底，不是外链 mp3。

## 建议下一步（未做，需 Hans 点头再扩大）

- 把 `index.html` 拆成模块（仅当文件继续膨胀、改不动时）
- 幻影回放真实轨迹，而不是分数差估算位置
- 排行榜按日/周重置
- 音效在微信里仍可能被系统静音，需要更稳的解锁路径
- 移动端 UI 再收一收（HUD / 选车）

## 验证命令

```bash
npm test
```

失败就修，不要带着红的部署。

## 生产身份

- GitHub：`BHnuit/midnight-neon-racer`（本仓库）
- Netlify site id：`31c60f42-99a4-4890-a9a3-aa50ff2c7c92`
- 域名：`racer.bhnuit.cn`
