# 真夜中道路

**Type**: 微信小游戏（个人 IAA）
**Status**: in_progress
**Created / Last Updated**: 2026-08-18
**协作等级 / 角色**: L2 执行者（Gate 2–3 已过；Gate 4 广告延后；下一项 Gate 5）
**Alignment**: aligned
**Feishu**: 未发布

## Startup Summary

**Project Snapshot**: Gate 2–3 已过。AppID `wxcce206285c95068b` 已收到。流量主开不了，第一版无广告、无续命（ADR 0006）。画面仍是色块。Gate 5–6 与 `run_game` 未过。

**Next Step**: **Gate 5：好友榜**。默认历史最高单局分；两个微信号对顺序。未确认前不上传。

## Objective

上架微信小游戏 **真夜中道路**。第一版走个人主体、IAA。核心循环是种子大图短局得分，不以 Demo 的一命闪避为契约，也不用圈。

## Scope

第一版产品边界以 `CONTEXT.md` 为准。文件树见 [TREE.md](TREE.md)。

做：个人主体（声明不开虚拟支付）、动作/跑酷、12+、种子大图约 5 分钟、三车道跟手横移、双击加速、晚躲擦车、擦车连击、五车+里程、分值 A、结算好友榜、Cocos 导出微信包。第一版无广告续命。

不做（第一版）：内购、全球榜、幻影陪跑、手写正式包 `game.js`、把 Demo 当提审包、局内精细出图（暂停）。

H5 Demo 已归档（`archive/h5-demo/`）并下线。Netlify 站保留，只发 `archive/offline/`。以后有新 Demo 再开。

## Acceptance Criteria

本轮（访谈 + 框架）已满足：

- AC-align：Hans 确认复述即第一版；词在 `CONTEXT.md`，决定在 [ADR 0001](docs/adr/0001-first-version-loop.md)
- AC-pipe：空场景微信包能编（第一刀 A）；Creator 预览里色块循环能选车/开/结算（[slice-b](docs/cocos-slice-b-mvp.md)）；MCP 能操作 `midnightroad`

第一版上架验收（**尚未做**，按 [完整开发方案](docs/plan.md) S1–S7 推进）：

- AC-play：能选车、开种子大图、当场看到四项分、可本地结算
- AC-cars：五车定位与里程节奏符合契约
- AC-iaa：第一版无广告；结算好友榜；无内购。激励续命等流量主开通（Gate 4 延后）
- AC-ship：Cocos 微信包在开发者工具/真机可玩，名称与备案稿一致

正式第二刀范围仍是「选车 + 一段三车道 + 本地结算」，按方案 S1 实施；广告和好友榜不进入这一刀。

## Acceptance Review

- Mode: sequential
- Current Item: Gate-5
- Batch Authorization: 2026-08-18 授权先独立做完 S1–S5；2026-08-18 收工时 Hans 指定醒来后逐项确认下列 6 项
- Items:
  - Gate-1-plan: accepted
    - Evidence: [docs/plan.md](docs/plan.md)
    - Hans Confirmation: 2026-08-18「接受，授权开工」
  - Gate-2 手感: accepted
    - Evidence: 契约 ADR 0003–0005；Cocos 已改；Hans 短段试玩
    - Hans Confirmation: 2026-08-18「可以 手感对了」
  - Gate-3 五车定位: accepted
    - Evidence: 飞/碾手势正常；摩托能挂虚线穿缝，跑车挂虚线会撞。色块上看不出宽窄外形，属预期
    - Hans Confirmation: 2026-08-18「可以 这两条对了」
  - Gate-4 广告: deferred
    - Evidence: AppID `wxcce206285c95068b`；流量主未开（UV 不足 500）；第一版无广告见 [ADR 0006](docs/adr/0006-no-ads-first-ship.md)
    - Hans Confirmation: 2026-08-18「第一版可以先做无广告版本」
  - Gate-5 好友榜: pending
    - Evidence: 默认 `best_score_v1` 历史最高；openDataContext 源码已就位；无双号实榜
    - Hans Confirmation: none — 确认「历史最高」并两号对顺序
  - Gate-6 出图: pending
    - Evidence: 出图仍暂停；预览色块是预期
    - Hans Confirmation: none — 是否解除暂停、用哪套图
  - S0-PKG run_game: pending
    - Evidence: [docs/evidence/S0.md](docs/evidence/S0.md) BLOCKED；用户级 `~/.grok/config.toml` 已写助手项
    - Hans Confirmation: none — 新会话热加载助手后补空包验证

