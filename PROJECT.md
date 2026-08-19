# 真夜中道路

**Type**: 微信小游戏（个人 IAA）
**Status**: active
**Created / Last Updated**: 2026-08-19
**协作等级 / 角色**: L2 执行者（Gate 2–3、5、6 已过；Gate 4 广告延后；出图按 G0→G6 单锚点推进）
**Alignment**: aligned
**Feishu**: 未发布

## Startup Summary

**Project Snapshot**: `midnightroad` 已完成可试玩色块原型：完整路线、五屏、路段级混合车流、三种换向外皮、OutRun 式左右弯/上下坡、统一擦车、低文字 TaiT CRT 菜单、顶栏命格/总分与底部时速环均已落地。49 项规则测试通过；跑车满速全程约 300 秒，试玩启动档案抬到最高解锁里程。道路前视距离为 1800、透视深度为 260，机位 A-2 使用 `(376,700)`、`k=1.572`。同向车按逐车速度运动；技能空表在未释放时 20 秒回满；进入危险段前同向车先侧向退场，迎面车从报信阶段才入场，规则层禁止混流。场景主题在段尾 1200 距离内渐变，日月重叠交接，并以连续地表补足远景到屏幕下方。Cocos MCP 已重建局内色块预览。Hans 已解除 Gate 6；正式图按 G0→G6 从 A0 单锚点开始，尚未生成。

**Next Step**: **下一会话写 A0 发车页 TaiT 风格锚点的 G0 工单**（一张 `720×1280` 预览，只进 `assets/minigame/previews/`，不进微信包）。本轮不写工单、不生成图。改玩法先读 [docs/framework-loop.md](docs/framework-loop.md)。

## Objective

上架微信小游戏 **真夜中道路**。第一版走个人主体、IAA。核心循环是种子大图短局得分，不以 Demo 的一命闪避为契约，也不用圈。

## Scope

第一版产品边界以 `CONTEXT.md` 为准。文件树见 [TREE.md](TREE.md)。

做：个人主体（声明不开虚拟支付）、动作/跑酷、12+、种子大图约 5 分钟、三车道跟手横移、双击加速、贴近擦车（迎面晚躲 / 同向超车）、擦车连击、五车+里程、分值 A、结算好友榜、Cocos 导出微信包。第一版无广告续命。

不做（第一版）：内购、全球榜、幻影陪跑、手写正式包 `game.js`、把 Demo 当提审包、跳过 G0/G1.5 批量出图。

H5 Demo 已归档（`archive/h5-demo/`）并下线。Netlify 站保留，只发 `archive/offline/`。以后有新 Demo 再开。

## Acceptance Criteria

本轮（访谈 + 框架）已满足：

- AC-align：Hans 确认复述即第一版；词在 `CONTEXT.md`，决定在 [ADR 0001](docs/adr/0001-first-version-loop.md)
- AC-pipe：空场景微信包能编（第一刀 A）；Creator 预览里色块循环能选车/开/结算（[slice-b](docs/cocos-slice-b-mvp.md)）；MCP 能操作 `midnightroad`

第一版上架验收（**代码与 Creator 色块验证已覆盖 AC-play/AC-cars；平台与正式视觉仍未完成**，按 [完整开发方案](docs/plan.md) S1–S7 推进）：

- AC-play：能选车、开种子大图、当场看到四项分、可本地结算
- AC-cars：五车定位与里程节奏符合契约
- AC-iaa：第一版无广告；结算好友榜；无内购。激励续命等流量主开通（Gate 4 延后）
- AC-ship：Cocos 微信包在开发者工具/真机可玩，名称与备案稿一致

正式第二刀范围仍是「选车 + 一段三车道 + 本地结算」，按方案 S1 实施；广告和好友榜不进入这一刀。

## Acceptance Review

