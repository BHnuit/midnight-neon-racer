# 真夜中道路 · 第一版完整开发方案

**状态**：accepted（Hans 2026-08-18「接受，授权开工」；Gate 1 关闭）

**适用工程**：Cocos Creator 3.8.6，`/Users/hant/工作台/projects/creation/midnightroad/`

**目标平台**：微信小游戏，个人主体，IAA

**方案日期**：2026-08-17；2026-08-18 前期用 Game Studio 1.0.0 与微信小游戏助手 1.0.1 复审，后续改用 `game-architect` 按需提供架构参考

**正式实现状态**：尚未开始；现有 `MvpLoop.ts` 只是一轮色块验证

## 1. 这份方案解决什么

这份文档是实现 Agent 的执行契约。它把已经确认的产品需求翻译为：

- 正式代码应采用的模块、interface、seam 与 adapter；
- 从当前色块验证到微信可提审版本的开发顺序；
- 每一刀包含什么、不包含什么、如何验收；
- 自动测试、Creator 预览、微信开发者工具和真机分别证明什么；
- 自审、交接、停止和 Hans 决策的标准。

实现 Agent 不需要重新访谈已锁需求，也不能用本方案覆盖 `CONTEXT.md`。若产品事实冲突，优先级为：

1. `PROJECT.md` 的当前目标、验收与唯一下一步；
2. `CONTEXT.md` 的已确认产品语言；
3. ADR（当前为 `adr/0001-first-version-loop.md`）；
4. 本方案的实现决定；
5. 当前代码与运行证据。

若 1–3 与实际代码冲突，先报告，不以代码现状反推产品契约。

## 2. 交付目的

第一版最终交付不是 H5，也不是一个演示场景，而是可由 Cocos Creator 导出、在微信开发者工具和真机运行的微信小游戏 **真夜中道路**。

玩家最终应能：

1. 在竖屏选车页查看五辆定位车并选择已解锁车辆；
2. 进入由种子生成的一条必经三车道大图，从傍晚开到清晨；
3. 滑动换道，并可同时按住当前车辆的氮、飞行或碾压技能；
4. 当场看到路程、擦车、碾压和完赛四项得分；
5. 中途折损时选择直接结算，或每局最多看一次激励视频后原地续命；
6. 以累计里程解锁五辆车，不使用货币或内购；
7. 在结算页看到本局细分、总分和微信好友榜；
8. 退出后再次进入仍保留累计里程、已解锁车辆、所选车辆和历史最佳单局分。

第一版完成印章必须分开：

```text
实现完成 -> Cocos 正式工程可运行 -> 微信包验证 -> Hans 验收 -> Hans 授权提交 -> 正式发布
```

本方案只授权走到可验收版本；不授权自动提交备案、上传审核或发布。

### 2.1 玩家体验支柱

实现决策先过下面四个设计测试；不能服务支柱的功能不进入第一版。

| 支柱 | 玩家感受 | 设计测试 |
| --- | --- | --- |
| 一晚一局 | 从傍晚驶到清晨，短时间内走完一条完整旅程 | 删除该内容后，玩家是否还明确感到「开完一整晚」 |
| 轻操作高风险 | 只做换道与按住技能，但要持续读路、抢擦车和管理保险杠 | 是否能用两种输入完成，且技巧不是自动送分 |
| 五车有取舍 | 解锁不是单向变强，而是速度、耐撞、车宽、飞行和碾压的选择 | 每辆车是否能在一次短测中表现出独有优势与代价 |
| 分数当场可读 | 技巧行为立即反馈，结算能解释总分从哪里来 | 玩家不看代码能否复述本次主要得分来源 |

反支柱：不做驾驶模拟、不做复杂连招、不做开放路网、不做付费数值成长，也不把广告变成强制流程。

### 2.2 核心循环与玩家旅程

```text
选已解锁车辆 -> 读路/换道/用技能 -> 冒险拿技巧分 -> 完赛或折损
      ^                                                   |
      |                                                   v
里程解锁新取舍 <- 保存本局实际里程 <- 结算细分/好友榜/重开
                                      ^
                                      └─ 每局最多一次自愿广告续命
```

首局必须在不读说明的前提下完成「选跑车、开局、换道、碰撞、结算、重开」；长期目标只由累计里程和好友最高单局分承载，不再引入货币或任务系统。

## 3. 已锁产品契约

| 项 | 第一版契约 |
| --- | --- |
| 名称 | 正式名为「真夜中道路」；旧 H5 名称不得作为正式店招 |
| 平台 | 仅微信小游戏，不继续交付网页游戏 |
| 主体 / 变现 | 个人主体；IAA；无虚拟支付 |
| 类目 / 适龄 | 动作 / 跑酷；12+ |
| 画布 | 720×1280，Portrait |
| 局结构 | 一张由种子拼成的必经大图，无圈、无分叉、无高度 |
| 局长 | 按最高速度约 5 分钟；不是倒计时 |
| 路面 | 默认三车道；路段可暂时宽窄变化，但操作仍是离散换道 |
| 输入 | 滑动换道；按住技能；技能期间仍能换道，两种输入互不取消 |
| 天色 / 天气 | 每局傍晚到清晨；每局抽一种晴、雨、雪、雾或大风滤镜，天气不改物理 |
| 得分 | 路程约 3000；每车擦车 +200 且只记一次；技能碾压 +500；完赛 +1200 |
| 短段完赛 | 按短段占完整大图的比例给完赛分，最低 +300 |
| 飞行得分 | 飞行期间只计路程，不计擦车或碾压 |
| 生命 | 全车 1 心；保险杠空后下一撞才掉心 |
| 保险杠 | 跑车/飞行汽车 1 格，小货车/压路机 3 格，摩托车 0 格 |
| 技能条 | 按住消耗；一次约 2 秒；满表约两次；开局半表；装置补充 |
| 车辆 | 跑车、小货车、摩托车、飞行汽车、压路机 |
| 车辆定位 | 跑车更快；货车更硬；摩托窄且无杠；飞行无视交通；压路机技能碾车与护栏 |
| 解锁 | 新号跑车；约 2 局货车、6 局摩托、15 局飞行汽车与压路机 |
| 里程 | 跨局累计走过的路，中途结束也累计；不是货币 |
| 续命 | 每局最多一次；完整观看激励视频后原地恢复 1 心和该车满杠 |
| 社交 | 只做结算好友榜；不做全球榜、幻影、上榜奖励 |
| 美术 | 赛博像素；机位 A 已锁；局内精细出图当前暂停 |

第一版明确不做：内购、金币/商城、全球榜、幻影陪跑、连击、真转向、摇杆、分叉、高度、天气物理、横幅或插屏广告、手写正式 `game.js`、复活次数购买、把旧 H5 搬进 Cocos。

## 4. 当前基线与已知缺口

### 4.1 已证明

- Cocos Creator 3.8.6 Empty 2D 工程存在，设计分辨率为 720×1280；
- Cocos 能导出 `build/wechatgame/`，微信开发者工具已成功导入第一刀空包；
- Cocos MCP 3.x Pro 可操作工程；
- `MvpLoop.ts` 在 Creator 预览跑通过「选车 -> 三车道短段 -> 本地结算」；
- 色块验证包含滑动换道、按住氮、路程/擦车计分、碰撞与结算三屏。

### 4.2 没有证明

- `MvpLoop.ts` 不是正式架构，也没有证明五分钟长局、确定性种子或五车能力；
- 当前微信包是第一刀空包，未证明正式玩法已重新构建进微信包；
- 未接真实存储、激励视频、微信关系链或开放数据域；
- 未验证真机多点触控、前后台切换、广告返回、包体和长局性能；
- 局内正式美术尚未批准，机位 A 尚未进入运行时；
- 契约仓本刀有文档与证据提交；Cocos 工程基线为 `dda5a64`（`main`），实现分支 `BHnuit/s1-formal-second-slice`。

### 4.3 2026-08-18 磁盘结构审查