## Tools & Resources

- 产品契约仓库：`BHnuit/midnight-neon-racer`（本目录）
- Cocos 工程（不在本 git 根下）：`/Users/hant/工作台/projects/creation/midnightroad/`
- 微信导出包：`midnightroad/build/wechatgame/`
- 完整开发方案：[docs/plan.md](docs/plan.md)
- 架构顾问：`game-architect`（只按 [§5.6](docs/plan.md#56-架构顾问按需调用) 的节点调用；不负责日常工作流）
- 包级验证：`@tencent-adm/weixin-minigame-helper`（只接 Creator 导出的 `build/wechatgame/`）
- 文件树：[TREE.md](TREE.md)；文档索引：[docs/README.md](docs/README.md)
- Netlify（已下线，站还留着）：site `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`；publish=`archive/offline/`；旧游戏在 `archive/h5-demo/`
- Cocos MCP 3.x Pro：`midnightroad/extensions/cocos-mcp-server/`（v1.7.9）；`http://127.0.0.1:21569/mcp`。不要往仓库扔 `.mcp.json`

## Progress Snapshot

- 需求已对齐；两轮框架验证已过；H5 已归档；Netlify 已下线
- 完整开发方案已由 Hans 接受（Gate 1）；S1–S5 代码已落地；美术出图暂停
- 双仓目录治理已完成：契约仓主动目录有职责 README；Cocos 工程有根级 AGENTS/README、架构地图和测试目录契约
- 工具策略已收敛：保留微信小游戏助手做包级验证，`game-architect` 只在 §5.6 架构节点调用；不为常规编码启用大型游戏工作室流程
- S1–S5 代码已提交（Cocos `1931557`）；`MvpLoop` 已删，画面仍是色块
- Hans 已试玩并否定离散换道；`run_game` 仍 BLOCKED
- 下一步：Gate 5 好友榜历史最高 + 双号对顺序

## Execution Log

- 2026-08-17：重入项目，补 `PROJECT.md`，`Alignment: pending`。先读现有架构，再按 grill-with-docs 对齐游戏框架。未实施玩法改动。
- 2026-08-17：Hans 确认第一版 **个人主体 + IAA**。术语写入 `CONTEXT.md`。下一问：第一版提审切片。
- 2026-08-17：Hans 确认账号已注册、备案与开发并行，第一版选 **重做循环**。下一问：玩家在比什么。
- 2026-08-17：Hans 定方向为肉鸽短局赛车：3–5 圈约 10 分钟、每局换图、局外成长、局内随机道具、目标单场得分。下一问：圈的空间含义。
- 2026-08-17：Hans 取消「圈」，改为一张种子大图从头到尾；路程按满速约 5 分钟。下一问：必经赛道还是分叉选路。
- 2026-08-17：Hans 确认大图为 **必经赛道**（选项 A）。下一问：弯是真转向还是三车道路段变化。
- 2026-08-17：Hans 确认 **三车道路段 + 轻量操作**（选项 A）。默认滑动换道，不做摇杆/方向盘。下一问：一局如何结束。
- 2026-08-17：Hans 确认结算 **C**：可看广告续 1 心（一局 1 次）。IAA 开发量按「一块激励视频 + 已选上架路径」计，不加横幅/插屏。下一问：局外成长怎么获得。
- 2026-08-17：Hans 确认局外成长为 **里程解锁新车，新车生命更高**；护盾/氮仍当局内。默认里程为账号累计（含未完赛已跑路程）。下一问：车是阶梯还是取舍。
- 2026-08-17：Hans 确认车库 **各有取舍**（B）。下一问：多生命换什么。
- 2026-08-17：Hans 定为四辆定位车：小货车（命）、跑车（更快/得分）、摩托车（窄、1 心）、飞行汽车（主动飞、无视交通）。撤销「后解锁生命更高」。下一问：飞行规则。
- 2026-08-17：Hans 定为两条进阶线：跑车→飞行汽车、小货车→压路机。飞行选 **B**：按住飞，飞量表替换氮表。摩托车是否保留未确认。下一问：压路机怎么硬。
- 2026-08-17：Hans 确认小货车是厚护盾条、多抗；压路机是长按氮条碾所有车和护栏。「小火车」按小货车记录。下一问：护盾条与心如何叠。
- 2026-08-17：Hans 确认全车 1 心；除摩托车外有保险杠（规则同 A）；局内有氮气装置。局外不再加心。摩托车留在车库。下一问：新号车与解锁顺序。
- 2026-08-17：Hans 确认解锁顺序 **A**（跑车→小货车→摩托车→飞行/压路机），续命为 **回满开局状态**（1 心+满杠）。下一问：得分构成。
- 2026-08-17：Hans 确认得分 **A**（路程+擦车+碾压+完赛，飞行只计路程），加分提示要当场可读；连击留后期。下一问：种子路段随机什么。
- 2026-08-17：Hans 确认种子路段要五件套，并加天气滤镜（晴雨雪雾风）和傍晚→清晨；明确不加分叉/高度。大风按不推车收。下一问：天气整局锁定还是途中变。
- 2026-08-17：Hans 确认天色/天气 **A**：每局傍晚→清晨，天气整局一种滤镜。下一问：备案二级类目。
- 2026-08-17：Hans 确认二级类目 **休闲**（后台已选定）。下一问：技术栈。
- 2026-08-17：Hans 确认技术栈 **自研 Canvas2D**（A）。不用 Cocos/Unity。下一问：是否开做最小包。
- 2026-08-17：Hans 选择继续访谈（好友榜+数值），先定游戏名。
- 2026-08-17：Hans 定名 **真夜中道路**。下一问：好友榜。
- 2026-08-17：Hans 自定介绍文案；头像要赛博像素但更干净，参考格子旗速度标。下一问：两张新头像选哪张。
- 2026-08-17：Hans 定头像为 A 构图、红色车、144×144 PNG（`assets/wechat-avatar-144.png`）。下一问：好友榜。
- 2026-08-17：Hans 确认头像已上传。下一问：好友榜。
- 2026-08-17：Hans 确认第一版社交 **A 结算好友榜**。全球榜和幻影以后再做。下一问：四项得分比重。
- 2026-08-17：Hans 确认得分 **B**（技巧分多、求花活爽感）。默认擦车每车一次、磨蹭不刷、碾压仅技能期间。下一问：保险杠抗几下。
- 2026-08-17：Hans 确认保险杠 **A**（薄 1 / 厚 3 / 摩托 0）。下一问：里程解锁节奏。
- 2026-08-17：Hans 确认里程节奏 **B**（约 2/6/15 局）。备案场景/玩法/系统文案写入 `docs/wechat-beian-copy.md`。下一问：益智类目是否改。
- 2026-08-17：Hans 将类目改为 **动作/跑酷**；备案字段只留本地，截图齐了再开口提交。
- 2026-08-17：Hans 确认适龄 **12+**。下一问：局内美术。
- 2026-08-17：Hans 确认美术 **A 赛博像素整套重画**；增加 `mayonaka-art` 技能与 `docs/art-bible.md`。下一问：技能条时长。
- 2026-08-17：Hans 确认技能条 **B**（约 2 秒、满表两次、开局半表）。下一问：是否结束对齐。
- 2026-08-17：Hans 选先出美术锚点。已交跑车正后视图（`mayonaka-art`），未写玩法。
- 2026-08-17：Hans 指定 cyber pixel city，并安装 TaiT CRT + pixel-asset-master。风格写入 art-bible；公路预览在 `assets/minigame/previews/`。
- 2026-08-17：三车道预览重画（旧双车道线已刮掉）。Hans 指定原图两侧品红光带只在氮加速时出现；写入 art-bible / CONTEXT，预览 `play-night-3lane-nitro.jpg`。
- 2026-08-17：Hans 确认风格留、构图按修订 01。落下 `docs/art/`（色卡、像素格、图层、CRT）和 `assets/minigame/palette/`、`layers/`。未改透视脚本，等选定 A/B/C。
- 2026-08-17：Hans 点头先做修法 A。`_paint_3lane.py` 改为 `VX,VY=376,797`、`LANE_AT_CAR=340`。验收：消失点/夹角已 PASS，车位未动；底边退让、接地、点阵、空天仍 FAIL。
- 2026-08-17：Hans 确认透视对，并要为出图 agent 补框架。写下 `docs/art/roadside-approach.md`、`car-grounding.md`、`sky-catalog.md`。中景定为纵向街墙+卡片按 1/z 推近，不重烤整张底板。
- 2026-08-17：傍晚进城空天第一版被否（色卡硬切条，没用参考）。重做为 ref-5 扫描线 + ref-3 暖边取样，扁日落在橙带里。样张 `play-dusk-approach.jpg`。
- 2026-08-17：Hans 判定天空观感仍不合格，美术框架先跳过。技术栈从自研 Canvas2D **改回 Cocos**（Creator 3.8.6+，MCP 3.x Pro + Codex/Cursor，导出到微信开发者工具）。手搓 `game.js` 计划作废。`CONTEXT.md` 用「Cocos工程」替换「自研画布」。
- 2026-08-17：把官方「学习新手教程」补进附录 [docs/wechat-minigame-start.md](docs/wechat-minigame-start.md)。
- 2026-08-17：Hans 选第一刀 **A**。过线=Cocos 空包在微信开发者工具里能跑。写入 `CONTEXT.md` 与 [docs/cocos-slice-a.md](docs/cocos-slice-a.md)。不在本会话手搓 game.js。
- 2026-08-17：工程落在 `/Users/hant/工作台/projects/creation/midnightroad/`。MCP 插件已就位；`npm install` 完成。该包无 `build` 脚本，`dist/main.js` 已存在。待 Creator 里启用扩展。
- 2026-08-17：Grok 用户配置接上 Cocos MCP：`http://127.0.0.1:21569/mcp`。doctor 健康，16 工具。
- 2026-08-17：Cocos「发布到微信小游戏」手册补进 [docs/cocos-publish-wechatgame.md](docs/cocos-publish-wechatgame.md)。
- 2026-08-17：第一刀 A 过线。`midnightroad/build/wechatgame` 已导入微信开发者工具，空场景黑屏。起始场景 `assets/scene.scene`。
- 2026-08-17：Hans 准备重开会话。后半段已写回：工程名 `midnightroad`、机位修法 A、出图暂停、第一刀已过、第二刀未开、Grok MCP 要新会话。不要提交仓库内 `.mcp.json`。
- 2026-08-17：新 Grok 会话已接到 Cocos MCP（16 个 Pro 工具，工程 `midnightroad`，端口 21569）。对照 https://github.com/DaxianLee/cocos-mcp-server 的 Pro 说明，把用法写入 [docs/cocos-mcp-pro.md](docs/cocos-mcp-pro.md)。第二刀仍未开。
- 2026-08-17：Hans 把工程设计分辨率改成 **720×1280**（`project_info` 已核）。写入 `CONTEXT.md`「画布」。未关仍是：第二刀是否开工、换道时能否同时按氮、四项得分数字。
- 2026-08-17：Hans 确认 **同时氮换道**。写入 `CONTEXT.md`。下一问：四项得分数字（推荐方案已给出，待选）。
- 2026-08-17：Hans 确认分值 **A**：路程 3000 / 擦车 +200 / 碾压 +500 / 完赛 +1200；短段完赛按比例、地板 +300。写入 `CONTEXT.md`「分值」。下一问：是否开第二刀。
- 2026-08-17：Hans 确认复述即第一版，并定调：本轮只验证需求 + 开发框架；第二刀实现前必须 **另开会话拆开发计划**。`Alignment: aligned`。落下 [ADR 0001](docs/adr/0001-first-version-loop.md)。MCP 复核：`midnightroad` ready，画布 720×1280。未写玩法代码。
- 2026-08-17：Hans 澄清第二轮验证 = **最小 MVP，不是正式开工**。在 `scene.scene` 用 MCP 搭了选车/三车道/本地结算，脚本 `midnightroad/assets/scripts/MvpLoop.ts`。预览已见到三屏（选车、赛道 HUD 路程 810、结算 路程/擦车/碾压/完赛）。记下 [docs/cocos-slice-b-mvp.md](docs/cocos-slice-b-mvp.md)。正式计划仍待下轮会话。
- 2026-08-17：本轮收工。进度写回；H5 Demo 整包迁到 `archive/h5-demo/`；根 `netlify.toml` 改指向归档以免误发空站。落下 [TREE.md](TREE.md)、[docs/README.md](docs/README.md)。下一轮会话写整个项目方案（`docs/plan.md`）。
- 2026-08-17：Hans 确认 Netlify 先下线，目标平台只留微信小游戏。publish 改为 `archive/offline/`（停机页），站点不删，以后有新 Demo 再开。
- 2026-08-17：按已对齐需求与 Cocos 色块验证写下 [完整开发方案](docs/plan.md)：正式模块、S0–S7 垂直切片、验证矩阵、审查标准、Agent 开工卡与 Hans 决策门。只改契约仓文档，未改 Cocos 玩法；方案待 Hans 验收。
- 2026-08-18：按 SkillHub 指南安装并校验 `@tencent-adm/weixin-minigame-helper@1.0.1` 与 `@user_5e9ef3eb/game-studio@1.0.0`。用两者复审契约仓、Cocos 磁盘结构和完整方案：修正旧名/多点触控表述，补现状与目标结构、玩家体验支柱、系统依赖、状态/边界/调参、风险、追溯、证据格式，以及 Cocos 构建后 `run_game` / `get_logs` / 截图 / 真机验证链。未改正式玩法代码。
- 2026-08-18：按 Game Studio 的阶段识别、系统映射、架构落位和 QA 交接方法治理双仓文件树。契约仓为主动维护的 `docs/`、`assets/minigame/` 各层补职责 README；新增 [ADR 0002](docs/adr/0002-dual-repo-governance.md)。Cocos 工程新增根 AGENTS/README、`docs/architecture.md`、`tests/core/` 说明并加固忽略规则。为避免 Asset Database 与模板污染，没有在 Cocos `assets/` 或 `build-templates/wechatgame/` 内塞 README，也未改 `.scene/.prefab/.anim/.meta` 或玩法代码。
- 2026-08-18：按 Hans 决定卸载 `@user_5e9ef3eb/game-studio`，安装 `game-architect` 作为架构知识顾问。后续按方案 §5.6 仅在 S0/S1 架构落地、S2 种子地图、重大需求变更和已测出的性能瓶颈节点调用；常规实现、修 Bug、调数值、微信包验证不调用。保留前期 Game Studio 复审记录，不再把它写成当前依赖。
- 2026-08-18：Hans 接受 [完整开发方案](docs/plan.md) 并授权按 S0→S1 开工。原话：「接受，授权开工」。Gate 1 关闭。未改正式玩法；进入 S0 工程基线。
- 2026-08-18：完成 S0 工程部分。Cocos 首个基线提交 `dda5a64`，分支 `main` 与 `BHnuit/s1-formal-second-slice`。`npm test` / `typecheck:core` 通过；`game.ejs` 与 Creator 3.8.6 默认一致；Creator 打开 `scene.scene` 无断裂引用。S0-PKG 因本会话无微信助手 MCP 标 BLOCKED。未改正式玩法。
- 2026-08-18：S1 开工。Cocos `assets/scripts/core/RunSession.ts` 通过 10 个纯规则测试；未改场景，未删 `MvpLoop`。
- 2026-08-18：Hans 授权无人值守完成 S1–S5，验收统一留 S6。原话见计划评论。Gate 2–5 延后确认。
- 2026-08-18：S1–S5 实现落地。`GameDirector`/`RoadFactory`/`PlayerProgress`/Dev+WeChat adapter/开放数据域源码；场景改挂 `MainController` 并删除 `MvpLoop`。16 个 core 测试通过；Creator 选车屏无 error。PKG/真机广告/双号验榜/出图仍待 S6。
- 2026-08-18 03:17 +0800：本轮收工存档。Hans 确认下一步是醒来后逐项确认 Gate 2–6 与微信助手 `run_game`。已写明：Creator 无完整试跑；预览仍是色块属预期。状态改为 `waiting`。
- 2026-08-18：Gate 2 试玩。Hans 否定离散换道；锁跟手横移（松手停缝）、双击加速。写入 [ADR 0003](docs/adr/0003-follow-steer.md)。擦车未锁。未改 Cocos。
- 2026-08-18：擦车定为迎面晚躲，不是贴身路过。写入 [ADR 0004](docs/adr/0004-late-dodge-graze.md)。连击是否进第一版未锁。未改 Cocos。
- 2026-08-18：Hans 确认连击进第一版，只吃擦车。写入 [ADR 0005](docs/adr/0005-graze-combo.md)。加成算法未锁。未改 Cocos。
- 2026-08-18：连击定为阶梯 200/300/400、第 4 下起单笔封顶 +500。未改 Cocos。等点头开工。
- 2026-08-18：Cocos 已改跟手横移、双击加速、晚躲擦车、连击。预览改短段。`npm test` 17 过。等 Hans 再摸。
- 2026-08-18：Hans 确认 Gate 2「可以 手感对了」。预览改回完整一局。进入 Gate 3。
- 2026-08-18：Hans 确认摩托钻缝、跑车挂虚线会撞。Gate 3 关闭。预览五车解锁已关。进入 Gate 4。
- 2026-08-18：Hans 交 AppID `wxcce206285c95068b`；流量主开不了。第一版无广告、无续命。写入 [ADR 0006](docs/adr/0006-no-ads-first-ship.md)。Gate 4 延后。进入 Gate 5。