- Mode: sequential
- Current Item: A0-G0
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
  - Gate-5 好友榜: accepted
    - Evidence: 上报 `best_score_v1` 历史最高；低分不覆盖。双号实榜仍待以后
    - Hans Confirmation: 2026-08-18「确认」历史最高
  - Gate-6 出图: accepted
    - Evidence: 按 [ai-game-art-pipeline](.grok/skills/ai-game-art-pipeline/SKILL.md) 串行 G0–G6；第一件是 A0 发车页风格锚点
    - Hans Confirmation: 2026-08-19「可以，解除出图暂停，应用 ai-game-art-pipeline」
  - S0-PKG run_game: accepted
    - Evidence: [docs/evidence/S0.md](docs/evidence/S0.md) `S0-PKG-02`；[S1–S5](docs/evidence/S1-S5.md) `S1-PKG-06`
    - Hans Confirmation: none — 包能启动已有助手+Orca 证据；不替代开发者工具或真机

## Tools & Resources

- 产品契约仓库：`BHnuit/midnight-neon-racer`（本目录）
- Cocos 工程（不在本 git 根下）：`/Users/hant/工作台/projects/creation/midnightroad/`
- 微信导出包：`midnightroad/build/wechatgame/`
- 完整开发方案：[docs/plan.md](docs/plan.md)
- 改代码 / Creator / 微信预览：[docs/framework-loop.md](docs/framework-loop.md)
- AI 美术生产：`.grok/skills/ai-game-art-pipeline/`；一手资料与引擎依据见 [AI 美术流水线研究](docs/ai-game-art-pipeline-research.md)。Gate 6 解除后按 G0→G1→G1.5→G2–G6 调用，先单锚点校准再批量
- 架构顾问：`game-architect`（只按 [§5.6](docs/plan.md#56-架构顾问按需调用) 的节点调用；不负责日常工作流）
- 包级验证：`@tencent-adm/weixin-minigame-helper`（只接 Creator 导出的 `build/wechatgame/`）
- 文件树：[TREE.md](TREE.md)；文档索引：[docs/README.md](docs/README.md)
- Netlify（已下线，站还留着）：site `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`；publish=`archive/offline/`；旧游戏在 `archive/h5-demo/`
- Cocos MCP 3.x Pro：`midnightroad/extensions/cocos-mcp-server/`（v1.7.9）；当前 `settings/mcp-server.json` 端口 **21570**（`http://127.0.0.1:21570/mcp`）。不要往仓库扔 `.mcp.json`

## Progress Snapshot

- 需求已对齐；两轮框架验证已过；H5 已归档；Netlify 已下线
- 完整开发方案已由 Hans 接受（Gate 1）；S1–S5 代码已落地；Gate 6 已于 2026-08-19 解除，出图从 A0 单锚点按 G0→G6 推进
- 双仓目录治理已完成：契约仓主动目录有职责 README；Cocos 工程有根级 AGENTS/README、架构地图和测试目录契约
- 工具策略已收敛：保留微信小游戏助手做包级验证，`game-architect` 只在 §5.6 架构节点调用；不为常规编码启用大型游戏工作室流程
- S1–S5 代码已提交（Cocos `1931557`）；已锁规则色块已落地（midnightroad `de97611` 之后还有未提交测试与结算屏）
- Hans 已试玩并否定离散换道；助手 `run_game` 已于 2026-08-19 补上，发车页可见
- U1 主体与 U2 的 720×1280 核心矩阵已完成：混合车流、三次危险段、4–6 波、弯坡与隐藏车灯光提示、统一擦车、五屏固定槽、锁车态、三灯发车、结算揭示与交通节点池已跑通；长屏/异形安全区仍留 Gate 6 前补测
- Creator 当前 67 节点、最大深度 5，场景引用/层级/布局 0 问题；`npm test` 49 项通过；`build/wechatgame` 于 11:11:14 刷新，约 2.90 MB / 40 文件，`libVersion=""`
- 项目级 `ai-game-art-pipeline` 已建立，并由三轮独立前向测试驱动修订、最终新上下文复测通过：先锁结构白模，再用同一锚点做模型/提示词/语言/控制参数矩阵，冻结可复现 `style-profile` 后才风格化、像素化和接入 Cocos；未知生产值保持 `TBD`，不从安全框、容器色卡或“低/高”标签反推具体数值
- 接局内 FX 前仍欠 `RunEvent[]` 与 `FxBack/FxFront`；长屏 SafeArea Hans 已嘱先不管。A0 风格锚点不依赖这两项
- 下一步：下一会话写 A0 的 G0 工单；本轮已写 [framework-loop.md](docs/framework-loop.md) 并整理文档入口

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
- 2026-08-18：Hans 确认好友榜为历史最高单局分。Gate 5 规则关闭。双号实榜以后再验。进入 Gate 6。
- 2026-08-18：屏幕定为发车进门（中开车、右下选车/说明），结算两 tab，无续命。选车出口未锁。见 [ADR 0007](docs/adr/0007-screen-map.md)。
- 2026-08-18：Hans 确认选车只换车、回发车；只有发车页「开车」开局。
- 2026-08-18：Hans 确认发车页露出当前车。屏幕关系收口。
- 2026-08-18：开车 HUD 定为顶栏心杠/总分/时速/技能条；技巧分跳字并做小丑牌式燃烧震动。路程不烧。
- 2026-08-18：选车改为左右翻页（侧视+性能+说明）。HUD 左命格下叠技能条，中总分，右时速下累计计时。命格=杠+心。
- 2026-08-18：界面结构确认。选车文案按宝开语写入 [docs/ui-copy.md](docs/ui-copy.md)。
- 2026-08-18：选车图鉴换成正式稿：逮虾户 / 钢板 / 无头骑士 / 云玩家 / DIO。无头骑士速度按机制改为快于跑车、慢于飞车。
- 2026-08-18：落下 `.grok/skills/popcap-almanac/`。图鉴系统标为以后做；第一版只在选车页用车图鉴。
- 2026-08-18：Hans 确认保险杠+重量级一起用。见 [ADR 0008](docs/adr/0008-weight-and-bumper.md)。压路机时停技能未锁。
- 2026-08-18：Hans 确认压路机满条双击、时停清屏。见 [ADR 0009](docs/adr/0009-roller-timestop.md)。代码未改。
- 2026-08-18：来车定为 24 种（重量/速度/占道/行为/权重）。见 [docs/traffic-roster.md](docs/traffic-roster.md)。第一版建议先做 10 种。
- 2026-08-18：Hans 确认第一版 10 种来车；结算失败提示随撞上的车变化。文案写入 [docs/ui-copy.md](docs/ui-copy.md)。
- 2026-08-18：结算一行提示定稿（完赛平安夜、警车请喝茶，其余 9 句最终稿）。
- 2026-08-18：已锁规则做进 midnightroad 色块。Creator 自测：发车/选车/说明/开车/肇事结算/好友榜 tab/回发车。core 27 测通过。未点头前不出图。
- 2026-08-18：删掉空的 `assets/scene.scene`。正式入口只留 `scenes/Main.scene`。
- 2026-08-18：Hans 明确施工/路障与路形变化（大桥、隧道、土路）分开，同一段不叠。写入 [ADR 0010](docs/adr/0010-exclusive-road-kinds.md)。midnightroad 工厂、碰撞和色块绘制已按此拆开。
- 2026-08-18 收工：玩法先停。落下 [docs/color-block-now.md](docs/color-block-now.md)（代码结构、已锁需求、文案、屏幕文字图示）。下一会话 Codex 审查界面。未提交。
- 2026-08-18：使用 `game-architect` 的 UI/反馈/3C 边界与 TaiT CRT 设计语言复审正式工程；Cocos MCP 读取场景、运行时截图和知识库，确认 720×1280、场景结构/引用无错误。落下 [docs/ui-art-production-spec.md](docs/ui-art-production-spec.md)：固定五屏几何、HUD、前后 FX、素材批次和验收矩阵；把全迎面/全同向/路段级混合设为出图前决策门。未改玩法代码或 Creator 资产，Gate 6 仍暂停。
- 2026-08-18：Hans 选择路段级混合车流；接受可变车道换向门、施工借道、隧道换向三种外皮混用。三者共享“车流减少→视觉预警→道路导流→无车缓冲→首辆报信车→迎面车流”的固定语法。危险段车道组合、时长、频率与同向超车计分继续逐项确认；未改代码。
- 2026-08-18：Hans 确认危险段三条车道都可能出现迎面车。每个波次按最宽玩家车保证至少一条连续可解通道；双车道大巴、横扑和摆动不得封死最后通道，技能不作为生存前提。下一项确认危险段时长；未改代码。
- 2026-08-18：Hans 选择每个危险段 20–25 秒有效迎面车流，目标 4–6 波；进入/离开的换向演出不计入这段时长。下一项确认一局出现次数；未改代码。
- 2026-08-18：Hans 选择一局约 5 分钟出现 3 次危险段，有效迎面车流合计约占 20%–25%。随后提出是否加入 OutRun 式上下坡、左右弯与岔路；核对确认当前契约和实现均未包含这些几何，转为下一项范围决策。未改代码。
- 2026-08-18：Hans 选择加入 OutRun 式真实 2.5D 左右弯与上下坡，不加岔路。跟手横移保持相对道路中心，不增加方向盘或弯道离心甩车；先做隔离色块投影原型。下一项确认迎面危险段与弯坡的叠加范围；未改正式代码。
- 2026-08-18：Hans 选择危险段与急弯、坡顶完全混合，并明确“撞了就是命”。允许具体来车被道路遮住且不保证逐车反应时间；仍保留每波至少一条几何通道、固定 seed 固定答案。下一项确认是否给环境弱提示；未改正式代码。
- 2026-08-18：Hans 选择隐藏来车使用环境弱提示：至少有头灯染光、坡顶闪光或护栏反光之一，可加短促喇叭；不显示 HUD 警告，也不保证足够反应。下一项确认同向超车计分；未改正式代码。
- 2026-08-18：Hans 选择同向贴近超车也计入擦车，并指出它与迎面晚躲都是“贴近后横移通过”。新增 [ADR 0011](docs/adr/0011-mixed-flow-graze.md)：统一玩家用语、连击与结算项；同一目标一次，普通远距超车不计分。下一步开始逐屏确认 UI；未改正式代码。
- 2026-08-18：Hans 选择菜单以游戏界面为主，只借 TaiT 的硬边窗口、点阵、CRT 外缘信号和不对称层级；不做完整复古电脑桌面，不放假菜单栏、假光标或无功能桌面图标。下一项确认发车页车辆占比；未改正式代码。
- 2026-08-18：Hans 选择发车页当前车辆完整收在 `600×340` 主展示窗内，车辆本体使用 `300×140` 安全框，不做破框海报构图。下一项确认车辆展示角度；未改正式代码。
- 2026-08-18：Hans 选择发车页车辆使用车尾三分之四视角。五辆车各做独立发车展示图，与选车侧视图、局内正后视精灵分开，并保持同框同锚点。下一项确认展示窗背景；未改正式代码。
- 2026-08-18：Hans 选择五辆车共用霓虹公路发车线背景。背景独立为 `568×288` 窗内图层，只含夜城、空道路和发车线，不烤入车、交通、文字或按钮。三个入口沿用 ADR 0007 已确认的“开车居中、选车/说明右下”；下一项确认展示窗待机动画；未改正式代码。
- 2026-08-18：Hans 选择发车页低强度待机动画：尾灯呼吸、远处灯牌低频闪烁、车身最多 `2 px` 轻摆；道路和镜头不动，也不自动播放引擎声。下一项确认选车页翻车方式；未改正式代码。
- 2026-08-18：Hans 选择选车页同时支持左右滑动和 `88×88` 箭头；两者共用同一切车逻辑，一次输入只翻一辆，不另加手势说明文字。下一项确认车库首尾是否循环；未改正式代码。
- 2026-08-18：Hans 选择五车首尾循环；第一辆向左到第五辆，第五辆向右回第一辆，滑动与箭头方向一致。下一项确认未解锁车辆的信息可见度；未改正式代码。
- 2026-08-18：Hans 选择未解锁车辆只公开名称、侧视剪影和解锁里程；速度、命格、格言与图鉴正文解锁后才出现，窗口尺寸不变。下一项确认切车过渡；未改正式代码。
- 2026-08-18：Hans 选择切车时使用内容窗内 `2–4` 帧 CRT 信号错位，总长 `120–160 ms`；不做车辆滑入或全屏闪烁，也不新增过渡素材。下一项确认说明页演示形式；未改正式代码。
- 2026-08-18：Hans 选择说明页三项各配 `112×72` 低帧率小动画并轮流播放，任一时刻只动一项。发现并修正旧“迎面晚躲”说明为统一擦车短句；下一项确认擦车动画是否同时演示两种车流；未改正式代码。
- 2026-08-18：Hans 选择擦车小动画逐轮交替演示迎面晚躲和同向贴近超车，共用区域与一句文案，以正背轮廓和运动方向区分。下一项确认结算页结果插图；未改正式代码。
- 2026-08-18：Hans 要求剩余问题改为每次 5 项。复核后保留 10 个真正会改变体验、构图或素材量的决策，分为结算页 5 项和局内 HUD 5 项；其他技术规格不再逐项打扰。未改正式代码。
- 2026-08-18：Hans 一次确认第一批结算页为 `1B 2A 3B 4C 5A`：四类 `96×96` 结果图、默认本局、约 0.8 秒快速揭示、前三加本人、CRT 信号切入。下一批为最后 5 项 HUD 决策；未改正式代码。
- 2026-08-18：Hans 一次确认最后一批 HUD 为 `6B 7B 8A 9B 10A`，并要求界面尽量减少文字提醒：三块独立底板、四段技能条、纯 `×N`、只用三灯发车、路段只靠环境提示。至此 10 项批量确认和全部出图前决策完成；规格状态改为 decision-complete，Gate 6 仍暂停，未改正式代码。
- 2026-08-18：完成 U1 主体与 U2 的 720×1280 核心矩阵，形成可试玩 Cocos 色块原型。正式工程加入 `ROAD_VERSION=3` 混合车流、三次危险段、4–6 波可解生成、OutRun 式左右弯/上下坡、隐藏车辆灯光提示、同向/迎面统一擦车、五屏 CRT 色块 UI、三块低文字 HUD、锁车态、说明演示、0.8 秒结算揭示与交通节点复用池。`npm test` 43 项、两层 TypeScript 检查、Cocos scene/references/hierarchy/layout 均通过；Orca 浏览器逐屏与手势复验通过；Creator 于 23:30 重建约 3.0 MB 微信包。长屏/异形安全区仍留 Gate 6 前补测；当前宿主未暴露微信助手 MCP，故 `run_game/get_logs` 继续 BLOCKED；Gate 6 仍未解除。
- 2026-08-19：为 Gate 6 后的正式美术生产建立 `.grok/skills/ai-game-art-pipeline/`。基于 ControlNet、ImageMagick、Adobe、SPDX、Cocos/Unity/Godot 一手资料，流程固定为来源与规格 G0→结构白模 G1→模型/提示词/语言/控制参数矩阵 G1.5→正式风格化 G2→像素/点阵 G3→透明导出 G4→Cocos 代表资产接入 G5→微信包验收 G6；附 brief、style calibration、manifest 模板和 PNG 验证脚本。三轮独立前向测试依次暴露并修正：安全框不等于逻辑母版、菜单容器色卡不等于车辆色板、“低/高”控制标签不能脑补数值、不同模型参数不能无依据归一化；最终新上下文复测通过。未生成或导入正式美术，Gate 6 仍暂停。
- 2026-08-19：按试玩反馈完成原型修订。完整路线按跑车满速约 300 秒；试玩启动档案抬到最高解锁里程，五车全部可测但正式里程规则不变。道路、车道线、护栏、墙和路侧物件统一消费 `RoadSample` 投影，消除弯道第二消失点。选车页恢复 `ui-copy` 中格言、宝开体正文和独白，最长 DIO 文案无截断。发车页标题升为第一层，车辆窗缩至 `520×224` 并下移，按钮改为「发动」「车库」。`npm test` 45/45、core typecheck、Creator/Orca 运行预览通过；微信包于 00:17:50 构建成功。微信小游戏助手已通过 `codex mcp add` 安装并完成 MCP 2024-11-05 握手，当前会话工具表未动态暴露 `run_game/get_logs`。
- 2026-08-19：第二次试跑后延长局内视距。道路前视从 900 扩到 1800，透视深度独立为 260，坡度垂直投影提到 1.15；试玩机位由 A 修订为 A-2：消失点 `(376,700)`、`k=1.572`，保留近处约 509px 半路宽和玩家锚点，只增加画面内道路纵深。交通定义加入基准 km/h，固定 seed 生成 ±10% 逐车差异，`RunSession` 改为真实相对位移；`ROAD_VERSION=4`。46/46 测试、core typecheck、Cocos MCP 纯 Canvas 截图、场景/引用校验和 0 条 console error 通过。Orca 浏览器自动化通道未暴露，未取得 Orca 截图。用户报告的 `project.config.json: libVersion 字段需为 string, string` 按要求留到下个微信助手 MCP 会话，本轮未编辑配置或刷新微信包。
- 2026-08-19：第三次试跑后补齐三个原型缺口。技能条在未释放时按 `200ms/s` 自然恢复，空表 20 秒回满，装置仍立即补满；换向由 core 做方向许可，同向车在预警/导流阶段向两侧退场，迎面车从 sentinel 才激活，任一 snapshot 不混流；场景主题在段尾 1200 距离内连续混色，日月重叠淡变，并在 Mid 层铺道路外缘到画布外的连续地表。49/49 测试与两层 TypeScript 检查通过；Cocos 局内截图确认外侧地表无透明空带，同向车处于侧向退场状态。`project.config.json` 与微信导出包按约定未动。
- 2026-08-19：Hans 回复“可以，把本轮开发进度写回文档”，同意将 20 秒自然回能、换向不混流、场景/天空/地表连续接续及其 Cocos/测试证据纳入当前原型基线。该确认不等于解除 Gate 6；下一步收敛为修复微信 `libVersion`、刷新导出包并完成助手 `run_game/get_logs` 包级验证。
- 2026-08-19：完成微信包级验证。根因是 Creator 默认模板把 `libVersion` 写成 `"game"`，微信开发者工具校验失败；模板与导出包改为空字符串。Creator CLI 于 11:11:14 刷新 `build/wechatgame/`（约 2.90 MB、40 文件、AppID 正式号）。助手 `run_game` 起在 `http://localhost:3847`；Orca 内置浏览器见到发车页（逮虾户 / 发动 / 车库 / 说明）。助手 `capture_screenshot` 超时，改用 Orca 视口截图。未上传、未解除 Gate 6。
- 2026-08-19：预览里来车堆在路面上。根因是微信包把 `[...trafficPool.entries()]` 编成 `[].concat(iterator)`，回收循环每帧对 `undefined` 调 `removeFromParent`。已改成 `Map.forEach` 并刷新导出包。
- 2026-08-19：Hans 要求局内 HUD 避开微信右上角胶囊。先试过整套下移，试玩后改为顶栏只留命格/技能/总分/连击，底部单独一只时速+计时仪表。正式形是半圆环仪表盘；当前整圆 Graphics 只占槽，出图时整件替换。见 [ADR 0012](docs/adr/0012-bottom-hud-cluster.md)。Orca 预览（iPhone 6/7/8）已见到分槽；证据 [play-hud-split](docs/evidence/s1/midnightroad-play-hud-split.png)。
- 2026-08-19：Hans「可以，解除出图暂停，应用 ai-game-art-pipeline」。Gate 6 关闭。正式图按 G0→G6 串行，批次从 A0 一张发车页风格锚点开始；未填 G0、未过 G1.5 不批量，预览不进包。
- 2026-08-19：Hans 交代 A0 工单留到下一轮新会话；本轮把进度写回文档，并写清改代码 / Creator / 微信预览巡环。见 [docs/framework-loop.md](docs/framework-loop.md)。根目录 `参考/` 与契约仓根 `package-lock.json` 不入库。