| 观察 | 风险 | 处理阶段 |
| --- | --- | --- |
| 正式工程只有 `assets/scene.scene` 与 `MvpLoop.ts` | 单文件同时管输入、生成、碰撞、计分和 UI，无法安全扩展 | S1 用 §6 模块纵切替换，不原地重构成上帝类 |
| Cocos Git 尚无 commit | 不能定位验证基线，也无法可靠交给下一位 Agent | S0 建基线提交后才写正式玩法 |
| `package.json` 没有测试脚本或 lockfile | 纯规则没有可重复自动验证入口 | S0 建 `tests/core/`、独立 tsconfig、test/typecheck 脚本并提交 lockfile |
| 根 `tsconfig.json` 依赖生成的 `temp/tsconfig.cocos.json` | 无 Creator 环境时 core typecheck 不可恢复 | S0 新增只覆盖 core/tests 的 `tsconfig.core.json` |
| 2026-08-18 已补 `.DS_Store`、微信私有配置、私钥与测试产物忽略规则，但尚未进入基线提交 | 规则未被可定位 commit 固化；磁盘仍有已忽略的系统垃圾 | S0 复核 ignore 命中、清点已知垃圾，并随 Cocos 基线提交固化规则 |
| `build-templates/wechatgame/game.ejs` 含自定义方向/DPR 修补 | 模板可能偏离 3.8.6 默认行为，影响触摸坐标与分辨率 | S0 与 3.8.6 默认模板 diff；没有复现证据就移除，有必要则写明原因并做 Android/iOS 检查 |
| `project.config.json` 的 AppID 为空，导出包仅是第一刀证据 | 不能据此证明广告、关系链或上传能力 | S4/S5/S7 用正式 AppID 分别验；私钥只在用户环境配置 |
| `build/wechatgame/` 是生成物且当前未含正式玩法 | 直接改生成的 `game.js` 会在下一次构建丢失 | 所有正式逻辑只进 Cocos 源；构建后把该目录交包级工具验证 |
| 微信小游戏助手 skill 已安装，但本会话没有暴露其 MCP 工具 | 安装 skill 不等于运行时 MCP 可调用 | S0 首次包级验证先调工具；不可用时按 skill 的检测/配置流程处理，不往契约仓写 `.mcp.json` |

当前树与目标树分别记录在 `TREE.md`。2026-08-18 已建立双仓治理骨架：契约仓主动目录有职责 README，Cocos 工程有根级 AGENTS/README、`docs/architecture.md` 和 `tests/core/` 说明。Cocos `assets/` 下的正式目录仍按切片通过 Creator/Cocos MCP 创建，不预先生成空 `manager`、空 adapter 或无消费者的抽象。

## 5. 总体开发原则

### 5.1 正式实现替换验证代码

`MvpLoop.ts` 只用于理解已验证行为。正式第二刀从新模块和正式场景结构开始，不在这个单文件状态机上继续加字段、条件和微信调用。

迁移规则：

1. 正式模块先达到与色块验证相同的三屏闭环；
2. 场景不再挂载 `MvpLoop` 后，删除脚本及其无用节点引用；
3. 不长期保留「新旧两套循环」或兼容层；
4. 任何有价值的规则转成正式模块的行为测试，不复制旧实现细节。

### 5.2 规则与引擎分开

纯规则代码不得 import `cc`，不得直接读节点，也不得调用 `wx`。Cocos 每帧把输入交给规则模块，再依据返回的 snapshot 与 events 更新画面。

这样可以在三层验证同一条规则：

```text
输入脚本 -> RunSession -> snapshot/events -> Cocos view -> 微信构建
                ^                                  |
                |                                  v
          纯 TypeScript 测试              Creator / 微信实机证据
```

### 5.3 只在真实 seam 放 adapter

微信 SDK 是真实外部依赖，需要生产 adapter 和开发 adapter。道路、计分和车辆规则都是进程内计算，不为它们创建一层层 port、repository 或事件总线。

### 5.4 配置数据化，但不做配置平台

车辆数值、得分、技能容量、解锁阈值、路段模板和天气列表集中在带类型的 TypeScript 配置中。第一版不做运行时后台、热更新协议或通用 JSON 编辑器。

### 5.5 一刀一个可运行纵切

每一刀结束时，玩家必须比上一刀多完成一段真实流程。只有文档、节点数量、类数量或测试数量增加，不算进度。

### 5.6 架构顾问按需调用

`game-architect` 是知识参考，不是项目工作流。流程、验收和停止条件仍以本方案为准；不要每次写代码、修 Bug 或跑包都调用它。

| 节点 | 调用时机 | 读取参考 | 输出边界 |
| --- | --- | --- | --- |
| S0/S1 架构落地 | 建立正式 `core/app/cocos/platform` seam、固定 tick/FSM/状态边界前 | `macro-design.md`、`principles.md`、`project-structure.md`、`system-time.md` | 只审模块职责、依赖方向和可测试性；不凭空增加框架层 |
| S2 种子大图 | 设计 `RoadFactory`、路段模板、seed 重放和可玩性验证前 | `system-pcg.md`、必要时 `algorithm.md` | 优先模板组装 + 确定性 seed；不引入 WFC、噪声或 AI Director，除非需求/测量证明需要 |
| 重大需求变更 | 已锁 `CONTEXT.md` 的规则、平台或交付边界发生实质变化时 | `requirement-change-strategy.md`，同域演进再读 `evolution.md` | 先划变更范围，再决定演进、迁移或重写；先更新契约/ADR，不直接补丁式扩散 |
| 已证实的性能瓶颈 | profile/真机证据显示掉帧、GC、加载或包体问题后 | `performance-optimization.md`，必要时 `distribution.md` | 先测量再优化；输出一项可验证改动，不为猜测提前上对象池、并行或复杂调度 |

以下情况不调用：普通功能实现、单元测试编写、数值微调、Creator MCP 操作、微信助手 `run_game/get_logs`、备案/上传操作。它们分别由本方案、Cocos MCP 和微信小游戏助手负责。

### 5.7 项目技能矩阵

按当前个人项目的实际边界，日常开发只保留下列 10 个项目技能；另有 3 个横切维护技能。技能是按需工具，不是每个会话的固定启动清单。

| 技能 | 类型 | 建议调用节点 | 明确不调用 |
| --- | --- | --- | --- |
| `game-architect` | 架构顾问 | S0/S1 架构落地、S2 PCG、重大需求变更、已测出的性能瓶颈；详见 §5.6 | 普通编码、修 Bug、调数值、跑包 |
| `weixin-minigame-helper` | 包级验证 | S0/S1/S4/S5/S7 重新构建 `build/wechatgame/` 后，做 `run_game`、预览、`get_logs`、截图；代码触发规则以其 SKILL 为准 | 把 Cocos 工程根直接交给助手，或手改生成 `game.js` |
| `codebase-design` | 深模块设计 | S1 设计 `RunSession` / `PlatformPort`，或后续发现模块边界变浅时 | 为一行转发函数、单实现接口或普通重命名调用 |
| `domain-modeling` | 领域词与模型 | 新增/改变车辆能力、局内状态、里程、续命、好友榜等稳定概念时 | 已锁术语的常规实现 |
| `tdd` | 行为测试 | S0 测试基线；S1-S5 每个新增 core 规则或平台边界；先补会失败的行为测试 | 纯文档、Creator 节点摆放、无行为变化的重命名 |
| `code-review` | 变更审查 | S1/S2/S3/S4/S5/S7 gate 前，对照 base commit 做 Spec/Standards 审查 | 每次小改动都启动完整审查 |
| `diagnosing-bugs` | 故障诊断 | 出现运行时错误、状态残留、掉帧、GC、触控或平台回归时 | 没有故障信号时预先“诊断” |
| `research` | 外部事实核查 | Cocos/微信 SDK、平台限制、广告/开放数据域、包体或发布规则需要当前官方资料时 | 已由契约仓和本地手册覆盖的稳定事实 |
| `computer-use` | GUI 证据操作 | 需要操作 Creator、微信开发者工具或读取桌面窗口状态时 | 纯 TypeScript 测试和文档检查 |
| `prototype` | 隔离原型 | 新机制无法靠文档判断手感时，在正式工程外做最小验证 | 已通过的色块 MVP，或把原型直接升级为正式架构 |
| `ponytail:ponytail` | 横切约束 | 全程：优先删减、复用现有工具、拒绝无消费者抽象 | 用户明确要求完整复杂方案时绕过需求 |
| `self-improve` | 横切维护 | 命令/工具失败、用户纠正、发现可复用教训时 | 把项目进度或 ADR 写进 lesson |
| `skill-installer` | 环境维护 | 安装、替换、升级技能时 | 游戏实现和运行验证 |

