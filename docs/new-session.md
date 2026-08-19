# 新会话入口

先读这些，不要从聊天记录猜：

1. [PROJECT.md](../PROJECT.md) 的 Startup Summary
2. [CONTEXT.md](../CONTEXT.md) 全文
3. [framework-loop.md](framework-loop.md)（改代码、Creator、微信预览）
4. [color-block-now.md](color-block-now.md)（代码结构、已锁需求、文案、屏幕图示）
5. [TREE.md](../TREE.md) + [adr/0007-screen-map.md](adr/0007-screen-map.md) + [adr/0010-exclusive-road-kinds.md](adr/0010-exclusive-road-kinds.md)
6. 进入 Cocos 工程后读 `/Users/hant/工作台/projects/creation/midnightroad/AGENTS.md` 与同仓 `docs/architecture.md`

## 这一轮要做什么

Gate 2–3、5、U0 与 U1/U2 核心矩阵已过。第一版无广告，好友榜比历史最高。五屏、混合车流、弯坡、统一擦车与低文字 HUD 已进入可试玩色块原型；技能空表 20 秒自然回满，换向进入不混流，场景/天体/地表连续接续。49 项规则测试和 Creator 场景/引用校验通过。画面仍是色块。

Hans 已于 2026-08-19 解除 Gate 6，并交代 A0 工单留到下一轮新会话。入口仍以 [PROJECT.md](../PROJECT.md) Startup Summary、[出图前规格](ui-art-production-spec.md) 和 [AI 美术生产 skill](../.grok/skills/ai-game-art-pipeline/SKILL.md) 为准。改玩法先读 [framework-loop.md](framework-loop.md)。

然后按序：

1. A0 发车页 TaiT 风格锚点：G0 工单 → G1 结构白模 → G1.5 风格配方；未过 G1.5 不批量
2. A1 菜单/HUD 模块（含底部半圆环仪表，替换占位整圆）
3. 一辆玩家车三视图、一种交通、一个路段，再考虑铺开
4. 接局内 FX 前补 `RunEvent[]` 与 `FxBack/FxFront`；长屏 SafeArea 先不管
5. Gate 4（延后）广告续命；好友榜双号以后再验

不上传。签名稿和预览不进微信包。一次只做一个闸门。

## 两套目录

| 目录 | 是什么 |
| --- | --- |
| `.../midnight-neon-racer/` | 产品契约。GitHub `BHnuit/midnight-neon-racer`。旧 H5 在 `archive/h5-demo/` |
| `.../midnightroad/` | Cocos Creator 3.8.6 Empty(2D)。文件夹名不是店招 |

## 已锁、不要重问

个人主体、不开虚拟支付、动作/跑酷、12+、真夜中道路、目标平台只有微信小游戏、画布 720×1280、种子大图约 5 分钟、跟手横移、双击加速、统一擦车、连击阶梯 200/300/400/500、路段级混合车流、三次危险段、OutRun 式左右弯/上下坡、五车定位、技能满表约 4 秒/空表约 20 秒自然回满、分值 A、第一版无广告续命、好友榜比历史最高单局分、里程 2/6/15 局、Cocos 不用手搓 `game.js`、第一刀 A 已过线、机位 A-2、五屏 UI 与 HUD 规格、Gate 6 已解除且出图走 G0→G6、H5/Netlify 已下线。

## 先停

- 未填 G0 / 未过 G1.5 就批量出图
- 把 `assets/minigame/previews/` 或签名稿打进微信包
- 不要在契约仓库放 `.mcp.json`
- 不要把 `MvpLoop` 当成正式包
- 不要重开 Netlify 游戏站，除非 Hans 点名要新网页 Demo

## 未关

- Gate 4 等流量主；好友榜双号以后再验；长屏 SafeArea 先不管
- 备案截图等以后

## 实施会话手上有什么

- 已有：词、ADR 0001–0012、[完整开发方案](plan.md)、[调试巡环](framework-loop.md)、S1–S5 模块、五屏与 `ColorBlockUi` 色块图层、混合车流/弯坡/换向隔离/场景接续核心矩阵、49 个规则测试、正式图鉴文案、[出图前规格](ui-art-production-spec.md)、[AI 美术生产 skill](../.grok/skills/ai-game-art-pipeline/SKILL.md) 与 [研究依据](ai-game-art-pipeline-research.md)；助手 `run_game` 发车/开车预览已通
- 没有：A0 G0 工单、长屏/异形 SafeArea 补测、真机广告、双号实榜、正式美术进包、开发者工具/真机包级 smoke

实现时按 [framework-loop.md](framework-loop.md) 区分两套 MCP。不要在契约仓写 MCP 配置。

完整索引：[README.md](README.md)
