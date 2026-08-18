# 新会话入口

先读这些，不要从聊天记录猜：

1. [PROJECT.md](../PROJECT.md) 的 Startup Summary
2. [CONTEXT.md](../CONTEXT.md) 全文
3. [TREE.md](../TREE.md) + [adr/0001-first-version-loop.md](adr/0001-first-version-loop.md) + [adr/0002-dual-repo-governance.md](adr/0002-dual-repo-governance.md)
4. 进入 Cocos 工程后读 `../../midnightroad/AGENTS.md` 与 `../../midnightroad/docs/architecture.md`

## 这一轮要做什么

Gate 2 操作已改：跟手横移、双击加速、晚躲擦车、连击阶梯。Cocos 预览走短段。等 Hans 再摸。画面仍是色块。

下一会话按序确认：

1. Gate 2：短段新手感能不能进下一阶段
2. Gate 3：五车定位有没有被调参拧歪
3. Gate 4：正式 AppID + 激励广告位；真机看一次广告
4. Gate 5：好友榜默认「历史最高」；两个真实微信号对一下顺序
5. Gate 6：是否解除出图暂停、用哪套图
6. 微信助手 `run_game`：补包级验证（本会话 BLOCKED）

未确认前不上传、不出正式局内图。一次只确认一项。

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

- 上表 6 项确认（见「这一轮要做什么」）
- 备案截图等以后

## 实施会话手上有什么

- 已有：词、ADR 0001/0002、已接受的[完整开发方案](plan.md)、S0 基线、S1–S5 正式模块与 `MainController`、16 个 core 测试、选车截图
- 没有：Creator 完整试跑证据、微信助手 `run_game`、真机广告、双号实榜、正式美术进包

实现时区分两套 MCP：Cocos MCP 改 Creator 资产；微信小游戏助手只接含 `game.js` 的 `midnightroad/build/wechatgame/`，用于构建后的预览、日志、截图与真机证据。不要在契约仓写 MCP 配置。

完整索引：[README.md](README.md)