暂停或不纳入本项目日常清单：`game-studio` 已卸载；`imagegen`、`design`、`tait-crt-interface-skill` 只有在 Hans 解除 S6 出图暂停后才重新评估；飞书、幻灯片、品牌、Web UI 等技能不服务当前 Cocos 微信小游戏主线。

## 6. 正式模块设计

建议目录如下；实现 Agent 可在不改变 seam 和职责的前提下微调文件名：

目录职责、首次创建阶段和排除规则已同步到 Cocos 工程 `docs/architecture.md`。由于 `assets/` 受 Creator Asset Database 管理，不在其子目录放 README；下列运行时目录到对应切片才由 Creator/Cocos MCP 创建。

```text
midnightroad/
├── assets/
│   ├── scenes/Main.scene
│   ├── prefabs/
│   │   ├── screens/          # Select / Run / Revive / Result
│   │   └── game/             # TrafficCar / Pickup
│   └── scripts/
│       ├── core/             # RunSession / RoadFactory / PlayerProgress / GameBalance / types
│       ├── app/              # GameDirector
│       ├── cocos/            # MainController / RunInput / RunView / screen controllers
│       └── platform/         # PlatformPort / DevPlatformAdapter / WeChatPlatformAdapter
├── tests/core/
├── tsconfig.core.json
└── build-templates/wechatgame/
    └── openDataContext/      # S5 才创建；开放数据域源码随构建复制
```

依赖方向固定为单向；箭头右侧不得反向 import 左侧：

```text
types/GameBalance -> RoadFactory -> RunSession -> GameDirector -> Cocos controllers/views
                                               -> PlatformPort <- Dev / WeChat adapters
WeChat adapter -> 主域消息 -> open-data renderer（独立执行环境）
```

| 模块 | 上游输入 | 对外输出 | 禁止依赖 |
| --- | --- | --- | --- |
| `RoadFactory` | seed、版本化 `RoadConfig` | 不可变 `RoadPlan` | Cocos Node、`wx`、存档 |
| `RunSession` | `RoadPlan`、车辆配置、逐帧输入 | snapshot、events、最终 result | UI、存储、广告、排行榜 |
| `PlayerProgress` | raw profile、`RunResult` | 校验后的新 profile | Cocos、`wx`、局内 Node |
| `GameDirector` | core 接口、`PlatformPort` | 产品状态与 screen model | 道路生成细节、直接 `wx` |
| Cocos 层 | director snapshot/events | 节点、触摸、视觉反馈 | 第二份权威分数/生命/解锁规则 |
| Platform adapters | `PlatformPort` 调用 | 存储/广告/榜结果 | 改写 core 结果或 UI 层级 |
| 开放数据域 | 主域消息、微信好友托管数据 | shared canvas 排行榜 | 主域节点、车辆解锁、奖励 |

### 6.1 `RunSession`：最深的局内规则模块

职责：一局从开始到结束的全部可测试规则，包括固定步进、距离、车道、车辆能力、技能条、交通、碰撞、擦车、碾压、道具、得分、续命资格和结束原因。

外部 interface 保持小：

```ts
type RunInput = {
  laneDelta: -1 | 0 | 1;
  abilityHeld: boolean;
};

type RunFrame = {
  snapshot: RunSnapshot;
  events: readonly RunEvent[];
};

interface RunSession {
  tick(dtMs: number, input: RunInput): RunFrame;
  resolveRevive(granted: boolean): RunFrame;
}

function createRun(options: {
  seed: string;
  carId: CarId;
  road: RoadPlan;
  mode: 'slice' | 'full';
}): RunSession;
```

Interface 不暴露内部计分器、碰撞集合或随机数发生器。测试和调用者只看 snapshot、events 和最终 result。

关键 invariant：

- 相同版本、seed、车辆与输入脚本必须得到相同路图和结果；
- `tick` 内使用固定时间步，外部大 `dt` 要截断，前后台回来不能瞬移或一次撞多车；
- 每个交通对象的擦车与碾压最多记一次；
- 结算后 `tick` 不再改变里程或分数；
- 等待续命时世界暂停；只有 `resolveRevive(true)` 恢复；
- 每局只能成功续命一次，跳过、失败或已使用都转结算；
- 续命恢复原进度、1 心和该车满保险杠，不重置分数、交通 seed 或里程；
- 飞行期间忽略路面交通碰撞，且只计路程；
- 压路机只有技能生效时才碾压并得分；普通碰撞不能冒充碾压；
- 换道与技能按住是同一帧可并存的两个输入维度。

### 6.2 `RoadFactory`：确定性大图模块

职责：用 seed 和版本化配置生成不可变 `RoadPlan`。一次生成描述，不持有 Cocos Node。

```ts
function createRoad(seed: string, config: RoadConfig): RoadPlan;
```

`RoadPlan` 至少包含：总距离、路段顺序、每段车道宽窄、主题标识、交通生成表、护盾/技能装置、天气和天色进度。第一版不生成分叉、高度或真实转弯物理。

同一种子必须稳定；不同种子必须在路段顺序、车流或道具中至少一项可观察地不同。若以后改变算法，提升 `roadVersion`，不要悄悄改变旧 seed 的含义。

### 6.3 `PlayerProgress`：局外进度模块

职责：校验/迁移存档，记录本局实际里程，计算解锁车和最佳单局分。存储 I/O 不在这个模块里。

```ts
function loadProfile(raw: unknown): PlayerProfile;
function applyRun(profile: PlayerProfile, result: RunResult): PlayerProfile;
```

存档至少包含：

```ts
type PlayerProfile = {
  schemaVersion: number;
  totalDistance: number;
  unlockedCarIds: CarId[];
  selectedCarId: CarId;
  bestScore: number;
};
```

规则：损坏或未知字段不得让游戏黑屏；回退为可玩的默认档并记录诊断。累计里程包含未完赛实际路程。解锁阈值按完整大图等价里程配置为约 2 / 6 / 15 局，不使用货币。

### 6.4 `GameDirector`：产品流程模块

职责：协调选车、开局、续命询问、结算、存档和好友榜显示。它不实现道路或碰撞规则，也不直接访问 `wx`。

唯一流程：

```text
boot -> select -> playing -> finish -----------------> result
                         \-> dead -> revive offer ----> result
                                      \-> ad complete -> playing
```

| 状态 | 进入条件 | 可接受输入 | 退出条件 | 必须行为 |
| --- | --- | --- | --- | --- |
| `boot` | 首场景加载 | 无玩家输入 | profile 校验/恢复完成 | 失败也生成默认可玩档，不白屏 |
| `select` | boot 或 result 重开 | 选车、发车 | 已选已解锁车并确认 | 未解锁车不能开局 |
| `playing` | 创建/恢复 `RunSession` | 换道、技能按住、系统暂停 | 完赛、死亡、生命周期暂停 | 每帧只有一份 snapshot；暂停清 active touch |
| `revive-offer` | 死亡且本局未使用续命 | 放弃、请求广告 | 放弃/失败到 result；完整观看回 playing | 世界不推进；异步结果只消费一次 |
| `result` | 完赛、放弃或不可续命 | 看细分/榜、重开 | 重开到 select | apply/save/submit 各最多一次；平台失败不阻塞重开 |
| `suspended` | 后台、锁屏、广告或榜覆盖 | 无玩法输入 | 明确回前台并清理输入 | 丢弃大 `dt`，不累计距离、不保留 held 状态 |

`suspended` 是覆盖状态，不是第五个 screen；恢复后回到此前的 `select`、`playing`、`revive-offer` 或 `result`。任何未知或重复异步事件都必须幂等忽略并留诊断日志。

