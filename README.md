# 午夜霓虹 · 极速赛车

单文件 canvas 赛车小游戏。线上：https://racer.bhnuit.cn

对向车会变道（带转向灯），排行榜记录会以幻影车同场陪跑。微信可打开（自有域名，不用 `*.netlify.app`）。

## 本地玩

直接打开 `index.html`，或：

```bash
python3 -m http.server 8001
# http://127.0.0.1:8001/
```

离线也能玩。排行榜需要 Netlify Functions，本地静态打开时榜为空。

## 仓库结构

```
index.html                      # 游戏本体（CSS/JS 全内联）
netlify/functions/leaderboard.js  # GET 拉榜 / POST 提交
netlify.toml                    # publish + functions
package.json                    # @netlify/blobs + npm test
tests/                          # Playwright 端到端（30 项）
DEPLOY.md                       # 部署与域名
AGENTS.md                       # 给 grokbot / 后续 Agent 的交接
```

## 测试

需要 Python 3 + Playwright：

```bash
python3 -m venv .venv
.venv/bin/pip install playwright
.venv/bin/playwright install chromium
npm test
```

`tests/run.sh` 会优先用仓库 `.venv`，其次本机 `/tmp/ptest-venv`。没有 Playwright 会直接报缺模块。

默认打线上 `https://racer.bhnuit.cn/`。改目标：

```bash
RACER_URL=http://127.0.0.1:8001/ npm test
```

若本机 Chromium 不在默认路径：

```bash
export PLAYWRIGHT_CHROMIUM=/path/to/chrome
```

## 部署

见 [DEPLOY.md](DEPLOY.md)。要点：

- 站点已经存在，**不要新建站**
- site id `31c60f42-99a4-4890-a9a3-aa50ff2c7c92`
- 正式地址 `https://racer.bhnuit.cn`（Netlify DNS 自动签 SSL）
- 交付前必须真浏览器测，不能只 curl 200

## 授权

MIT。作者 BHnuit / Hant。
