# 附录 · 微信小游戏新手教程

一手来源（2026-08-17 本机 HTTPS 拉页）：  
https://developers.weixin.qq.com/minigame/dev/guide/develop/start.html  

官方标题是「学习新手教程」。Clash fake-ip 时抓取工具会把该域判成内网，以本机 200 页面为准。进阶见 https://developers.weixin.qq.com/minigame/dev/guide/develop/develop.html  

和本项目的关系：真夜中道路用 **Cocos Creator 导出包**，再按本文「导入小游戏项目」进微信开发者工具。不要把文中的飞机示例当正式包骨架。平台总览仍看 [wechat-minigame-platform.md](wechat-minigame-platform.md)。Creator 构建面板逐步说明见 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md)。

## 注册小游戏账号

1. 去注册页注册**小程序**账号。  
2. 类目选 **游戏**。选完该账号就是小游戏账号。  
3. **一级类目不能改**，选错只能重开号。

## 下载开发者工具

https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html  

- 要新能力：开发版  
- 要稳：稳定版  

打开后用注册号对应的微信扫码进开发环境。

## 创建小游戏项目

工具左侧选「小游戏」，点 `+`。

| 项 | 官方说法 |
| --- | --- |
| 名称 / 目录 | 可改；目录用本机空目录 |
| AppID | 下拉选刚注册的号 |
| 云服务 | 可勾「不使用」，以后再用 |
| 测试号 | 没 AppID 时先点「测试号」体验。**不能验商业化、不能上传发布**，其余可玩 |

创建后进可视化开发界面。界面说明见开发者工具主界面介绍。

## 导入小游戏项目（Cocos / Unity / Laya）

引擎侧先导出小游戏代码包，工具里点 **导入**，选对应文件夹。

- 导入目录里**必须有** `project.config.json`  
- Unity 导出常见结构是 `minigame/` + `webgl/`：**要选 `minigame/`**，不要选上一层  

Cocos 同理：导入 Creator 构建出来的微信小游戏目录（含 `project.config.json` 的那一层），不是整个 Creator 工程根。

## 小游戏项目结构

最小四件：

```
├── game.js
├── game.json
├── project.config.json
└── project.private.config.json
```

| 文件 | 干什么 |
| --- | --- |
| `project.config.json` / `project.private.config.json` | 项目编辑配置 |
| `game.json` | 运行时配置 |
| `game.js` | 逻辑主入口；示例里其它代码和资源都由它引用 |

若 `project.config.json` 里配了 `miniprogramRoot`，则 `game.js` / `game.json` 可以不和 `project.config.json` 同级。选「微信云开发」模板时，游戏文件在 `miniprogram/` 下。

## 飞机示例：只当思路，不当线上骨架

官方原话：默认飞机示例本质是 **Canvas2D**，本文只讲开发思路，**不推荐线上用该示例**，更推荐 **Unity、Cocos 或 Laya**。

示例入口：`game.js` → `js/main.js` 的 `Main`。想写 Web 风格需自行引入 `weapp-adapter`（不是基础库，模拟不完整）。

官方拆的八步（引擎会替你包掉其中大部分）：

1. **初始化 Canvas**：`wx.createCanvas()` + `getContext("2d")`。**第一次调用是上屏画布，之后都是离屏。** Adapter 里通常会先建好主屏 Canvas。  
2. **游戏初始化**：拼背景 / 玩家 / UI，监听重开，`start()`。  
3. **帧循环**：`requestAnimationFrame` → `update()` 算逻辑 → `render()` 清屏再画。  
4. **数据和状态**：示例用 `DataBus` 管分和是否结束。  
5. **对象**：玩家 / 敌机 / 子弹都继承 `Sprite`，各自 `update` / `render`。  
6. **交互**：`wx.onTouchStart/Move/End/Cancel`。示例是按住飞机区域再拖，用触摸坐标改飞机 x/y。  
7. **反馈**：碰撞时播爆炸动画、音效、震动。  
8. **总结**：架构、状态、对象要分开。熟悉概念后去读引擎文档；引擎已封装对象和帧循环。

对本项目：这些步骤由 Cocos 负责。我们验收的是 **Creator 导出目录能被开发者工具导入并跑**，不是手写一套 `Main.loop`。

## 和本仓库的对照

| 官方新手教程 | 真夜中道路 |
| --- | --- |
| 游戏类目账号 | 已注册，备案并行 |
| 开发者工具创建 / 导入 | 用 Cocos 导出包 **导入**，不要从飞机模板开正式工程 |
| `game.js` 主入口 | 由 Creator 构建生成，不手搓 IIFE |
| 不推荐 Canvas2D 示例上线 | 与已锁的「Cocos工程」一致 |
| 测试号不能上传、不能验商业化 | 激励续命、广告必须用正式 AppID 才验得了 |

## 尚未从该页抽出、不要当事实

- 主包 / 分包体积上限（本页没写死数字）  
- Cocos 当前构建面板的默认输出文件夹名（以本机 Creator 构建结果为准）  