广告加载失败、用户中途关闭或平台不支持，都必须留在可理解的产品路径上：提示不可续命后进入结算，不能卡死、白屏或免费发奖励。

### 6.5 `PlatformPort`：微信 seam

这是唯一允许平台能力穿过正式规则的 seam。生产有 `WeChatPlatformAdapter`，Creator 预览与自动测试有 `DevPlatformAdapter`。

```ts
interface PlatformPort {
  loadProfile(): Promise<unknown | null>;
  saveProfile(profile: PlayerProfile): Promise<void>;
  showRewardedRevive(): Promise<'completed' | 'skipped' | 'unavailable' | 'error'>;
  submitBestScore(score: number): Promise<void>;
  setFriendLeaderboardVisible(visible: boolean): void;
}
```

`DevPlatformAdapter` 用本地内存/浏览器存储，并能确定性模拟广告四种结果。`WeChatPlatformAdapter` 才允许调用 `wx`：本地存储、激励视频、用户托管数据、开放数据域消息和 shared canvas。

好友榜开放数据域可以按微信要求使用独立的轻量 Canvas2D renderer；它只画 shared canvas 排行榜，不承载游戏循环，也不改变「正式游戏由 Cocos 构建、不得手搓正式 `game.js`」的规则。

第一版好友榜默认上传**历史最高单局总分**，key 使用版本化名称（如 `best_score_v1`），避免低分覆盖高分。若 Hans 在好友榜切片前改成「最近一局」，先写回 `CONTEXT.md` 再改实现。

### 6.6 Cocos adapter 与场景

- `Main.scene` 作为唯一首场景；四个 screen prefab 按流程显隐，不为每个弹窗切场景；
- `MainController` 是 composition root，只负责创建模块、注入 adapter、绑定 screen；
- `RunInput` 用 touch id 分开跟踪「道路滑动」和「技能按住」，保证多点触控；
- `RunView` 只把 snapshot/events 映射为位置、动画、HUD 和飘字；
- 交通与道具在长局中使用 Cocos 对象池，回收时必须清理状态；
- Cocos 生命周期函数负责暂停/恢复，广告、后台和排行榜覆盖时停止 `RunSession.tick`；
- 所有 screen 适配安全区域，动态文本不得遮挡控制或相互重叠。

禁止全局可变单例、通用事件总线、依赖注入框架、为五辆车创建五套重复循环、把节点路径散落到 core、在 platform adapter 之外判断 `typeof wx`。

## 7. 可执行规则

### 7.1 路程与得分

- 内部世界距离与显示分数分开；跑完整图时路程分严格封顶 3000；
- 路程分按实际完成比例单调增加，不按车速倍率重复加成；
- 擦车事件每个交通 id 只发一次，+200；磨蹭或反复贴近不能刷分；
- 压路机技能期间每个有效目标 +500；同一目标不能同时算擦车和碾压；
- 完整大图终点 +1200；开发短段按占比计算并最低 +300；
- 结算总分必须等于四项之和，HUD 与结算使用同一份 result，不各算一遍；
- 加分事件当场标明「擦车 +200」「碾压 +500」「完赛 +1200」等来源。

### 7.2 车辆与碰撞

| 车 | 开局 | 保险杠 | 技能行为 | 得分限制 |
| --- | --- | --- | --- | --- |
| 跑车 | 默认解锁 | 1 | 按住氮加速 | 正常四项 |
| 小货车 | 约 2 局解锁 | 3 | 按住氮加速 | 正常四项 |
| 摩托车 | 约 6 局解锁 | 0 | 按住氮加速；碰撞宽度更窄 | 正常四项 |
| 飞行汽车 | 约 15 局解锁 | 1 | 按住飞行，无视交通 | 飞行期间只计路程 |
| 压路机 | 约 15 局解锁 | 3 | 按住碾压，破坏交通与护栏 | 技能目标 +500 |

每次普通有效碰撞只扣一格：有保险杠先扣一格；保险杠已空才把 1 心扣为 0。短暂受击保护只用于防止同一接触重复扣除，不形成新的生命系统。

速度倍率、碰撞宽度、车流密度和装置补充量属于可逆调参。实现 Agent 将初值集中在 `GameBalance.ts`，以「定位可感知且流程可验」为目标，不把调参散进脚本。若调参会改变上表的产品含义，再交 Hans 决定。

### 7.3 技能条与输入

- 满表容量对应约 4 秒连续消耗，开局约 2 秒；不强制把连续按住切成两段；
- 松手、耗尽、失去焦点、广告打开和进入结算都必须停止技能；
- 普通氮加速时才显示道路两侧品红氮光带；飞行和碾压不用氮光带；
- 滑动越过阈值只移动一条相邻车道；一次手势可继续滑到下一道，但不能越界；
- 技能按钮占用的 touch 不参与换道；道路区域的另一根手指仍能滑动；
- 暂停/恢复不得留下「技能永久按住」状态。

### 7.4 道路、天气与天色

- 玩家车保持在主镜头约 24% 画宽、80% 画高处；机位使用 `(376, 797)` 与 `k=2.244`；
- 路和两侧所有平行线共用机位 A，不另造透视；
- 玩家纵向相对固定，世界依距离推进；路段变化只改变画面和可用车道，不变成方向盘转向；
- 天色由完成距离驱动，0% 为傍晚、100% 为清晨；暂停不推进；
- 每局只抽一种天气滤镜；大风不推车，其余天气也不改碰撞；
- 功能切片可继续使用色块，但必须先让道路模型支持主题与天气字段，避免以后重写 seed 契约。

### 7.5 边界与失败规则

| 如果 | 精确结果 |
| --- | --- |
| 一帧 `dt` 因切后台异常增大 | 截断或丢弃超额时间，不补跑距离、生成与碰撞 |
| 同一帧同时到终点并发生致命碰撞 | 以距离穿越终点的时间顺序判定；完全同刻时完赛优先，规则写成测试固定下来 |
| 同一交通对象同时满足擦车与碾压 | 只记碾压 +500，不再记擦车 +200 |
| 交通对象与玩家持续重叠 | 一次接触最多造成一次扣除；分离并超过保护窗后才可再次命中 |
| 技能恰好在碰撞帧耗尽 | 用固定步开始时的 ability active 状态判定该步，避免帧率改变结果 |
| 触摸取消、窗口失焦、广告打开或切后台 | 清除技能按住与滑动 touch id；恢复后必须重新按/滑 |
| 存档为空、损坏、版本更高或缺字段 | 回到默认可玩档并记诊断；不推断或授予未解锁车 |
| 保存失败 | 本局结算仍可看和重开；显示非阻断诊断，不重复 apply 本局里程 |
| 广告 close 回调缺失、重复或结果不明 | 只有明确完整观看发一次续命；其余按失败进入结算 |
| 好友榜无权限、无好友、离线或超时 | 显示明确空/失败状态；本局总分、存档和重开保持可用 |
| 开放数据域收到未知/过期消息 | 忽略并记录，不改变当前排行或主域状态 |
| 对象池对象再次取出 | 必须重置 id、lane、得分标记、碰撞状态、sprite、监听和 active 状态 |
| 结算后仍收到输入/广告/榜回调 | 幂等忽略，不改结果、不重复里程、不重复上传分数 |

### 7.6 `GameBalance` 控制清单

下表把 Hans 已锁的值与可逆调参分开。初值是实现起点，不是新增产品承诺；每次改动必须记录「旧值、理由、证据、影响车辆」。超出安全范围或改变车辆定位时走 Gate 3。

