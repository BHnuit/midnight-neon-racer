# 附录 · 发布到微信小游戏（Cocos）

一手来源（2026-08-17 本机 HTTPS 拉页）：  
https://docs.cocos.com/creator/4.0/manual/zh/editor/publish/publish-wechatgame.html  

官方标题是「发布到微信小游戏」，挂在 Creator **4.0 LTS** 手册下。同路径的 3.8 页与之同文；文中写明「Cocos Creator 3.8 中，将引擎相关的构建选项统一到了引擎设置」。本机工程是 **3.8.6**，按这篇点构建即可。

微信侧导入规则仍看 [wechat-minigame-start.md](wechat-minigame-start.md)。第一刀过线看 [cocos-slice-a.md](cocos-slice-a.md)。

## 引擎替你做了什么

微信小游戏运行环境是小程序环境的扩展，有 WebGL 封装，**不等于浏览器**。Cocos 承诺：

- 引擎框架已适配微信 API，纯游戏逻辑一般不用再改一层
- 编辑器可直接发布为微信小游戏，并能唤起开发者工具
- 自动加载远程资源、缓存、缓存版本控制

提交、审核、发布和小程序同一套微信流程。平台要求见 [wechat-minigame-platform.md](wechat-minigame-platform.md)。

## 环境配置

1. 安装 [微信开发者工具](https://developers.weixin.qq.com/miniprogram/dev/devtools/download.html)  
2. Creator 主菜单 **Cocos Creator / 文件 → 偏好设置 → 外部程序**，填开发者工具路径  
3. 登录[微信公众平台](https://mp.weixin.qq.com/)拿 AppID  

第一次若没单独开过开发者工具，点构建任务的「运行」可能报 `Please ensure that the IDE has been properly installed`。先手动打开一次开发者工具。

## 发布流程（对应第一刀）

1. 打开 `midnightroad` 工程  
2. **项目 → 构建发布**，发布平台选 **微信小游戏**  
3. 设好选项后点 **构建**  
4. 构建任务左下角文件夹图标：默认在工程 `build/` 下生成 `wechatgame`（以任务名为准），里面已有 `game.json`、`project.config.json`  
5. 构建任务右下角 **运行**：打开微信开发者工具  

导入时选这一层（有 `project.config.json` 的目录），不要选整个 Creator 工程根。

## 主包设置

| 面板项 | 作用 |
| --- | --- |
| 初始场景分包 | 首场景及依赖进 `assets/start-scene`，加快首屏 |
| 资源服务器地址 | 填远程资源地址；构建后须**手动**把发布包里的 `remote/` 上传上去 |

## 引擎设置（3.8 起归在一栏）

| 面板项 | 作用 |
| --- | --- |
| CLEANUP_IMAGE_CACHE | 纹理上传 GPU 后删内存；删了就不能动态合图 |
| 物理系统 | 发布以当前选择为准 |
| WebGL 2.0 | 选 WebGL 版本 |
| 原生代码打包模式 | 管 Spine、物理等 wasm/asmjs；默认最优，无故别改 |
| Wasm 3D 物理（ammo.js） | 项目设置里 3D 物理为 bullet 时生效 |
| 引擎原生代码分包 | WASM/Asm.js 进子包，减小主包 |
| 启用 WASM Brotli 压缩 | 体积更小，加载时多一点解压时间 |

第一刀空场景：保持默认即可，不必开远程资源、不必开开放数据域。

## 构建选项

| 面板项 | 作用 |
| --- | --- |
| 设备方向 | Portrait / Landscape，写入 `game.json`。本项目用 **Portrait** |
| AppID | **必填**。面板默认 `wx6ac3f5090a6b99c5` 只用于测试。写入 `project.config.json`。真夜中道路用自己的号；没有就测试号，不能上传、不能验广告 |
| 生成开放数据域工程模板 | 好友榜以后再开，见官方「开放数据域」 |
| 分离引擎 | 是否用微信小游戏引擎插件 |
| 高性能模式 | 微信高性能模式 |

## 资源管理（官方硬限制）

- **主包不能超过 4MB**（代码 + 资源）。多出来的必须网络下载  
- 包体过大就配「资源服务器地址」，资源上远程  
- 包内资源不是按需加载，而是**一次加载完再进页**  
- **不能从远程服务器下载脚本**  

主包资源都放到远程时，勾「初始场景分包」，首场景会留在本地 `assets/start-scene`，启动更快。

远程下载、缓存、版本由引擎缓存管理器处理。分包见官方「小游戏分包」。

## 平台 SDK

用户、登录、支付、转发、上传下载、媒体、定位等是微信环境里的原生能力，**引擎不包移植**，要自己接 `wx`。第一刀不接。好友榜以后走开放数据域，不走 Demo 的 Netlify 全球榜。

## WebAssembly

3.0 起有「Wasm 3D 物理（ammo.js）」，仅当项目设置 → 功能裁剪 → 3D 物理为 bullet 时生效。默认开 wasm；关掉用 js。

注意（官方原文）：

- 微信小游戏引擎插件目前仅支持 js 模式  
- 微信版本 ≥ v7.0.17  
- 开发者工具调试基础库 ≥ v2.12.0  

本项目是 2D 公路，第一刀不必开 3D 物理。

## 限制

官方写明：**微信小游戏不支持 WebView**。

## 官方参考（该页列出）

- 微信小游戏开发文档  
- 微信公众平台  
- 小游戏 API  
- 微信开发者工具下载与文档  

## 尚未从该页抽出、不要当事实

- 当前微信后台对分包数量/单个分包上限的最新数字（本页只写主包 4MB）  
- Creator 构建面板里「微信开发者工具」路径在你这台机器上的实际值  
