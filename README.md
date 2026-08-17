# 真夜中道路

微信小游戏的**产品契约仓库**。玩法工程在旁边的 Cocos 目录 `../midnightroad/`，不在本 git 根下。

目标平台只有**微信小游戏**。旧 H5 在 [archive/h5-demo/](archive/h5-demo/)，Netlify 已下线（racer.bhnuit.cn 现在是停机页）。

## 先读

1. [PROJECT.md](PROJECT.md) 的 Startup Summary  
2. [CONTEXT.md](CONTEXT.md)  
3. [docs/new-session.md](docs/new-session.md)  
4. [TREE.md](TREE.md)

## 现在到哪

需求已对齐。Cocos 空包能进微信开发者工具；色块最小循环（选车 → 三车道 → 本地结算）在 Creator 预览里跑通过，**不是**正式第二刀。

[完整开发方案](docs/plan.md)已在前期用 Game Studio 与微信小游戏助手复审，当前待 Hans 验收。Game Studio 已卸载；后续只在架构决策节点按 §5.6 调用 `game-architect`。双仓目录治理和交接框架已经落地，但不等于 S0 或正式第二刀已开工。验收后先做 S0 工程基线，再做 S1 正式第二刀；验收前不改正式玩法。

## 两套目录

| 路径 | 是什么 |
| --- | --- |
| 本仓库 | 词、决定、完整方案、美术契约、验证证据、归档 Demo |
| `/Users/hant/工作台/projects/creation/midnightroad/` | Creator 3.8.6 工程 |

双仓目录责任与排除范围见 [ADR 0002](docs/adr/0002-dual-repo-governance.md)。

## 授权

MIT。作者 BHnuit / Hant。