| 参数 | 类型 | 初值/契约 | 实现安全范围 | 过低/过高风险 |
| --- | --- | --- | --- | --- |
| 完整路程分 | contract | 3000 | 锁定 | 改动会破坏分值 A |
| 擦车/碾压/完赛 | contract | 200 / 500 / 1200 | 锁定 | 改动会改变技巧占比 |
| 技能容量/开局量 | contract | 约 4s / 约 2s | 3.6–4.4s / 45%–55% | 太短无策略；太长能力常驻 |
| 跑车完整局长 | gate | 满速约 5 分钟 | 4.5–5.5 分钟 | 太短无旅程；太长偏离短局 |
| 基础速度 | feel | 由 5 分钟目标反推 | 基线 0.9–1.1 倍 | 影响局长和反应窗口 |
| 普通氮倍率 | feel | 实测定 | 1.25–1.80 | 太低无感；太高来不及读路 |
| 滑动阈值 | feel | 以 720×1280 设计坐标记录 | 32–96 px 等价 | 太低误触；太高换道迟钝 |
| 受击保护 | feel | 实测定 | 0.35–1.00s | 太低连扣；太高可穿车 |
| 摩托碰撞宽度倍率 | feel | 实测定 | 跑车的 0.55–0.80 | 太宽无定位；太窄失去风险 |
| 跑车/飞车保险杠 | contract | 1 | 锁定 | 改动破坏车辆契约 |
| 货车/压路机保险杠 | contract | 3 | 锁定 | 改动破坏耐撞线 |
| 摩托保险杠 | contract | 0 | 锁定 | 改动破坏高风险定位 |
| 车流密度倍率 | curve | 路段模板实测定 | 0.7–1.3 | 太低无技巧；太高不可读 |
| 装置间隔 | curve | 五分钟局实测定 | 相邻至少留一段可反应距离 | 太密技能常驻；太疏无法验证能力 |
| 里程解锁阈值 | gate | 约 2 / 6 / 15 完整局等价 | 仅在不改变节奏档位内微调 | 太快无成长；太慢看不到新取舍 |

所有距离、速度、计时和碰撞尺寸使用统一单位并在 `GameBalance.ts` 注明。热路径不得读取松散 JSON、场景节点或字符串 key 来决定规则。

## 8. 开发顺序与每刀验收

### S0：建立可恢复工程基线

**目的**：让后续实现有可定位 base commit，不让正式代码继续堆在无提交工程上。

工作：

- 分别检查契约仓和 Cocos 工程的 `git status`，保留已有改动；
- 清理不应提交的 `.DS_Store`、`library/`、`temp/`、`local/`、`build/` 等生成物规则；补忽略 `project.private.config.json`、上传私钥和本地证据缓存；
- 复核 2026-08-18 已建立的根级 AGENTS/README、`docs/architecture.md` 与 `tests/core/` 边界；目录治理本身不算测试基线或玩法进度；
- 确认 Cocos 的 `assets/`、`settings/`、`build-templates/`、`.meta`、`package.json` 可恢复；
- 将 `build-templates/wechatgame/game.ejs` 与 Creator 3.8.6 默认模板做 diff；没有明确复现证据的方向/DPR 修补移除，需要保留则记录原因并验证触摸坐标；
- 为当前已验证状态建立 Cocos 基线提交，再从它创建正式实现分支；
- 在 Cocos 根建立最小测试脚本：纯 core typecheck 与行为测试；推荐 `vitest` + TypeScript，提交 lockfile；
- 建立独立 `tsconfig.core.json`，只覆盖 core 与测试，不依赖 Creator 运行后才出现的 `temp/tsconfig.cocos.json`；
- 记录 Creator 3.8.6、Cocos MCP 1.7.9、720×1280 和当前微信空包证据；
- 在正式 seam 落地前按 §5.6 做一次 `game-architect` 架构参考核对；把结论写入本刀任务卡或 ADR，不把调用本身当作 S0 通过证据；
- 区分并验证两套 MCP：Cocos MCP 指向工程根；微信小游戏助手首次直接尝试 `run_game` 指向含 `game.js` 的 `build/wechatgame/`，不可用时才按其 skill 做检测/用户级配置；
- 对基线导出包执行助手 `run_game`，主动打开返回的预览，约 2 秒后 `get_logs`，无 error 后留一张截图；这只证明包能启动，不把第一刀升级成正式玩法证据。

验收证据：两个仓库状态、Cocos base commit、模板审计结论、测试命令能空跑、Creator 能打开当前场景、导出包助手日志无 error 与截图。S0 不改变产品行为。

### S1：正式第二刀——选车、短段、四项本地结算

**目的**：用正式模块替换 `MvpLoop`，产生第一条可继续扩展的产品纵切。

包含：

- 正式 `Main.scene`、Select / Run / Result screen；
- `RunSession`、开发用短 `RoadPlan`、`GameDirector`、`DevPlatformAdapter`；
- 仅跑车可用；其他车可不出现或明确显示锁定，不实现假能力；
- 三车道、滑动换道、按住氮、同时氮换道；
- 交通、碰撞、路程/擦车、短段完赛、本地四项结算；碾压为 0；
- 继续使用清晰色块，不接美术、广告、好友榜、里程解锁。

验收：

- Creator 预览能从选车进入短段，完成和撞毁都能到结算并重开；
- 按住氮时另一根手指能左右换道；
- 路程、擦车与完赛按 §7.1 计算，结算总分严格相加；
- 自动测试覆盖确定性、计分一次性、两次碰撞掉命和状态终止；
- 场景已不挂 `MvpLoop`，正式行为通过后删除旧脚本；
- Creator 控制台无 error，场景引用校验通过；
- 重建微信包后，用助手 `run_game` + `get_logs` 证明生成包启动无 error，并留一组 720×1280 选车/游玩/结算截图；
- 微信开发者工具重新导入该包并跑通主路径，证明正式架构仍可导出。

**S1 是 Hans 的第一个正式验收点。未通过不进入 S2。**

### S2：完整种子大图与局内规则

**目的**：把短段扩为可重复、可复现、约五分钟的完整一局，先用跑车证明 AC-play。

包含：

- 版本化 seed、路段模板、路宽变化、主题标识、交通和道具生成；
- 在实现 `RoadFactory` 前按 §5.6 读取 PCG 参考，优先验证模板组装、seed 重放、连通性和可玩性，不提前引入通用 PCG 框架；
- 护盾与技能装置；护盾补满，技能装置补当前表；
- 完整路程 3000、擦车、完赛 1200；
- 每局一种天气字段，天色随路程傍晚到清晨；
- 长局对象池、暂停/恢复、终点和中途失败；
- 调试入口可固定 seed 和使用加速验证，但生产入口不可显示开发控制。

验收：

- 同 seed + 同输入脚本结果一致；不同 seed 有可观察差异；
- 正常最高速完整局约 5 分钟，速度更高的车以后可更快完成，不把局长写成倒计时；
- 路段始终是必经路线，无分叉、高度或真转向；
- 连续运行三局无残留交通、重复监听、分数串局或明显内存持续增长；
- 后台/前台切换不跳距离、不自动撞车、技能不粘住；
- Creator 预览、短调试模式和一局完整模式均通过。

### S3：五车、里程与本地持久化

**目的**：完成 AC-cars，让局外循环成立。

包含：

- 五车目录、锁定/解锁/选择状态；
- 三种保险杠厚度、摩托窄碰撞；
- 普通氮、飞行和碾压三种技能效果；
- 完成飞行只计路程、压路机碾车/护栏规则；
- `PlayerProgress`、schema 迁移、本地存储；
- 约 2 / 6 / 15 完整局等价里程解锁；中途里程照记；
- 结算后保存，启动时恢复档案。

验收：

- 每辆车的定位不用看代码即可从一次短测试感知；
- 保险杠扣除顺序、飞行免碰、碾压计分均有行为测试；
- 里程临界值前后解锁准确，退出重开仍保留；
- 损坏、空或旧版本存档能恢复为可玩默认档，不白屏；
- 未解锁车不能通过 UI 或存档字段直接开局；
- Creator 预览用 Dev adapter 走完五车测试矩阵。

### S4：一次激励视频续命

**目的**：完成 IAA 的唯一广告位，不改变局外成长。

包含：

- 死亡后的 Revive screen 与一次性资格；
- Dev adapter 的 completed / skipped / unavailable / error 四路；
- WeChat 激励视频 adapter，广告对象生命周期、加载/重试和关闭结果处理；
- 广告期间暂停，返回后清理输入；完整观看才调用 `resolveRevive(true)`；
- 续命恢复 1 心 + 满保险杠，保留进度和分数；一局第二次死亡直接结算。

验收：

