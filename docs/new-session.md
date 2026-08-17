# 新会话入口

先读这些，不要从聊天记录猜：

1. [PROJECT.md](../PROJECT.md) 的 Startup Summary
2. [CONTEXT.md](../CONTEXT.md) 全文
3. [TREE.md](../TREE.md) + [adr/0001-first-version-loop.md](adr/0001-first-version-loop.md) + [adr/0002-dual-repo-governance.md](adr/0002-dual-repo-governance.md)
4. 进入 Cocos 工程后读 `../../midnightroad/AGENTS.md` 与 `../../midnightroad/docs/architecture.md`

## 这一轮要做什么

[整个项目的开发方案](plan.md)已由 Hans 于 2026-08-18 接受。治理完成不等于 S0 完成。按方案先做 S0 工程基线，再做 S1 正式第二刀。不要把 `MvpLoop` 扩成正式架构。

## 两套目录

| 目录 | 是什么 |
| --- | --- |
| `.../midnight-neon-racer/` | 产品契约。GitHub `BHnuit/midnight-neon-racer`。旧 H5 在 `archive/h5-demo/` |
| `.../midnightroad/` | Cocos Creator 3.8.6 Empty(2D)。文件夹名不是店招 |

## 已锁、不要重问

个人 IAA、动作/跑酷、12+、真夜中道路、目标平台只有微信小游戏、画布 720×1280、种子大图约 5 分钟、三车道滑动换道、同时氮换道、五车定位、技能条约 2 秒、分值 A（路程 3000 / 擦车 200 / 碾压 500 / 完赛 1200）、一次广告续命、只做好友榜、里程 2/6/15 局、Cocos 不用手搓 `game.js`、第一刀 A 已过线、机位修法 A、出图暂停、H5/Netlify 已下线。

## 先停

- 局内精细出图
- 不要在契约仓库放 `.mcp.json`
- 不要把 `MvpLoop` 当成正式包
- 不要重开 Netlify 游戏站，除非 Hans 点名要新网页 Demo

## 未关

- 新会话热加载微信小游戏助手后，对 `midnightroad/build/wechatgame/` 补 `run_game` → 预览 → `get_logs`（S0-PKG）
- 按方案做 S1 正式第二刀：用 `RunSession` / `GameDirector` 替换 `MvpLoop`
- 备案截图等以后

## 实施会话手上有什么

- 已有：词、ADR 0001/0002、前期经 Game Studio / 微信小游戏助手复审的[完整开发方案](plan.md)、当前按需使用的 `game-architect`、画布 720×1280、MCP Pro、第一刀空包、[色块循环](cocos-slice-b-mvp.md)、双仓治理与 Cocos 架构地图
- 没有：正式第二刀、机位 A 上路、美术进包
- 第二刀预定范围仍是：选车 + 一段三车道 + 本地结算；广告和好友榜仍不进

实现时区分两套 MCP：Cocos MCP 改 Creator 资产；微信小游戏助手只接含 `game.js` 的 `midnightroad/build/wechatgame/`，用于构建后的预览、日志、截图与真机证据。不要在契约仓写 MCP 配置。

完整索引：[README.md](README.md)
