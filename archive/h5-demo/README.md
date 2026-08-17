# 归档 · H5 Demo（午夜霓虹 · 极速赛车）

2026-08-17 起，本目录是**冻结的旧 Demo**。不是提审包，也已从 Netlify **下线**。

- 店招是 **真夜中道路**，目标平台只有微信小游戏  
- 不要把这里的循环、全球榜、幻影搬进小游戏  
- 不要重新部署本目录，除非 Hans 明确要再开网页 Demo

## 里面有什么

| 路径 | 是什么 |
| --- | --- |
| `index.html` | 单文件 Canvas 游戏 |
| `netlify/functions/leaderboard.js` | 排行榜 |
| `tests/` | Playwright，默认打线上站 |
| `DEPLOY.md` | 已有站点的部署说明 |

## 不要默认部署

仓库根 `netlify.toml` 现在指向 `archive/offline/`（停机页）。site 还在，id `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`。禁止另建站。