- 四种 Dev 结果自动/手动测试均不锁死流程；
- 中途关闭、加载失败、平台不支持不发奖励；
- 完整观看只发一次奖励，重复回调不能二次续命；
- 正式 AppID 与广告位可用后，在微信开发者工具和真机各完整看一次；
- 真实验证可由助手 `real_device_preview` 生成二维码；成功后禁止再调用 `run_game` 或刷新预览，直到二维码使用完成；
- 广告返回后距离、技能与触摸状态正确；
- 不加入横幅、插屏或广告换永久成长。

若账号尚不能创建广告位，S4 的 Dev adapter 与生产代码可完成，但状态只能记为「待真实广告验证」，不能宣称 AC-iaa 通过。

### S5：结算好友榜与开放数据域

**目的**：完成第一版唯一社交能力。

包含：

- 结算后比较并上传 `best_score_v1`；
- 在 `build-templates/wechatgame/openDataContext/` 维护独立开放数据域源码，读取好友托管分数、解析、稳定排序和绘制；不直接改被 Git 忽略的构建产物；
- 主域通过消息控制排行榜刷新/显隐，用 shared canvas 显示；
- 当前玩家、本局分、历史最佳、无好友、无权限、离线和读取失败状态；
- 好友榜只影响展示，不控制车辆解锁或发奖励。

验收：

- 低分局不会覆盖历史高分；
- 开放数据域是独立执行环境，主域不直接读取好友关系数据；
- 至少两个真实微信账号产生可核对顺序；同分排序稳定；
- 无好友/未授权/离线时结算仍可完成并可重开；
- 不调用旧 Netlify leaderboard，不出现全球榜入口；
- 微信开发者工具和真机都验证 shared canvas 尺寸、清晰度与关闭后的资源状态；
- 刷新 S5 微信包后先用助手检查启动日志；关系链结果仍必须在开发者工具与真实微信账号验证，浏览器兼容层不能代替。

若真实好友关系链条件不足，先保留 Dev adapter 截图，但不能把模拟数据当最终 AC-iaa 证据。

### S6：正式视觉与触屏完成度

**进入条件**：Hans 明确解除「出图暂停」并批准可用资产。未解除时，S1–S5 继续用统一色块，不自行生成或认可正式局内图。

包含：

- 按 art bible 的图层栈接入天空、远景、中景、近景、道路、氮光带、车、特效、HUD；
- 机位 A、三车道、车位、路边推近、接地、天气滤镜和傍晚到清晨；
- 菜单/选车/续命/结算可用 CRT 表面，开车画面保持平直；
- 五车图、碰撞/擦车/碾压/飞行/道具/加分的即时反馈；
- 安全区域、多尺寸手机、文字可读和拇指可达性。

音效尚未写入第一版产品契约，不作为本方案默认阻断项。若 Hans 在 S6 前批准音频范围和资产，可增加行驶、氮、碰撞、拾取、飞行、碾压、按钮和结算反馈；实现使用 Cocos/微信兼容音频能力，不沿用网页 AudioContext。

验收：

- 在契约仓运行 `python3 assets/minigame/previews/_check_perspective.py`，机位检查全部通过；
- 人工抽查与道路平行的线落在消失点 ±20px；
- 氮光带只在普通氮加速出现；CRT 不进入局内；
- 所有正式资产可追到批准来源，未把旧 H5 图当正式资产；
- 720×1280、窄屏和长屏均无文本/按钮重叠；
- 真机上帧率和触摸反馈不因特效明显退化。

### S7：微信发布候选与上架证据

**目的**：完成 AC-ship，形成可交给 Hans 验收和截图的候选包。

包含：

- 清除开发入口、模拟广告、测试榜和未使用资源；
- Cocos 构建目标 Portrait，使用真夜中道路 AppID；
- 检查主包体积；若超过当前微信限制，先裁剪未使用引擎/资源，再决定分包或远程资源；禁止远程下载脚本；
- 微信开发者工具完整编译，模拟器与真机 smoke；
- 名称、头像、类目、适龄、玩法和备案本地稿一致；
- 按 `wechat-beian-copy.md` 准备主界面、游玩、技巧得分、技能、续命和好友榜截图。
- 对最终导出包执行助手 `run_game`、`get_logs` 和 `capture_screenshot`；再用 `real_device_preview` 做获授权的真机 smoke。`publish` 只有 Hans 明确给出版本号、描述并授权上传时才可调用，成功后禁止刷新二维码页面。

最终验收矩阵：

| 场景 | 必须证明 |
| --- | --- |
| 新号 | 只有跑车可用，可正常开局 |
| 完整跑车局 | 约五分钟、四项分、傍晚到清晨、结算 |
| 技巧 | 擦车一次 +200，重复不刷；压路机技能每车 +500 |
| 五车 | 保险杠、摩托宽度、飞行、碾压定位正确 |
| 里程 | 中途结束计入；2/6/15 局等价阈值解锁；重启保留 |
| 续命 | 完整广告恢复满状态且仅一次；跳过/失败不奖励 |
| 好友榜 | 高分上传、真实好友顺序、异常时可降级结算 |
| 生命周期 | 来电式切后台、锁屏、广告、回前台均不跳帧或粘输入 |
| 兼容 | 开发者工具 + 至少一台真实手机，竖屏安全区域正常 |
| 包 | 无 runtime error，无旧 H5/Netlify 依赖，无手写正式 `game.js` |

S7 完成后状态是 `ready_for_review`，不是自动 `accepted` 或已发布。Hans 验收后才能更新为 accepted；上传审核、备案提交和正式发布仍要单独授权。

## 9. 测试与验证流程

### 9.1 每次代码改动的最小反馈环

S0 建立脚本后，Cocos 工程根运行：

```bash
npm ci
npm run test
npm run typecheck:core
git diff --check
```

再检查 core 没有穿透到引擎或微信：

```bash
rg -n "from ['\"]cc['\"]|\bwx\." assets/scripts/core
```

该 `rg` 应无输出。Cocos 脚本的完整编译仍以 Creator 控制台为准，不用 core typecheck 冒充引擎构建。

### 9.2 core 必测行为

- 同 seed、同输入得到同 RoadPlan、同分数和同结束原因；
- 大 `dt` 截断，暂停期间不推进；
- 三车道不越界，同时技能换道成立；
- 路程分封顶、擦车一次、碾压一次、完赛分和总分；
- 各车保险杠顺序与摩托无杠；
- 飞行免交通且不拿技巧分；压路机技能/非技能两条路径；
- 道具补满保险杠、技能条不超过上限；
- 续命四路、一次性、原地满状态、第二次死亡；
- 中途里程、解锁临界值、最佳分、存档迁移与损坏档；
- 结算后输入不再改变结果。

测试断言外部可观察结果，不断言私有字段、节点数量或内部函数调用。

### 9.3 Creator 验证

每一刀至少执行：

1. 确认工程与版本、MCP ready、当前场景和 720×1280；
2. 用 Cocos MCP 修改/创建 `.scene`、`.prefab`、`.anim`、`.meta` 相关资产；禁止文本手改；
3. 保存并执行 `cocos_scene.validate_scene` 查断裂引用；
4. 执行 `cocos_validate` 检查布局、引用和层级；
5. Creator 预览完整走一次本刀主路径与一条失败路径；
6. 检查控制台无 error、重复监听或未释放对象警告；
7. 截取固定 720×1280 证据图，动态 UI 不得改动布局尺寸。

### 9.4 微信小游戏助手包级验证

助手只接 Creator 已导出的、含 `game.js` 的 `/Users/hant/工作台/projects/creation/midnightroad/build/wechatgame/`。不要把 Cocos 工程根传给它，也不要把它当构建器。

每次刷新候选微信包后执行：

1. `run_game(workspacePath=build/wechatgame)` 启动或幂等刷新预览；
2. 主动打开返回 URL：优先当前 host 内置浏览器；VSCode 系按 skill 生成的内置 Simple Browser 配置；其他环境才用系统浏览器；
3. 等约 2 秒后 `get_logs`，至少过滤 `error|warn|Uncaught|TypeError|ReferenceError`；
4. 有错误就修 Cocos 源或构建配置，重新由 Creator 构建，再回到第 1 步；同一根因超过 5 次或累计修复超过 15 次时停止并报告；
5. 无 error 后按本刀主路径操作，需要视觉证据时用 `capture_screenshot`，记录包对应的 Cocos commit。

