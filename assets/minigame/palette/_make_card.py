#!/usr/bin/env python3
"""Render the locked 游戏01 card. Hex labels are drawn with code, not a model."""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 960, 640
P = 2

CANON = [
    ("霓虹青", "#22e6da", (34, 230, 218)),
    ("琥珀", "#fabf37", (250, 191, 55)),
    ("品红", "#e90cbe", (233, 12, 190)),
    ("电蓝", "#2a4ac5", (42, 74, 197)),
    ("夜靛", "#1d2c6b", (29, 44, 107)),
]
TRACK = [
    ("底", "#0a0d16", (10, 13, 22)),
    ("暮底", "#1c1430", (28, 20, 48)),
    ("店招红", "#ee190b", (238, 25, 11)),
]


def font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in (
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def snap(n: int) -> int:
    return (n // P) * P


def main() -> None:
    img = Image.new("RGB", (W, H), (10, 13, 22))
    d = ImageDraw.Draw(img)
    title = font(28)
    body = font(18)
    small = font(15)

    d.rectangle((0, 0, W, 72), fill=(29, 44, 107))
    d.text((24, 18), "真夜中道路 · 色卡 游戏01", font=title, fill=(34, 230, 218))
    d.text((24, 50), "TaiT 菜单只用上排五色。下排仅赛道工作色。", font=small, fill=(250, 191, 55))

    def swatches(items, y0, caption):
        d.text((24, y0), caption, font=body, fill=(233, 12, 190))
        gap = 16
        box = 150
        x = 24
        y = y0 + 32
        for name, hx, rgb in items:
            d.rectangle((x, y, x + box, y + 88), fill=rgb)
            d.rectangle((x, y, x + box, y + 88), outline=(42, 74, 197), width=2)
            ink = (10, 13, 22) if sum(rgb) > 360 else (231, 245, 254)
            d.text((x + 8, y + 10), name, font=body, fill=ink)
            d.text((x + 8, y + 52), hx, font=small, fill=ink)
            x += box + gap

    swatches(CANON, 96, "菜单 / HUD / CRT  ·  游戏01")
    swatches(TRACK, 260, "赛道另开  ·  底 / 暮底 / 店招红")

    d.rectangle((24, 420, W - 24, H - 24), outline=(42, 74, 197), width=2)
    rules = [
        "像素格 p = 2px（720 短边 / 360）。菜单与赛道共用边长，不共用畸变。",
        "CRT 桶形、扫描线、tait-crt-interface-skill 签名只出现在菜单。",
        "赛道禁止新色相。点阵只用同色相明暗阶（见 youxi-01.json dither_steps）。",
        "图层分 00 天空 … 08 HUD，见 assets/minigame/layers/stack.json。",
    ]
    yy = 436
    for line in rules:
        d.text((36, yy), line, font=small, fill=(34, 230, 218))
        yy += 36

    out = ROOT / "youxi-01-card.png"
    img.save(out)
    print("wrote", out)


if __name__ == "__main__":
    main()
