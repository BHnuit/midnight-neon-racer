# 文件树

两套目录，不要混。本仓库是**产品契约**；玩法代码在旁边的 Cocos 工程。

```
creation/
├── midnight-neon-racer/     ← 本仓库 GitHub BHnuit/midnight-neon-racer
│   ├── PROJECT.md           状态、验收、唯一下一步
│   ├── CONTEXT.md           已对齐的词
│   ├── AGENTS.md            本仓执行契约
│   ├── TREE.md              本页
│   ├── README.md
│   ├── docs/                契约与附录（见 docs/README.md）
│   ├── assets/              正式向素材（头像、美术预览）
│   ├── archive/h5-demo/     已冻结的旧 Demo（不再上线）
│   ├── archive/offline/     Netlify 停机页
│   ├── netlify.toml         publish = archive/offline
│   ├── package.json         无产品测试；目标平台是微信
│   └── .grok/skills/        本仓美术技能（mayonaka-art 等），未强制进 git
│
└── midnightroad/            ← 不在本 git 根下
    ├── assets/scene.scene   当前场景（含色块 MVP）
    ├── assets/scripts/MvpLoop.ts
    └── build/wechatgame/    第一刀导出包
```

## 本仓库根上放什么

只放跨会话恢复和部署指针：`PROJECT.md`、`CONTEXT.md`、`AGENTS.md`、`TREE.md`、`docs/`、`assets/`、`archive/`。

不要在根上再堆 `index.html` 或新的玩法脚本。不要放 `.mcp.json`。Cocos 场景不要手改、也不要拷进本仓。

## 归档

`archive/h5-demo/` 是旧 H5。Netlify 已下线，只留停机页。目标平台只有微信小游戏。以后有新网页 Demo 再开站。

## 下一轮方案往哪写

新会话写「整个项目的方案」时：结论进 `PROJECT.md` / `docs/adr/`；不要在聊天里只留一份。计划正文建议 `docs/plan.md`（还没有就新建，不要另起一套仓库）。