`run_game` 的浏览器兼容层只做快速包级反馈，不能证明广告、好友关系链、真机性能、包体审核或微信生命周期。`real_device_preview` 和 `publish` 缺 AppID/上传私钥时必须停下让 Hans 配置，不用测试号或他人凭据替代。二维码生成或上传成功后不得再 `run_game`/刷新页面。上传是外部状态变更，始终需要 Hans 对该版本的单独授权。

### 9.5 微信开发者工具与真机验证

- S1 完成后重建一次微信包，证明正式架构仍能出包；
- S4、S5 必须分别用正式 AppID 验真实广告和开放数据域；
- S7 做完整构建，不以 MCP `editor.build` 或 web-mobile 预览替代「发布到微信小游戏」；
- 导入含 `project.config.json` 的 `build/wechatgame/` 层，不导入 Creator 根；
- 检查 Portrait、基础库、启动、触摸、存储、前后台、广告、排行榜和无网络路径；
- 真机至少连续跑三局，包含一次续命与一次放弃续命；
- 构建产物是证据，不默认提交进 Cocos Git。

官方实现细节在接入当刀重新核对：

- Cocos 3.8 发布微信小游戏：`https://docs.cocos.com/creator/3.8/manual/zh/editor/publish/publish-wechatgame.html`
- 微信好友榜：`https://developers.weixin.qq.com/minigame/dev/guide/open-ability/ranklist.html`
- 本仓平台笔记：`wechat-minigame-platform.md`、`cocos-publish-wechatgame.md`

### 9.6 测试证据格式

每一刀在契约仓新增或更新 `docs/evidence/S<n>.md`，只提交小型日志摘录、截图索引和结果，不提交整个 `build/`。每条证据必须有：

| 字段 | 要求 |
| --- | --- |
| Evidence ID | `S<n>-CORE/CREATOR/PKG/DEVTOOLS/DEVICE-<nn>` |
| 版本 | Cocos branch、base commit、result commit；契约 commit |
| 环境 | Creator/开发者工具/微信版本、设备型号、基础库、MCP 版本 |
| 前置 | seed、车辆、profile、网络、AppID 类型；敏感值只记是否配置 |
| 步骤与预期 | 可由下一位 Agent 重放，不写“试了一下” |
| 实际与结果 | PASS / FAIL / BLOCKED；原始错误和时间戳 |
| Artifact | 截图/日志/录屏相对路径或稳定本机路径及内容哈希 |
| 已知限制 | 模拟能力、账号条件、未测分支和唯一下一步 |

模拟广告、模拟好友和浏览器截图必须显式标 `DEV`，不能与 `DEVICE` 证据混用。FAIL 不删除；修复后新增证据并链接旧 ID。

### 9.7 需求追溯与关键验收场景

| ID | Given / When / Then | 系统 | 首次通过 | 最终证据 |
| --- | --- | --- | --- | --- |
| PLAY-01 | GIVEN 新号，WHEN 选跑车并发车，THEN 能换道、用氮、完成或折损并结算 | Director / RunSession / Cocos | S1 | Creator + PKG + DEVTOOLS |
| SCORE-01 | GIVEN 同一交通 id，WHEN 擦车多帧，THEN 只加一次 200 | RunSession | S1 | CORE + Creator |
| SCORE-02 | GIVEN 压路机技能 active，WHEN 命中目标，THEN 只加碾压 500；非技能不加 | RunSession | S3 | CORE + Creator + DEVICE |
| ROAD-01 | GIVEN 同版本 seed 与输入，WHEN 重放一局，THEN 路图、事件和结果一致 | RoadFactory / RunSession | S2 | CORE |
| CAR-01 | GIVEN 五车均解锁，WHEN 各跑短测，THEN 保险杠、车宽与能力符合 §7.2 | Config / RunSession | S3 | CORE + Creator |
| PROG-01 | GIVEN 临界值前 profile，WHEN 应用本局实际里程，THEN 在 2/6/15 局等价阈值准确解锁并持久化 | PlayerProgress / Platform | S3 | CORE + Creator + DEVICE |
| REVIVE-01 | GIVEN 首次死亡，WHEN 完整看广告，THEN 原地恢复 1 心和满杠且分数/里程不重置 | Director / Platform / RunSession | S4 | CORE + DEVTOOLS + DEVICE |
| REVIVE-02 | GIVEN 跳过/失败/第二次死亡，WHEN 处理结果，THEN 不奖励并可到结算 | Director / Platform | S4 | CORE + DEVICE |
| RANK-01 | GIVEN 两个真实好友有历史最佳，WHEN 打开结算榜，THEN 高分不被低分覆盖、排序可核对 | Platform / open-data | S5 | DEVTOOLS + DEVICE |
| LIFE-01 | GIVEN 正在按技能，WHEN 后台/广告后返回，THEN 不跳距离、不自动撞车、技能不粘住 | Director / Cocos / Platform | S4 | CORE + DEVICE |
| SHIP-01 | GIVEN S0–S7 结果 commit，WHEN 构建候选，THEN Portrait 可启动、无 runtime error、无旧 H5/测试入口 | 全系统 | S7 | PKG + DEVTOOLS + DEVICE |

第一版 AC 映射：`AC-play = PLAY/SCORE/ROAD`，`AC-cars = CAR/PROG`，`AC-iaa = REVIVE/RANK`，`AC-ship = LIFE/SHIP`。任何 AC 只有模拟证据时状态最多为 `provisional`。

## 10. 代码与产品审查标准

### 10.1 Spec 审查

- 所有行为能指向 `CONTEXT.md` 或本方案；
- 没有重新引入圈、分叉、真转向、全球榜、内购、连击或强制广告；
- 分值、保险杠、里程、续命和五车定位逐项匹配；
- 对未锁的数值只做集中可逆调参，不伪装成 Hans 已确认决定。

### 10.2 模块审查

- `RunSession` interface 小，复杂规则留在内部；删除该模块会让复杂度散回调用者，说明它有足够 depth；
- core 不依赖 Cocos / `wx`，测试通过同一 interface；
- `PlatformPort` 确实有 Dev 与 WeChat 两个 adapter；
- 没有只有一个实现的假 port、只转发一行的 manager、重复 DTO 映射或通用事件总线；
- Cocos controller 不重复计算规则，view 不持有第二份权威分数/生命；
- 配置集中，五辆车共享循环，用数据和能力分支表达差异。

### 10.3 可靠性审查

- 异步广告回调幂等；错误、跳过、超时都有终点；
- 存档有 schemaVersion、校验和默认值；写失败不阻塞本局结算；
- 前后台、广告、排行榜打开时暂停，返回时清理所有 active touch；
- seed 不使用裸 `Math.random()`；生产结果能记录 seed 供复现；
- 对象池回收清理 id、得分标记、lane、sprite 和监听；
- 结算只发生一次，上传失败不会重复累计里程或重复发分；
- 移动、生成、技能消耗和动画都基于受控 `dt`，不把每帧固定增量写死；
- `update` 热路径避免临时数组、字符串和闭包分配，不在每帧查找节点或组件；
- `onDisable` / `onDestroy` 对称解绑输入、生命周期、广告和开放数据域监听；
- 所有魔法数归 `GameBalance` 或版本化道路配置，代码注释解释边界原因而非复述语句。

### 10.4 Cocos / 资产审查

- `.scene` / `.prefab` / `.anim` / `.meta` 只通过 Creator / Cocos MCP 改；
- 使用 `db://assets/...` 和真实 UUID 查询，不猜 UUID；
- `.meta` 与源资产一起提交，场景无断裂引用；
- 不把 `library/`、`temp/`、`local/`、构建缓存或 token 提交；
- AppID 可记录，token、secret、广告后台凭据不得入仓；
- `project.private.config.json`、上传私钥路径、助手预览配置和设备日志中的身份信息不得入仓；
- 不改构建生成的 `game.js` 实现正式逻辑。

### 10.5 交付审查

每刀交付说明必须回答：

