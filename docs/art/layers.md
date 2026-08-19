# 图层栈

预览和局内都按同一叠法。底板上不要再烧车、不要再烧氮光带、不要再烧数字。

目录：[assets/minigame/layers/](../../assets/minigame/layers/)，机器表是 [stack.json](../../assets/minigame/layers/stack.json)。

```
08  HUD          心 / 保险杠 / 技能条 / 数字
07  FX           天气粒子、尾灯落光、车底压印、加分
06  cars         玩家车、对向车、道具
05  nitro        氮光带（默认关）
04  road         行车面 + 三车道线
03  near         护栏、路肩
02  mid          路侧楼、路灯
01  far          远城剪影
00  sky          天色横带、月亮、空天
```

画布 720×1280，透明 PNG，偶数坐标。合成时从 00 画到 08。

## 谁负责切换

| 层 | 何时换 | 换什么 |
| --- | --- | --- |
| 00 sky | 天色随路程 | dusk / night / dawn 三张，或一张加横向扫带 |
| 01 far | 路段主题 | 城区 / 桥 / 隧道剪影 |
| 02 mid | 路段主题 | 楼和灯的排布 |
| 03 near | 路段宽窄 | 护栏左右同 `d` |
| 04 road | 路宽变化 | 仍是三车道；变窄变宽不能画成双车道 |
| 05 nitro | 按住氮 | `off` 空层，`on` 两侧品红光带 |
| 06 cars | 每帧 | 只放精灵，不画进 00–05 |
| 07 fx | 天气整局一种；接地每帧 | 粒子 + [修订 01](../art-bible-revision-01.md) §5 |
| 08 hud | 每帧 | 数字和条，位图字 |

天气只改 07 和一层染色，不改 04 的路形。氮光带只改 05。

## 透视

00 可以没有消失点（天）。01–05 里 **凡是与路平行的线**，延长后必须落在 `(376, 700)` ±20px（试玩修订 A-2 已锁）。

`02-mid` 不要交一张烤死透视的街景。密的城用 128×2048 纵向街墙，能认的房子用卡片，运行时按 1/z 推近。见 [roadside-approach.md](roadside-approach.md)。

`00-sky` 必须有空天件，目录见 [sky-catalog.md](sky-catalog.md)。车的落光和残影在 `07-fx`，见 [car-grounding.md](car-grounding.md)。

## 现有预览怎么算

`play-night-3lane.jpg` 和 `play-night-3lane-nitro.jpg` 是烤在一起的样张，风格可留，**不能当图层源**。下一张可用预览必须按本栈分文件交，再用脚本合成。

## 交付

每层：

1. `assets/minigame/layers/<id>/<name>.png`（透明）
2. 同目录 `manifest.md`：文件名、对应切换键、格子尺寸、未修好的缺陷
