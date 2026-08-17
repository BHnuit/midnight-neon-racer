# 文件树与治理边界

项目分成产品契约、正式 Cocos 源工程和微信生成包。三者职责不可混用，决定见 [ADR 0002](docs/adr/0002-dual-repo-governance.md)。

## 2026-08-18 磁盘现状

```text
creation/
├── midnight-neon-racer/          # 本仓：产品契约
│   ├── PROJECT.md                # 状态、验收与唯一下一步
│   ├── CONTEXT.md                # 已锁产品语言
│   ├── AGENTS.md                 # 本仓执行规则
│   ├── TREE.md                   # 本页
│   ├── docs/
│   │   ├── README.md             # 文档索引
│   │   ├── plan.md               # S0-S7 完整开发方案
│   │   ├── new-session.md        # 新会话恢复入口
│   │   ├── adr/README.md         # 稳定决策与编号规则
│   │   ├── art/README.md         # 美术分册索引；出图暂停
│   │   └── evidence/README.md    # 验证证据契约
│   ├── assets/
│   │   ├── README.md             # 素材进入/排除边界
│   │   └── minigame/
│   │       ├── README.md         # 小游戏美术工作区入口
│   │       ├── cars/             # 逐车资产与 manifest
│   │       ├── layers/           # 00-sky 到 08-hud 图层栈
│   │       ├── palette/          # 锁定色板与生成源
│   │       ├── previews/         # 构图实验，不是运行时资产
│   │       └── refs/             # 参考图，不进包
│   ├── archive/README.md         # 归档边界与禁止复用规则
│   ├── archive/h5-demo/          # 已冻结旧 H5
│   ├── archive/offline/          # Netlify 停机页
│   └── netlify.toml              # publish = archive/offline
│
└── midnightroad/                 # 独立 Git：Cocos Creator 3.8.6 源工程
    ├── AGENTS.md                 # 正式工程硬边界
    ├── README.md                 # 工程入口
    ├── docs/
    │   ├── README.md
    │   └── architecture.md       # assets 目标目录与模块职责地图
    ├── assets/
    │   ├── scene.scene           # 当前色块验证场景
    │   └── scripts/MvpLoop.ts    # 验证脚本，不是正式架构
    ├── tests/
    │   ├── README.md
    │   └── core/                 # S0 已配置 vitest + harness；尚无玩法行为测试
    ├── build-templates/
    │   ├── README.md             # 模板审计规则
    │   └── wechatgame/           # 微信模板，不塞说明文件
    ├── settings/                 # Creator 管理配置
    ├── extensions/               # Cocos MCP 插件/第三方依赖
    └── build/wechatgame/         # Creator 生成包；不作源代码
```

上表是主动维护内容摘要，不枚举 `.git/`、`.creator/`、`.grok/`、`.netlify/`、`.orca/`、`library/`、`temp/`、`profiles/`、`node_modules/`、`__pycache__/` 与 `.DS_Store` 等元数据、工具状态和生成缓存。

## README 覆盖规则

| 范围 | 规则 |
| --- | --- |
| 契约仓主动维护目录 | 每层放 README，说明职责、允许内容、禁区与上游规范 |
| 契约仓素材目录 | README 说明职责；`manifest.md` 另记实际文件、尺寸、版本与缺口，两者不能互相替代 |
| Cocos 工程根、`docs/`、`tests/`、`build-templates/` | 放 README/AGENTS，形成安全交接入口 |
| Cocos `assets/` 与子目录 | 不放 README，避免 Asset Database 导入和 `.meta` 噪声；职责集中在 `midnightroad/docs/architecture.md` |
| `build-templates/wechatgame/` | 不放 README，避免无关文件被复制进导出包 |
| 生成物、第三方依赖、工具状态、冻结归档内部 | 不批量加 README；由最近的主动目录入口说明排除原因 |

## 正式目标结构

Hans 接受 [完整开发方案](docs/plan.md) 后，实施 Agent 按切片通过 Creator/Cocos MCP 建立运行时目录：

```text
midnightroad/
├── assets/
│   ├── scenes/Main.scene
│   ├── prefabs/screens/          # Select / Run / Revive / Result
│   ├── prefabs/game/             # TrafficCar / Pickup
│   └── scripts/
│       ├── core/                 # 纯 TypeScript 局内规则、道路与进度
│       ├── app/                  # 产品流程协调
│       ├── cocos/                # 输入、视图和场景适配
│       └── platform/             # Dev / WeChat 平台适配
├── tests/core/                   # 确定性、计分、碰撞、进度行为测试
├── tsconfig.core.json            # 不依赖 Creator temp 的纯规则 typecheck
└── build-templates/wechatgame/
    └── openDataContext/          # S5 才创建的好友榜开放数据域
```

治理框架已经建立。S0 工程基线已有 Cocos commit `dda5a64`、独立 typecheck 与 vitest 空跑；微信助手空包验证仍 BLOCKED。不要把目录说明当作正式玩法进度，也不要提前创建无消费者的 manager、adapter 或序列化资产。

## 本仓库根上放什么

根目录只放跨会话恢复、产品契约、授权和下线部署指针。不要新增玩法脚本、根级网页入口或 `.mcp.json`；Cocos 场景不要拷入本仓。

旧 H5 只留在 `archive/h5-demo/`，Netlify 只发 `archive/offline/`。以后有明确的新网页 Demo 才调整站点。

## 后续从哪里开始

Hans 已于 2026-08-18 接受 [docs/plan.md](docs/plan.md)。当前从 S0 建立可恢复基线，再做 S1 正式第二刀；结论写回 `PROJECT.md` / `docs/adr/`，证据按 `docs/evidence/README.md` 归档。
