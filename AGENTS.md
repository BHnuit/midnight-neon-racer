# AGENTS.md — 真夜中道路（契约仓）

本仓库是产品契约，不是提审包。正式工程在 `/Users/hant/工作台/projects/creation/midnightroad/`。

先读 [PROJECT.md](PROJECT.md)、[CONTEXT.md](CONTEXT.md)、[docs/new-session.md](docs/new-session.md)、[TREE.md](TREE.md)。

## 两套东西，不要混

| | 是什么 | 状态 |
| --- | --- | --- |
| **真夜中道路** | Cocos 3.8.6 → 微信小游戏 | 主线。需求已对齐，正式方案未写 |
| **午夜霓虹 · 极速赛车** | [archive/h5-demo/](archive/h5-demo/) | 已归档且已下线 |

## 正式小游戏

- 工程：`midnightroad/`（Empty 2D）。`midnightroad` 只是文件夹名
- 导出：`midnightroad/build/wechatgame/`。第一刀 A 已过
- 色块 MVP：`midnightroad/assets/scripts/MvpLoop.ts`，说明 [docs/cocos-slice-b-mvp.md](docs/cocos-slice-b-mvp.md)。**不是**正式第二刀
- 不要手搓正式包 `game.js`；不要在本仓库放 `.mcp.json`。MCP：[docs/cocos-mcp-pro.md](docs/cocos-mcp-pro.md)
- 不要手改 `.scene` / `.prefab` / `.anim` / `.meta`，用 Cocos MCP
- 局内出图暂停。机位 A 在 [docs/art-bible-revision-01.md](docs/art-bible-revision-01.md)
- 正式开工前先另开会话写方案（`docs/plan.md`）

## Netlify（已下线）

站还留着，只发 [archive/offline/](archive/offline/)。site id `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`。禁止不带 siteId 的 `netlify deploy`，禁止另建站。禁止把 `*.netlify.app` 或 racer.bhnuit.cn 当交付链接。禁止把 token 写进仓库。以后有新 Demo 再改 publish。

## 验证

- 契约/方案：读 PROJECT + CONTEXT，对照磁盘
- 色块循环：Creator 预览 `midnightroad` 的 `scene`
- 微信包：开发者工具打开 `midnightroad/build/wechatgame/`
