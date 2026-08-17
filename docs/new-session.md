# 新会话入口

先读这些，不要从聊天记录猜：

1. [PROJECT.md](../PROJECT.md) 的 Startup Summary  
2. [CONTEXT.md](../CONTEXT.md) 全文  
3. [TREE.md](../TREE.md) + [adr/0001-first-version-loop.md](adr/0001-first-version-loop.md)

## 这一轮要做什么

写**整个项目的开发方案**，正文落 [plan.md](plan.md)（没有就新建）。不要一上来写正式第二刀代码，不要把 `MvpLoop` 扩成正式架构。

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

- 本会话：写出开发方案  
- 备案截图等以后  

## 方案会话手上有什么

- 已有：词、ADR 0001、画布 720×1280、MCP Pro、第一刀空包、[色块循环](cocos-slice-b-mvp.md)、文件树  
- 没有：`docs/plan.md`、机位 A 上路、美术进包  
- 第二刀预定范围仍是：选车 + 一段三车道 + 本地结算；广告和好友榜仍不进  

完整索引：[README.md](README.md)  
