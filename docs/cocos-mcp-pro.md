# 附录 · Cocos MCP 3.x Pro

本仓库用的是 **Pro**，不是 GitHub 开源 50 工具那一套。

- 上游仓库（开源说明 + Pro 介绍）：https://github.com/DaxianLee/cocos-mcp-server
- Pro 购买/说明：https://www.vberai.com/game-engines/cocos
- 本机安装：`midnightroad/extensions/cocos-mcp-server/` **v1.7.9**（production，2026-07-18）
- 公开 README 写的是 Pro 1.7.8；以本机 `package.json` / `INSTALL.md` 为准

Pro 的卖点（仓库 README）：**16 个意图级工具**、约 231 项操作、12 个模块、**Streamable HTTP**。开源版是另一套 `scene_management` / `node_lifecycle` 命名，不要对着开源示例调。

## 本机怎么接

| 项 | 值 |
| --- | --- |
| 工程 | `/Users/hant/工作台/projects/creation/midnightroad/` |
| Creator | 3.8.6，面板要开着 |
| MCP 端口 | 以工程 `settings/mcp-server.json` 为准（本机最近 **21570**；旧笔记里的 21569 不要死记） |
| HTTP | `http://127.0.0.1:<端口>/mcp` |
| Grok | `~/.grok/config.toml` 的 `[mcp_servers.cocos-creator]` |
| Cursor / Codex | 已接同一地址（各自客户端配置） |

Grok 配置：

```toml
[mcp_servers.cocos-creator]
url = "http://127.0.0.1:21570/mcp"
enabled = true
```

**不要**在契约仓库 `midnight-neon-racer` 放 `.mcp.json`。未信任的仓库文件会盖掉用户配置。

## 与微信小游戏助手的边界

本项目有两套不同的 MCP，不得互相替代：

| 服务 | 输入目录 | 负责 | 不负责 |
| --- | --- | --- | --- |
| Cocos MCP Pro | `midnightroad/` | 场景、节点、预制体、资源、Creator 预览与校验 | 微信包日志、真机二维码、上传 |
| 微信小游戏助手 | `midnightroad/build/wechatgame/` | 对含 `game.js` 的导出包执行 `run_game`、`get_logs`、截图、真机预览和授权后的上传 | 修改 `.scene`、替代 Creator 构建 |

工作顺序是「Cocos MCP 改资产并在 Creator 验证 → Creator 构建微信包 → 微信小游戏助手验证导出包」。助手技能安装在用户级 skill 目录，不复制进项目；其 stdio MCP 是否可调用在 S0 首次包级验证时确认。任何 AppID、上传私钥或 token 都不得写入仓库。

Grok 换会话才会把新 MCP 编进工具表；`/mcps` 按 `r` 刷新不够。Creator 关了、端口改了，本会话里的工具会立刻失败。

## 开源 vs 本机 Pro

| | 开源 README | 本机 Pro 1.7.9 |
| --- | --- | --- |
| 协议 | HTTP，示例端口 3000 | Streamable HTTP，本机以 `settings/mcp-server.json` 为准（最近 **21570**） |
| 工具形态 | 约 50 个细工具（`node_lifecycle` 等） | **16** 个意图工具，靠 `action` 切换 |
| 知识库 / 动画 / Spine | 无或不完整 | 有 `cocos_knowledge`、`cocos_animation`、`cocos_spine` |
| 一次搭整棵 UI | 无 | `cocos_builder` / `cocos_composite` / `cocos_template` |

开源 README 后半段的 `node_lifecycle` 示例**不能直接用**。

## Grok 里怎么调

先 `search_tool` 看当前 schema，再 `use_tool`。限定名是 `cocos-creator__<工具>`：

```text
search_tool  query="cocos scene hierarchy"
use_tool     tool_name="cocos-creator__cocos_scene"
             tool_input={"action":"hierarchy"}
```

Cursor / Codex 里工具名一般是裸的 `cocos_scene`，参数一样。