- 玩家现在新增能做什么；
- 对应哪个 AC / 本方案哪一刀；
- 自动测试、Creator、微信工具、真机各跑了什么；
- 当前分支、base commit、结果 commit 与未提交改动；
- 已知限制和唯一下一步；
- 哪些结论仍需 Hans 接受或外部账号验证。

没有 commit/branch 或可定位 artifact 的本地改动不算跨 Agent 交接。

### 10.6 四视角审查顺序

每刀由同一 Owner 自审，但要依次切换视角，不能只报“代码能跑”：

| 视角 | 先问什么 | 阻断问题 |
| --- | --- | --- |
| Game / Systems Design | 玩家幻想、规则、公式、边界和车辆取舍是否仍匹配 | 契约漂移、技巧不可读、调参改变定位 |
| Technical Director | 依赖方向、可测试性、热路径与平台 seam 是否清楚 | core 穿透 `cc`/`wx`、重复权威状态、上帝类 |
| UX / Accessibility | 首局是否无需说明、触控是否可达、反馈是否文字与状态都可读 | 按钮遮挡、只靠颜色、双指互斥、异常无出口 |
| QA / Release | 证据是否可复现，模拟和真实平台是否分开 | 没 commit、没日志、用 DEV 冒充 DEVICE、未授权上传 |

发现阻断问题先修当前纵切并重跑对应证据，不通过新增文档或降低验收标准绕过。

## 11. 实现 Agent 的开工卡

每次新会话按顺序读取：

1. 根 `AGENTS.md`；
2. `PROJECT.md` Startup Summary 与 Next Step；
3. `CONTEXT.md` 全文；
4. 本方案当前切片；
5. ADR 0001 / 0002、`cocos-mcp-pro.md`；
6. Cocos 工程 `AGENTS.md` 与 `docs/architecture.md`；
7. 当前 Cocos 代码、场景层级、两个仓库 `git status`。

只有当前任务命中 §5.6 的节点时，才读取 `game-architect` 对应参考，并在任务卡中记录“参考了什么、改变了什么、为什么没有新增抽象”。

任务卡必须写明：当前切片、base commit、可写仓库/文件、禁止事项、验收项、验证命令、预算和停止条件。默认一个 Owner 在一个 Cocos worktree 完成实现、自测、自审和交付；同一 worktree 同时只允许一个写入者。

实现过程中：

1. 先写或更新本刀行为测试；
2. 形成最短可运行纵切；
3. 通过 core 测试；
4. 用 MCP 搭/改场景并校验；
5. Creator 预览主路径与失败路径；
6. 到指定切片再构建微信包，不每个小改动都重打包；
7. 按 §10 自审；
8. 提交 Cocos 结果，再更新契约仓的真实进度。

不要创建按「规则/UI/测试」水平拆开的并行任务；一个切片应由一个 Owner 端到端交付。只有存在两个无共享写入且各自可演示的纵切，并已明确资源预算时，才考虑多 Agent。

## 12. 风险、决策门与停止条件

### 风险登记

| ID | 风险 | 概率 / 影响 | 触发信号 | 缓解与退出条件 | Owner |
| --- | --- | --- | --- | --- | --- |
| R1 | 当前验证单文件被继续堆成正式架构 | 中 / 高 | S1 继续给 `MvpLoop` 加平台或五车字段 | S1 先建 core 纵切；正式场景脱离后删除旧脚本 | 技术 Owner |
| R2 | 自定义 `game.ejs` 破坏方向、DPR 或触摸坐标 | 中 / 高 | Android/iOS 画布或触摸不一致 | S0 diff 默认模板；无证据移除；两端截图/触摸 smoke | 技术 Owner |
| R3 | 五分钟长局掉帧、GC 或状态残留 | 中 / 高 | 三局后内存持续涨、帧抖、重复监听 | 对象池、热路径审查、三局 soak；未达标不进 S3 | Gameplay / QA |
| R4 | 多点触控与生命周期互相污染 | 中 / 高 | 按氮换道失败、回前台仍 held | touch id 分工、cancel/blur 清理、真机 LIFE-01 | UI / QA |
| R5 | 广告账号/广告位/私钥不可用 | 中 / 高 | Dev 四路通过但真实广告无法创建或扫码 | 完成 adapter，标 provisional；Gate 4 前不宣称 AC-iaa | Hans / Platform |
| R6 | 真实好友关系不足或开放数据域显示不清 | 中 / 高 | 只有模拟榜或无法凑两个账号 | S5 提前约测试账号；SubContextView 尺寸/FPS 实测 | Hans / Platform |
| R7 | 正式美术未批准导致 S6 阻塞 | 高 / 中 | 出图暂停未解除 | S1–S5 保持统一色块；Gate 6 决定资产，不偷用预览 | Hans / Art |
| R8 | 主包超过当前平台限制 | 中 / 高 | 候选包接近/超过 4MB | 每刀记录包体；先裁引擎/未用资源，再评估分包/远程资源；不远程下脚本 | Technical / QA |
| R9 | 契约仓与 Cocos 仓提交失配 | 中 / 高 | 证据找不到对应代码或独有未提交改动 | 每条证据双 commit；一 worktree 一 writer；交接前状态清点 | Producer / Owner |
| R10 | skill/MCP 安装被误当成产品验证 | 中 / 中 | 没有 `get_logs`/真机证据却标 PASS | 严格按 §9 证据分层；工具缺失标 BLOCKED，不用 shell 假冒 MCP | QA Owner |

每个切片开始时复核本表；概率、影响或 Owner 变化写回证据记录。风险不能通过新增无消费者抽象或模拟截图关闭。

### Hans 决策门

- **Gate 1（已关闭）**：Hans 2026-08-18 接受本方案并授权 S0/S1；
- **Gate 2（S1 后）**：接受正式第二刀的结构与手感，才扩五分钟长局；
- **Gate 3（S3 调参）**：若车速/宽度等调参改变车辆定位，由 Hans 定；
- **Gate 4（S4）**：Hans 提供或确认正式 AppID、广告位与真实广告验证时机；
- **Gate 5（S5）**：默认好友榜为历史最高单局分；若要改语义，先由 Hans 确认；
- **Gate 6（S6）**：Hans 明确解除出图暂停并接受资产；
- **Gate 7（S7）**：Hans 验收候选包；上传、备案、审核、发布分别授权。

### Agent 必须停止并报告

- 目标、范围、验收与 `CONTEXT.md` 出现实质冲突；
- 需要手改 Cocos 序列化资产才能继续，且 MCP/Creator 无法完成；
- 当前 worktree 有来源不明且与本刀重叠的修改，无法安全保留；
- 广告或开放数据域被账号权限/平台条件连续阻塞，Dev adapter 已证明逻辑但真实验证不可得；
- 包体、性能或平台限制要求删除已锁功能、引入后端/付费资源或改变发布范围；
- 美术仍暂停却需要把未批准预览当正式资产；
- 连续两个检查点没有新的可运行行为或证据。

阻塞时保留已通过的最小纵切、原始错误与复现步骤；不要用新增架构、文档或模拟截图掩盖真实阻塞。

## 13. 第一版完成定义

只有以下全部成立，第一版才可交 Hans 最终验收：

- AC-play、AC-cars、AC-iaa、AC-ship 全部有对应运行证据；
- S0–S7 的验收项完成，或明确经 Hans 删除/改写；
- core 行为测试与 typecheck 通过；
- Creator 控制台、场景引用与布局校验通过；
- 最终导出包通过助手 `run_game` / `get_logs` / 截图检查，且能追到 Cocos result commit；
- 微信开发者工具和真机跑通完整局、续命、好友榜、重启存档；
- 正式包无旧 H5、Netlify 全球榜、模拟 adapter、测试入口或手写运行入口；
- 备案截图内容与名称、类目、适龄和玩法稿一致；
- 两个仓库的结果均可由 commit/branch 定位，交接时无未说明的独有改动；
- `docs/evidence/` 的 AC 追溯均为 PASS；真实平台要求没有被 DEV 模拟证据冒充；
- Hans 明确接受交付。

接受仍不等于上线授权。正式提交和发布另行确认。
