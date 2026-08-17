# 第一刀 · A

Hans 已选 **A**（2026-08-17）。

过线标准只有一条：Cocos Creator **空场景**导出的微信小游戏包，能用微信开发者工具打开并跑起来。黑屏、默认立方体、默认相机都算过。不做选车、公路、广告、好友榜。

导入规则以 [wechat-minigame-start.md](wechat-minigame-start.md) 为准：选含 `project.config.json` 的那一层。Creator 构建选项见 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md)。

## 不做

- 不从飞机 Canvas2D 模板开正式工程
- 不手写一套 `game.js` 冒充过线
- 不改归档 Demo（`archive/h5-demo/`）/ 不上新 Netlify 站
- 不把 Demo 的 `window.__game` 搬进 Cocos

## 建议落点

Dashboard 新建选 **Empty(2D)** + 编辑器 **3.8.6**。不要 Empty(3D) / HQ / AR / VR / Hello World。

工程已建在 `/Users/hant/工作台/projects/creation/midnightroad/`（Empty 2D，Creator 3.8.6）。H5 Demo 仍在 `midnight-neon-racer`。设计分辨率 720×1280。

Cocos MCP Server **v1.7.9 Pro** 已在 `extensions/cocos-mcp-server/`。Grok / Cursor / Codex 连 `http://127.0.0.1:21569/mcp`。工具表和用法见 [cocos-mcp-pro.md](cocos-mcp-pro.md)。Creator 面板要开着；改端口就改客户端 `url`。

构建目标：微信小游戏。AppID 用真夜中道路那个号；没有号时可用测试号看预览，但不能上传、不能验广告。

## 谁做什么

| 谁 | 做什么 |
| --- | --- |
| 本机 Creator 3.8.6+ + 微信开发者工具 | 建空项目、构建、导入、点预览 |
| Cocos MCP + Grok / Cursor / Codex | 改编辑器里的场景和节点（见 [cocos-mcp-pro.md](cocos-mcp-pro.md)） |
| 本仓库会话 | 记契约；不代替 Creator 点构建 |

**2026-08-17 已过线。** Creator 导出 `midnightroad/build/wechatgame/`（含 `game.js` / `game.json` / `project.config.json`），微信开发者工具 Stable 2.01 已导入，模拟器在编。空场景黑屏符合 A。起始场景文件：`assets/scene.scene`。

下一刀（未开）：选车 + 一段三车道 + 本地结算。广告和好友榜仍不在第二刀。