不熟的 `action` 先问知识库：

```text
cocos_knowledge  topic="tool_guide"            → 工具索引
cocos_knowledge  topic="tool_guide" query="scene"
cocos_knowledge  topic="tool_guide" query="node.create"
```

插件警告里写「不确定就调 `cocos_do`」。**本会话 16 个工具里没有 `cocos_do`**，不要编这个名字。

## 硬规则（改场景前先读）

1. **禁止**用 `write` / `search_replace` / `sed` 改 `.scene` / `.prefab` / `.anim` / `.meta`。这些是 UUID 引用资产，手改会「资源导入失败」。
2. 引用资产优先 `db://assets/...`，不要猜 UUID。要 UUID 就 `cocos_asset action=query_uuid`。
3. 节点参数可传 UUID、路径（`Canvas/Panel/Btn`）或名字，插件会解析。
4. 3 个以上同类改动走批量：`cocos_node.batch_modify`、`cocos_composite.batch_create_*`、`cocos_component.batch_click_event`。
5. 改完用 `cocos_scene action=validate_scene` 查断裂引用；布局/重叠用 `cocos_validate`。
6. 微信小游戏包仍按 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md) 在编辑器里构建。Cocos MCP 的 `build_settings` 自己说完整构建配置要走 Editor UI；`editor.build` 示例平台是 `web-mobile`，**不能代替**「发布到微信小游戏」，微信小游戏助手也不能替代 Creator 构建。
7. 不要手搓正式包 `game.js`，不要把 Demo 的 `window.__game` 搬进 Cocos。

## 16 个工具（2026-08-17 本会话实探）

Grok 侧全名一律加前缀 `cocos-creator__`。下表是裸名。

| 工具 | 干什么 | 常用 action |
| --- | --- | --- |
| `cocos_scene` | 开/存/建场景，层级，撤销组，脚本探测 | `is_ready` `get_info` `list` `open` `save` `create` `hierarchy` `is_dirty` `validate_scene` `list_components` `undo_begin`/`undo_end` |
| `cocos_node` | 节点 CRUD、变换、挂脚本、剪贴板 | `find` `info` `list` `tree` `create` `delete` `modify` `batch_modify` `move` `reorder` `mount_script` `remove_script` |
| `cocos_component` | 组件增删和属性；点事件 | `add` `remove` `list` `info` `set_property` `available_types` `click_event` `batch_click_event` |
| `cocos_prefab` | 预制体全生命周期（删预制体也走这里，不走 asset） | `list` `info` `create` `instantiate` `apply` `revert` `edit_enter` `edit_save` `edit_exit` |
| `cocos_asset` | 资源查询/导入/路径↔UUID | `query_uuid` `query_path` `query_url` `find_by_name` `search` `import` `import_folder` `dependencies` |
| `cocos_editor` | 工程信息、日志、预览、构建面板、MCP 端口 | `project_info` `project_settings` `run` `stop` `build` `open_build_panel` `console_logs` `server_status` |
| `cocos_view` | 视口、Gizmo、2D/3D、参考图 | `mode_2d_3d` `camera_focus` `camera_align_node` `ref_add` `ref_list` |
| `cocos_builder` | 一次 JSON 树搭完整层级 | `build`（复杂 UI 用这个，不要一层层 `node.create`） |
| `cocos_composite` | 一键 Button/Label/Image，挂脚本并绑属性 | `create_ui` `create_button` `mount_and_bind` `setup_widget` `batch_create_*` |
| `cocos_template` | 现成 UI 壳 | `list` `apply`（`dialog` / `scroll_list` / `nav_bar` / `settings_page`） |
| `cocos_animation` | 剪辑、关键帧、预设 | 先在 Creator **打开动画面板**；写之前 `query_edit_info` 拿 `clipUuid`。优先 `batch_file` / `preset` |
| `cocos_spine` | `sp.Skeleton` | `list_animations` `set_animation` `set_skin` `set_data` |
| `cocos_label` | Label / RichText / EditBox | `set_text` `set_font` `set_style` `set_outline` `batch_set_font` |
| `cocos_knowledge` | 组件属性、UI 规则、tool_guide | `topic`：`tool_guide` `component_properties` `ui_design_rules` `layout_patterns` `best_practices` |
| `cocos_validate` | 深检查（不是 scene.validate_scene） | `layout` `references` `hierarchy` |
| `cocos_capture` | 场景 JSON 快照 + 截图 | `scene_snapshot` `node_snapshot` `screenshot`（像素对比用 `mode=content` + `scenePath`） |

