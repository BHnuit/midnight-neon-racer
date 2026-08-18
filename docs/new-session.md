# 新会话入口

先读这些，不要从聊天记录猜：

1. [PROJECT.md](../PROJECT.md) 的 Startup Summary
2. [CONTEXT.md](../CONTEXT.md) 全文
3. [color-block-now.md](color-block-now.md)（代码结构、已锁需求、文案、屏幕图示）
4. [TREE.md](../TREE.md) + [adr/0007-screen-map.md](adr/0007-screen-map.md) + [adr/0010-exclusive-road-kinds.md](adr/0010-exclusive-road-kinds.md)
5. 进入 Cocos 工程后读 `/Users/hant/工作台/projects/creation/midnightroad/AGENTS.md` 与同仓 `docs/architecture.md`

## 这一轮要做什么

Gate 2–3、5 规则已过。第一版无广告。好友榜比历史最高。画面仍是色块。

玩法色块先停在这里。下一会话 **Codex 审查并优化界面**：发车/选车/说明/开车 HUD/结算的层级与可读性。入口 [color-block-now.md](color-block-now.md)。不改碰撞和分值，不接正式出图。改过 `MainController.ts` 后先 reimport 再播放。

然后按序：

1. Gate 6：是否解除出图暂停、用哪套图
2. 微信助手 `run_game`：补包级验证
3. Gate 4（延后）：流量主开通后接激励续命
4. 好友榜双号实榜

未确认前不上传、不出正式局内图。一次只确认一项。

## 两套目录

| 目录 | 是什么 |
| --- | --- |
| `.../midnight-neon-racer/` | 产品契约。GitHub `BHnuit/midnight-neon-racer`。旧 H5 在 `archive/h5-demo/` |
| `.../midnightroad/` | Cocos Creator 3.8.6 Empty(2D)。文件夹名不是店招 |

## 已锁、不要重问

个人主体、不开虚拟支付、动作/跑酷、12+、真夜中道路、目标平台只有微信小游戏、画布 720×1280、种子大图约 5 分钟、跟手横移、双击加速、晚躲擦车、连击阶梯 200/300/400/500、五车定位、技能条约 2 秒、分值 A、第一版无广告续命、好友榜比历史最高单局分、里程 2/6/15 局、Cocos 不用手搓 `game.js`、第一刀 A 已过线、机位修法 A、出图暂停、H5/Netlify 已下线。

## 先停

- 局内精细出图
- 不要在契约仓库放 `.mcp.json`
- 不要把 `MvpLoop` 当成正式包
- 不要重开 Netlify 游戏站，除非 Hans 点名要新网页 Demo

## 未关

- Gate 6、`run_game`；Gate 4 等流量主；好友榜双号以后再验
- 备案截图等以后

## 实施会话手上有什么

- 已有：词、ADR 0001–0010、[完整开发方案](plan.md)、S1–S5 模块、`MainController` 色块九层、37 个 core 测试、正式图鉴文案、[色块现状](color-block-now.md)
- 没有：界面设计审查结论、Creator 完整验收、微信助手 `run_game`、真机广告、双号实榜、正式美术进包

实现时区分两套 MCP：Cocos MCP 改 Creator 资产；微信小游戏助手只接含 `game.js` 的 `midnightroad/build/wechatgame/`，用于构建后的预览、日志、截图与真机证据。不要在契约仓写 MCP 配置。

完整索引：[README.md](README.md)
