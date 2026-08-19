# 框架验证与调试巡环

**Status**: current（2026-08-19）
**给谁**：下一会话继续改玩法、查局内 bug、验微信预览
**不是**：出图工单（A0 留给下一轮）、开发者工具/真机、上传

色块原型已经能选车、开车、结算。后面改手感和框架，按本页走，不要再从第一刀空包或 `MvpLoop` 起步。

历史过线记录仍在 [cocos-slice-a.md](cocos-slice-a.md)（空包进开发者工具）和 [cocos-slice-b-mvp.md](cocos-slice-b-mvp.md)（最小色块循环）。那两页不再指导日常改动。

---

## 1. 先分清三套目录、两套 MCP

| 位置 | 是什么 | 改什么 | 不改什么 |
| --- | --- | --- | --- |
| 契约仓 `midnight-neon-racer/`（本仓） | 需求、ADR、验收、美术源 | `CONTEXT.md`、ADR、本页、证据 | 不放运行时代码、不放 `.mcp.json` |
| 正式工程 `/Users/hant/工作台/projects/creation/midnightroad/` | Cocos 3.8.6 源码 | `assets/scripts/**/*.ts`、`tests/`、`build-templates/` | 不手改 `.scene` / `.prefab` / `.anim` / `.meta` |
| `midnightroad/build/wechatgame/` | Creator 导出的微信包 | 只能整包重建 | 不手改 `game.js` |

| MCP | 指向 | 负责 |
| --- | --- | --- |
| Cocos MCP Pro | `midnightroad/` 工程根；Creator 必须开着 | 场景、节点、资源、编辑器预览与校验 |
| 微信小游戏助手 | **必须**含 `game.js` 的 `build/wechatgame/` | `run_game`、`get_logs`、截图、授权后的真机/上传 |

顺序固定：

```text
改 TypeScript / 契约
    → 规则测试
    → Creator 预览（查画面和手感）
    → Creator 重建 wechatgame
    → 助手 run_game
    → Orca 打开 http://localhost:3847
    → get_logs / 截图
```

不要用助手去改场景，也不要用 Cocos MCP 去当微信预览器。

---

## 2. 代码改哪里

工程入口是 `assets/scenes/Main.scene` 上的 `MainController`。`MvpLoop` 已删。

| 要改的东西 | 文件 | 约束 |
| --- | --- | --- |
| 车速、命格、计分、技能时间、路肩 | `assets/scripts/core/GameBalance.ts` | 禁止 `import cc` / 调 `wx` |
| 一局规则、擦车、换向许可 | `assets/scripts/core/RunSession.ts` | 只出 snapshot；视图不要另存一份权威状态 |
| 路段、危险段、弯坡、车流种子 | `assets/scripts/core/RoadFactory.ts`、`RoadProject.ts`、`Traffic.ts` | `ROAD_VERSION=4`；机位 A-2 |
| 发车/选车/结算流程 | `assets/scripts/app/GameDirector.ts` | 只编排 |
| 触摸、交通池、道路色块 | `assets/scripts/cocos/MainController.ts` | 适配层 |
| 五屏与 HUD 色块 | `assets/scripts/cocos/ColorBlockUi.ts` | 顶栏两块 + 底部时速占位环 |
| 选车图鉴文案 | 先改契约仓 `docs/ui-copy.md`，再抄到 `core/CarCopy.ts` | 不在会话里自拟介绍 |

玩法词变了，先改 `CONTEXT.md` / ADR，再改代码。冲突时停下来，不要用实现反推契约。

微信包把 `[...map.entries()]` 编成 `[].concat(iterator)`，回收循环会炸。遍历 `Map` 用 `forEach`，并对节点做 `isValid` 判断。

---

## 3. 本机怎么验规则

在 `midnightroad/` 根目录：

```bash
npm test
npm run typecheck:core
```

当前是 49 项 vitest + `tsc -p tsconfig.core.json --noEmit`。`core` 里不得出现 `from 'cc'` 或 `wx.`。

只改文案或 HUD 几何时，测试可能全绿，仍要看画面。

---

## 4. 怎么在 Creator 里看

1. 用 **Cocos Creator 3.8.6** 打开 `midnightroad/`。面板要开着，Cocos MCP 才活。
2. 打开 `db://assets/scenes/Main.scene`，预览。
3. 画布 720×1280，`fitWidth`。机位 A-2：消失点 `(376,700)`，`k=1.572`。
4. 改 `.scene` / `.prefab` / `.anim` / `.meta` 只用 Cocos MCP 或编辑器，不要文本手改。