`cocos_scene.validate_scene` 只查断裂引用。布局重叠、出屏、层级深度用 `cocos_validate`。

卸脚本用 `cocos_node action=remove_script`，不要 `cocos_component.remove`。看组件属性用 `info`，没有 `get_properties`。

## 本工程起手

空场景第一刀已过：当前打开的是 `scene`，节点数可以为 0。

```text
1. cocos_editor  action=project_info      确认工程是 midnightroad
2. cocos_scene   action=is_ready
3. cocos_scene   action=get_info
4. cocos_scene   action=hierarchy
5. 要改东西 → MCP 工具；改完 save + validate_scene
```

当前设计分辨率已是 **720×1280**（竖屏，`fitWidth`）。和契约「画布」一致。改 Canvas / 机位前仍先读一次 `project_info`，不要手写另一套数。

## 典型调用

查场景：

```json
{ "action": "hierarchy", "includeComponents": true }
```

在 Canvas 下建按钮（有 Canvas 之后）：

```json
{ "action": "create", "name": "StartButton", "parent": "Canvas", "type": "Button" }
```

一次搭一棵树：

```json
{
  "action": "build",
  "parent": "Canvas",
  "tree": {
    "name": "Hud",
    "children": [
      { "name": "Score", "type": "Label" }
    ]
  }
}
```

查 UUID：

```json
{ "action": "query_uuid", "url": "db://assets/scene.scene" }
```

看画面（改完要先存场景；`content` 模式吃的是上次 web 构建）：

```json
{
  "action": "screenshot",
  "mode": "content",
  "scenePath": "db://assets/scene.scene",
  "rebuild": true
}
```

## 十二个模块（对照 README，方便找工具）

| 模块 | 主要工具 |
| --- | --- |
| 场景管理 | `cocos_scene` |
| 节点操作 | `cocos_node` |
| 组件系统 | `cocos_component` |
| 预制体 | `cocos_prefab` |
| 资源管理 | `cocos_asset` |
| 编辑器控制 | `cocos_editor` |
| 场景视图 | `cocos_view` |
| UI 与模板 | `cocos_builder` `cocos_composite` `cocos_template` |
| 动画 / Spine | `cocos_animation` `cocos_spine` |
| 知识库 | `cocos_knowledge` |
| 验证与快照 | `cocos_validate` `cocos_capture` `cocos_scene.validate_scene` |
| 字体与 Label | `cocos_label` |

## 挂了怎么查

| 现象 | 先看 |
| --- | --- |
| Grok 没有 16 个 cocos 工具 | 是不是旧会话；Creator 面板在不在；`~/.grok/config.toml` 的 url |
| 工具在但全失败 | `cocos_editor action=server_status`；端口是不是还和 `settings/mcp-server.json` 一致 |
| 场景没准备好 | `cocos_scene action=is_ready`，再 `open` |
| 资源导入失败 | `cocos_scene action=validate_scene`，不要手改 meta |
| 动画写不进去 | Creator 动画面板没开；先 `query_edit_info` |
| 想发微信包 | 回到编辑器「发布到微信小游戏」，见 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md) |

插件面板：Creator 菜单 **扩展 → Cocos MCP Server**。`INSTALL.md` 还写了工具管理器（可开关单个工具）；本项目保持默认 16 个全开。
