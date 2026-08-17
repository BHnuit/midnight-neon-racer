# 部署流程

给 grokbot / 后续开发者。不要把 Netlify token、GitHub token、账号密码写进仓库。

## 生产站点（已存在，禁止另建）

| 项 | 值 |
| --- | --- |
| 正式 URL | https://racer.bhnuit.cn |
| 备用 URL | https://euphonious-sprinkles-1c5a7d.netlify.app |
| site name | `euphonious-sprinkles-1c5a7d` |
| site id | `31c60f42-99a4-4890-a9a3-aa50ff2c7c92` |
| DNS zone | `bhnuit.cn`（Netlify DNS，zone `678f3df283aa15e6ccad9022`） |
| 账号 | BH Nuit / 已登录本机 Netlify CLI |

`*.netlify.app` 在微信里会被拦截。对外只发 `https://racer.bhnuit.cn`。

## 第一次在本机挂钩站点

`netlify deploy --prod` 在没有 site 链接时会**静默新建一个站**。必须先写回 siteId：

```bash
mkdir -p .netlify
printf '{"siteId":"31c60f42-99a4-4890-a9a3-aa50ff2c7c92"}\n' > .netlify/state.json
cat .netlify/state.json   # 部署前必须确认
```

`.netlify/` 已 gitignore，不要把 CLI 缓存提交上去。

## 发到生产

```bash
npm install
netlify deploy --dir . --functions netlify/functions --prod
```

依赖必须在**仓库根** `package.json`（`@netlify/blobs`）。放到 `netlify/functions/package.json` 不会被装进函数包。

## 自定义域名（已绑好，一般不用再跑）

CLI 的 `updateSite` 改 `custom_domain` **不生效**。必须 PATCH：

```bash
# token 只从本机读,不要写进仓库
TOKEN=$(python3 -c "import json; d=json.load(open('$HOME/.config/netlify/config.json')); print(d['users'][list(d['users'].keys())[0]]['auth']['token'])")
curl -s -X PATCH "https://api.netlify.com/api/v1/sites/31c60f42-99a4-4890-a9a3-aa50ff2c7c92" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"custom_domain":"racer.bhnuit.cn"}'
```

域名在 Netlify DNS 托管时，这一下会自动建 NETLIFY 记录并签 Let's Encrypt。不要走 `createDnsRecord`（会 422）。

## 排行榜 Functions + Blobs

- 路径：`/.netlify/functions/leaderboard`
- GET 拉榜，POST `{name, score, carId}` 提交
- Lambda 兼容模式必须 `connectLambda(event)` 再 `getStore('leaderboard')`
- 前端 GET 必须带 `?t=Date.now()` 且 `cache: 'no-store'`，否则会吃到 CDN 空榜
- 清测试数据（本机，不要提交脚本里的 token）：

```bash
TOKEN=... SITE=31c60f42-99a4-4890-a9a3-aa50ff2c7c92 node -e '
const { getStore } = require("@netlify/blobs");
const store = getStore({ siteID: process.env.SITE, token: process.env.TOKEN, name: "leaderboard" });
store.delete("leaderboard").then(() => console.log("cleaned"));
'
```

## 验证

交互页不能只 curl 200。改完必须：

```bash
npm test
```

30 项 Playwright：物理 6 + 幻影 10 + 回归 14。

## 误建新站怎么删

```bash
netlify api deleteSite --data '{"site_id":"<误建的 id>"}'
```

2026-08-17 踩过：`lucky-hamster-db18c2`（已删）。

## NAS DNS 不可信

本机 Clash fake-ip 会把解析变成 `198.18.x.x`。查公网解析走 `ssh tencentvps` 或换一台没劫持的机器。