Cocos MCP 的活端口写在工程 `settings/mcp-server.json`（本机最近是 **21570**，不要死记 21569）。客户端 url：`http://127.0.0.1:<端口>/mcp`。用法见 [cocos-mcp-pro.md](cocos-mcp-pro.md)。

不要对 Creator 可执行文件跑 `--help`：它会再拉起一个编辑器。本机已有工程窗口时，只对那个窗口说话。

面板里的「构建」只打开构建窗，不保证导出完成。要刷新微信包，用下一节的 CLI。

---

## 5. 怎么刷新微信包

模板在 `midnightroad/build-templates/wechatgame/`。`project.config.json` 的 `libVersion` 必须是空字符串 `""`。Creator 默认的 `"game"` 会被微信开发者工具判成非法（报 `libVersion 字段需为 string`）。

在工程已由 3.8.6 打开的前提下，用官方 CLI 构建（退出码 **36** 在本机表示构建成功，不是失败）：

```bash
/Applications/Cocos/Creator/3.8.6/CocosCreator.app/Contents/MacOS/CocosCreator \
  --project /Users/hant/工作台/projects/creation/midnightroad \
  --build "platform=wechatgame;debug=true"
```

成功后核对：

- `build/wechatgame/game.js` 时间戳已更新
- 同目录有 `game.json`、`project.config.json`
- `libVersion` 仍是 `""`

不要在导出包里手写玩法。`build/` 不提交。

也可用编辑器 **项目 → 构建发布 → 微信小游戏 → 构建**。导入开发者工具时，选含 `project.config.json` 的 `build/wechatgame/`，不要选工程根。面板构建说明见 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md)。

---

## 6. 怎么用助手预览

1. 调微信小游戏助手 `run_game`，`workspacePath` =  
   `/Users/hant/工作台/projects/creation/midnightroad/build/wechatgame`  
   （目录里必须有 `game.js`）。
2. 返回 `http://localhost:3847`。端口在同一次助手进程里保持不变；再调一次会重新打包并刷新已打开的页。
3. 用 Orca 内置浏览器打开或刷新该地址（`orca tab` / `orca goto` / `orca reload`）。
4. 等约 2 秒，`get_logs`。过滤可用 `error|Error|TypeError|Uncaught`。
5. 看画面：助手 `capture_screenshot` 只抓游戏画布，有时超时；超时就用 `orca screenshot`。点游戏里的按钮，要往 iframe 画布上点，DOM 快照里没有「发动」。

预览器控制台里的 `Element is not defined`、`detectIdeTheme is not defined` 来自预览壳，不是局内脚本。先看 `assets/main/index.js` 的栈。

设备选择：

- **iPhone 6/7/8**（375×667）接近 9:16，顶栏 HUD 完整，适合看开车。
- **iPhone 12/13** 带刘海且画布顶对齐，标题和顶栏会被裁，底下留白。这是预览机型，不是游戏坏了。长屏 SafeArea 先不管。

真机扫码、上传必须另有授权，且成功后禁止再 `run_game`（二维码会丢）。

---

## 7. 开车画面现在长什么样

顶栏左：命格 + 四段技能条。顶栏中：总分和 `×N`。顶栏右：空给微信胶囊。底部中央：时速 + 计时；正式形是半圆环仪表盘，现在的整圆 Graphics 只占槽。

证据：[evidence/s1/midnightroad-play-hud-split.png](evidence/s1/midnightroad-play-hud-split.png)。决定见 [ADR 0012](adr/0012-bottom-hud-cluster.md)。

试玩启动档案抬到最高解锁里程，五车都能开；正式里程规则没改。

---

## 8. 下一会话不要重踩的坑

- 契约仓和 Cocos 仓是两个 Git。改了代码只交契约、或只交工程，下一会话会对不上。
- 根目录 `参考/`、契约仓根 `package-lock.json`、工程根误放的 `project.config.json` 不入库。
- 助手预览不是开发者工具，更不是真机。包能启动 ≠ 平台能力过线。
- Gate 6 已解除，但 A0 工单还没写。未填 G0、未过 G1.5，不批量出图，不把 `previews/` 打进包。

未关且不挡日常调手感的：`RunEvent[]` 透传、`FxBack/FxFront`、长屏 SafeArea、开发者工具/真机 smoke、Gate 4 广告、好友双号榜。
