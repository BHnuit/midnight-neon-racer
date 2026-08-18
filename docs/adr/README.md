# 架构决策记录

这里保存会影响多个切片、后续 Agent 或交付边界的稳定决定。

| ADR | 决定 |
| --- | --- |
| [0001-first-version-loop.md](0001-first-version-loop.md) | 第一版产品循环，不沿用旧 Demo 一命闪避 |
| [0002-dual-repo-governance.md](0002-dual-repo-governance.md) | 契约仓、Cocos 源工程与微信生成包的职责边界 |
| [0003-follow-steer.md](0003-follow-steer.md) | 人车跟手横移，松手停缝；加速改双击 |
| [0004-late-dodge-graze.md](0004-late-dodge-graze.md) | 擦车是迎面晚躲，不是贴身路过 |
| [0005-graze-combo.md](0005-graze-combo.md) | 第一版做擦车连击，只吃擦车 |

新 ADR 使用递增四位编号，写清 Context、Decision、Consequences 和 Status。普通进度写 `PROJECT.md`，实现细节写代码/工程文档，不为可逆的小改动滥建 ADR。
