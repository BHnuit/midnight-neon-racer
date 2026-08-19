# AGENTS.md — 真夜中道路（契约仓）

本仓库是产品契约，不是提审包。正式工程在 `/Users/hant/工作台/projects/creation/midnightroad/`。

先读 [PROJECT.md](PROJECT.md)、[CONTEXT.md](CONTEXT.md)、[docs/new-session.md](docs/new-session.md)、[docs/framework-loop.md](docs/framework-loop.md)、[TREE.md](TREE.md)。进入正式工程后再读 `../midnightroad/AGENTS.md` 与 `../midnightroad/docs/architecture.md`。

## 两套东西，不要混

| | 是什么 | 状态 |
| --- | --- | --- |
| **真夜中道路** | Cocos 3.8.6 → 微信小游戏 | 主线。需求已对齐，方案已接受，当前 S0 |
| **午夜霓虹 · 极速赛车** | [archive/h5-demo/](archive/h5-demo/) | 已归档且已下线 |

## 正式小游戏

- 工程：`midnightroad/`（Empty 2D）。`midnightroad` 只是文件夹名
- 导出：`midnightroad/build/wechatgame/`。第一刀 A 已过
- 色块 MVP：`midnightroad/assets/scripts/MvpLoop.ts`，说明 [docs/cocos-slice-b-mvp.md](docs/cocos-slice-b-mvp.md)。**不是**正式第二刀
- 不要手搓正式包 `game.js`；不要在本仓库放 `.mcp.json`。MCP：[docs/cocos-mcp-pro.md](docs/cocos-mcp-pro.md)
- 不要手改 `.scene` / `.prefab` / `.anim` / `.meta`，用 Cocos MCP
- Cocos MCP 负责编辑器资产；微信小游戏助手 MCP 只验证 Creator 导出的 `build/wechatgame/`。两者不是同一个服务，不要混用工程路径
- 刷新微信导出包后，按 [完整方案](docs/plan.md) 执行助手 `run_game` → 打开预览 → `get_logs`；真机与上传必须另有授权和正式账号配置
- 出图已开。按 [ai-game-art-pipeline](.grok/skills/ai-game-art-pipeline/SKILL.md) 串行 G0→G6，先 A0 单锚点；预览和签名稿不进微信包。机位 A-2 在 [docs/art-bible-revision-01.md](docs/art-bible-revision-01.md)
- 完整方案在 [docs/plan.md](docs/plan.md)。Hans 已于 2026-08-18 接受，按 S0 再 S1 开工
- `game-studio` 只用于本轮前期顾问，已卸载；后续架构问题按 [docs/plan.md](docs/plan.md) §5.6 按需调用 `game-architect`，不把它当每次开发的工作流
- 双仓职责按 [ADR 0002](docs/adr/0002-dual-repo-governance.md) 执行。契约仓主动目录逐层 README；Cocos `assets/` 不放 README，职责统一写在工程 `docs/architecture.md`

## Netlify（已下线）

站还留着，只发 [archive/offline/](archive/offline/)。site id `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`。禁止不带 siteId 的 `netlify deploy`，禁止另建站。禁止把 `*.netlify.app` 或 racer.bhnuit.cn 当交付链接。禁止把 token 写进仓库。以后有新 Demo 再改 publish。

## 验证

- 契约/方案：读 PROJECT + CONTEXT，对照磁盘
- 色块循环：Creator 预览 `midnightroad` 的 `scene`
- 微信包：助手检查 `midnightroad/build/wechatgame/` 的预览/日志，再用开发者工具与真机验证平台能力
