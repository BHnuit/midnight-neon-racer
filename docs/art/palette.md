# 色卡 · 游戏01

权威文件：

| 文件 | 用途 |
| --- | --- |
| [youxi-01.json](../../assets/minigame/palette/youxi-01.json) | 机器可读 |
| [youxi-01.gpl](../../assets/minigame/palette/youxi-01.gpl) | 给画板 |
| [youxi-01-card.png](../../assets/minigame/palette/youxi-01-card.png) | 给人看的本项目卡 |
| [tait-color-card.png](../../assets/minigame/palette/tait-color-card.png) | TaiT 全卡副本，选卡时对照 |

来源是 `tait-crt-interface-skill` 的 **游戏01**。菜单生成仍按 TaiT 两段式入口，默认回复「游戏01」。不要改成「如图」除非 Hans 明确换卡。

## 两套用法，不要混

| 表面 | 能用的色 | 禁止 |
| --- | --- | --- |
| 菜单 / 选车 / 结算 CRT | 游戏01 五色整卡 | 底、暮底、店招红、任何插值灰、渐变、半透明 |
| 赛道 / 车 / 天气 | 五色 + 底 `#0a0d16` + 暮底 `#1c1430` + 店招红 `#ee190b` + 同色相明暗阶 | 新色相、写实金属、无关的黄 |
| 局内 HUD 数字和条 | 只用五色 | 不要 CRT 桶形，不要签名 |

店招红从 `assets/wechat-avatar-144.png` 取样，只给跑车车身。别的车以后各锁一色，仍走同卡约束。

## 角色

| 色 | hex | 菜单 | 赛道 |
| --- | --- | --- | --- |
| 霓虹青 | `#22e6da` | 窗亮、标题 | HUD 正常态 |
| 琥珀 | `#fabf37` | 警告 | 分数、技能条烫 |
| 品红 | `#e90cbe` | 热键/强调 | 路缘、氮光带、尾灯落光 |
| 电蓝 | `#2a4ac5` | 面板 | 远楼 |
| 夜靛 | `#1d2c6b` | 底场 | 远景并色 |
| 底 / 暮底 | `#0a0d16` / `#1c1430` | 不用 | 天顶、路面基色 |
| 店招红 | `#ee190b` | 不用 | 跑车 |

点阵只能在同色相里走明暗阶，见 json 里的 `dither_steps`。近处 cell 3–4px，中 2px，远 1px（[修订 01](../art-bible-revision-01.md) §7）。

## 验收

出一张菜单或一张赛道图之后：

1. 菜单图量化到游戏01 五色，图外不允许出现其它 hex。
2. 赛道图允许工作色，但不允许新色相。
3. HUD 数字只用青 / 琥珀 / 品红。
