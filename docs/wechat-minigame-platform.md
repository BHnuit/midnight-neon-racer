# 微信小游戏平台（2026-08-18 复核笔记）

一手来源：微信开放文档。本机 Clash fake-ip 导致部分抓取工具把 `developers.weixin.qq.com` 判成内网；正文以本机 HTTPS 200 页面为准。

## 平台是什么

微信小游戏是**小程序的一个类目**，不是 H5 网页、也不是把现有站点嵌进微信。不下载安装、强调「用完即走」，并依赖微信社交传播。

- 介绍：https://developers.weixin.qq.com/minigame/introduction/
- 接入：https://developers.weixin.qq.com/minigame/introduction/guide/
- 开发指南：https://developers.weixin.qq.com/minigame/dev/guide/
- 新手教程：https://developers.weixin.qq.com/minigame/dev/guide/develop/start.html（正文摘进 [wechat-minigame-start.md](wechat-minigame-start.md)）
- 运营规范：https://developers.weixin.qq.com/minigame/product/

## 运行时（和本仓库的冲突）

官方项目骨架是 `game.js` + `game.json` + `project.config.json`。用引擎时走「导入」：目录里必须有 `project.config.json`。详见 [wechat-minigame-start.md](wechat-minigame-start.md)。

iOS 用 JavaScriptCore、Android 用 V8：**没有 BOM/DOM，没有 `document` / `window`**。画布用 `wx.createCanvas()`，首次调用才是上屏画布。

官方示例是 Canvas2D 飞机大战，文档写明**不推荐线上用该示例**，更推荐 Unity / Cocos / Laya。若要以 Web 风格写，需自行引入 `weapp-adapter`（不是基础库的一部分，模拟不完整）。

- Adapter：https://developers.weixin.qq.com/minigame/dev/guide/runtime/adapter.html
- 引擎适配：https://developers.weixin.qq.com/minigame/dev/guide/game-engine/engine-overview.html
- 进阶：https://developers.weixin.qq.com/minigame/dev/guide/develop/develop.html
- Cocos 发布到微信小游戏：https://docs.cocos.com/creator/3.8/manual/zh/editor/publish/publish-wechatgame.html（正文摘进 [cocos-publish-wechatgame.md](cocos-publish-wechatgame.md)）

对本 demo 的直接含义：`index.html` 的 CSS HUD、DOM 菜单、Google Fonts、`navigator.share`、直接 `fetch` Netlify、浏览器 `AudioContext` **不能原样上架**。画布循环和 WebAudio 思路可迁，但要换成 `wx` API（平台提供 `wx.createWebAudioContext`）。

## 上架两条路

开发可以和审核并行，流程只挡发布。

| 路径 | 含义 | 官方预估 |
| --- | --- | --- |
| IAA | 靠广告赚钱，不承诺将来开虚拟支付 | 约 13–37 个工作日 |
| IAP | 靠虚拟支付，需先有《网络游戏出版物号核发单》（版号） | 约 9–22 个工作日（不含拿版号） |

发布前必须：**版本审核 + 备案**。企业主体必须先微信认证才能提交小程序备案。

IAA 备案还要走「小游戏备案」（主管部门约 10–20 个工作日）再走「小程序备案」（IAA 约 10–30 个工作日）。名称含英文或「软件」字样时，IAA 备案可能要《计算机软件著作权登记证书》。

- IAA：https://developers.weixin.qq.com/minigame/introduction/guide/iaa.html
- IAP：https://developers.weixin.qq.com/minigame/introduction/guide/iap.html
- 版本审核：https://developers.weixin.qq.com/minigame/introduction/guide/bbsh.html
- 小游戏备案：https://developers.weixin.qq.com/minigame/introduction/guide/nrjs.html
- 小程序备案：https://developers.weixin.qq.com/minigame/introduction/guide/xcxba.html
- IAA 资质：https://developers.weixin.qq.com/minigame/introduction/guide/zzsh-iaa.html

## 账号与类目

注册时必须勾选一级类目「游戏」，**选错只能重新注册**。二级类目发布前可改（文化互动除外），发布后不可改。个人主体暂不支持文化互动、角色类、牌类。

运营规范：功能不能过于简单、不能与其他小游戏同质化严重；核心功能必须在首页体现；禁止强制/诱导分享。

- 类目：https://developers.weixin.qq.com/minigame/introduction/guide/type.html

## 社交与后端

官方能力地图把「好友关系 / 排行榜」指向**关系链 + 开放数据域**（`wx.setUserCloudStorage` / `wx.getFriendCloudStorage`），不是任意全球公开榜。现有 Netlify Blobs 全局榜若要保留，必须自建 HTTPS 且域名 **ICP 备案**，并在后台配置 request 合法域名；或改用微信云开发/云托管以免配域名。

- 排行榜：https://developers.weixin.qq.com/minigame/dev/guide/open-ability/ranklist.html
- 网络：https://developers.weixin.qq.com/minigame/dev/guide/base-ability/network.html

## 尚未从文档抽出、不要当事实

- Cocos Creator 3.8 当前发布页写明主包不超过 4MB，但提审前仍要回微信官方后台/文档复核当时限制；本笔记不锁分包数量与单包上限
- 正式广告位、上传私钥、软著或其他后台资质的当前可用状态；已确认的是个人主体账号已注册、走 IAA
