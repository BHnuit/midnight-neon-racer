# 美术分册

本目录把 [art-bible.md](../art-bible.md) 和 [art-bible-revision-01.md](../art-bible-revision-01.md) 拆成可执行规范。Gate 6 已解除；按 skill 从 A0 单锚点串行出图。

| 文件 | 职责 |
| --- | --- |
| [palette.md](palette.md) | 色板语义与用色限制 |
| [pixel-grid.md](pixel-grid.md) | 像素网格与缩放纪律 |
| [layers.md](layers.md) | 00-sky 到 08-hud 图层合成 |
| [roadside-approach.md](roadside-approach.md) | 中近景按深度推进的方法 |
| [car-grounding.md](car-grounding.md) | 车辆接地、阴影与轮廓 |
| [sky-catalog.md](sky-catalog.md) | 天色阶段与空天主件 |
| [crt-menu.md](crt-menu.md) | CRT 只用于菜单，不覆盖赛道 |
| [../ui-art-production-spec.md](../ui-art-production-spec.md) | 出图前逐屏几何、运行时分层、素材批次和车流方向决策门 |
| [../ai-game-art-pipeline-research.md](../ai-game-art-pipeline-research.md) | AI 参考控制、像素/透明处理、manifest 与引擎验收的一手资料 |
| [AI 美术生产 skill](../../.grok/skills/ai-game-art-pipeline/SKILL.md) | G0–G6 正式生产编排；G1.5 先校准模型、提示词、语言与控制参数 |
| [pipeline-two-lists.png](pipeline-two-lists.png) | 工序 G0–G6 与批次 A0–A6 对照 |

Hans 已接受 [出图前规格](../ui-art-production-spec.md)并解除 Gate 6。从一个可验收锚点开始：G0 工单、G1 结构白模、G1.5 小型参数矩阵与 `style-profile`、G2–G4 成品，G5 代表资产进 Cocos，G6 验微信包。G1.5 未通过前不要批量生成整套资产。第一件是 A0 发车页风格锚点。
