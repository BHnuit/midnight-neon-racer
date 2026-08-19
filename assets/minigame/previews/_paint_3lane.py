#!/usr/bin/env python3
"""Paint a clean 3-lane road on the night city plate.

Covers every leftover 2-lane mark, then draws exactly four markings
that share one vanishing point: two solid curbs + two dashed dividers.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "assets/minigame/previews/bg-night-empty.jpg"
CAR = ROOT / "assets/minigame/cars/paoche/paoche-rear.png"
OUT_EMPTY = ROOT / "assets/minigame/previews/bg-night-3lane-empty.jpg"
OUT_PLAY = ROOT / "assets/minigame/previews/play-night-3lane.jpg"
OUT_NITRO_EMPTY = ROOT / "assets/minigame/previews/bg-night-3lane-nitro.jpg"
OUT_NITRO = ROOT / "assets/minigame/previews/play-night-3lane-nitro.jpg"
OUT_DEBUG = Path("/tmp/lane-debug.png")

W, H = 720, 1280
# 历史修订 01 · A 预览；当前运行时与新素材规格已升级为 A-2。
VX, VY = 376, 797

# Driving surface sized so the locked car sits in the center lane.
CAR_Y = int(H * 0.80)  # 1024, sprite bottom
LANE_AT_CAR = 340
DRIVE_HALF_AT_CAR = LANE_AT_CAR * 1.5  # 300 → 600px road at the car
T_CAR = (CAR_Y - VY) / (H - VY)
MOUTH_L = VX - DRIVE_HALF_AT_CAR / T_CAR
MOUTH_R = VX + DRIVE_HALF_AT_CAR / T_CAR

# Extra margin around the drive surface so the old center stripe is buried.
COVER_PAD = 22

BAYER8 = np.array(
    [
        [0, 32, 8, 40, 2, 34, 10, 42],
        [48, 16, 56, 24, 50, 18, 58, 26],
        [12, 44, 4, 36, 14, 46, 6, 38],
        [60, 28, 52, 20, 62, 30, 54, 22],
        [3, 35, 11, 43, 1, 33, 9, 41],
        [51, 19, 59, 27, 49, 17, 57, 25],
        [15, 47, 7, 39, 13, 45, 5, 37],
        [63, 31, 55, 23, 61, 29, 53, 21],
    ],
    dtype=np.float64,
) / 64.0

NEAR_PINK = np.array([255, 168, 226], dtype=np.float64)
MID_PINK = np.array([233, 12, 190], dtype=np.float64)
FAR_PINK = np.array([78, 42, 112], dtype=np.float64)
NEAR_CORE = np.array([255, 228, 246], dtype=np.float64)
BAND_NEAR = np.array([255, 58, 186], dtype=np.float64)
BAND_MID = np.array([233, 12, 190], dtype=np.float64)
BAND_FAR = np.array([132, 24, 108], dtype=np.float64)
BAND_HOT = np.array([255, 156, 220], dtype=np.float64)


def lerp_rgb(a: np.ndarray, b: np.ndarray, u: float) -> tuple[int, int, int]:
    u = max(0.0, min(1.0, u))
    c = a * (1.0 - u) + b * u
    return int(c[0]), int(c[1]), int(c[2])


def line_color(t: float) -> tuple[int, int, int]:
    """Near = hot pink/white, far = indigo. One family, no yellow jump."""
    if t < 0.45:
        return lerp_rgb(FAR_PINK, MID_PINK, t / 0.45)
    return lerp_rgb(MID_PINK, NEAR_PINK, (t - 0.45) / 0.55)


def hash01(x: int, y: int) -> float:
    n = (x * 374761393 + y * 668265263) & 0x7FFFFFFF
    return (n % 10007) / 10007.0


def asphalt_px(x: int, y: int, t: float, shoulder: bool) -> tuple[int, int, int]:
    n = float(BAYER8[y & 7, x & 7])
    h = hash01(x, y)
    v = 0.62 * n + 0.38 * h
    if shoulder:
        lo, base, hi = (14, 8, 30), (36, 20, 54), (78, 56, 96)
    else:
        lo, base, hi = (8, 4, 24), (20, 10, 42), (46, 28, 66)
    if v < 0.28:
        c = lo
    elif v > 0.74:
        c = hi
    else:
        c = base
    if t > 0.58 and h > 0.86:
        mag = (t - 0.58) / 0.42
        c = (
            min(255, c[0] + int(36 * mag)),
            c[1],
            min(255, c[2] + int(18 * mag)),
        )
    return c


def drive_edges(y: int) -> tuple[float, float]:
    t = (y - VY) / (H - VY)
    return VX + (MOUTH_L - VX) * t, VX + (MOUTH_R - VX) * t


def cover_edges(y: int) -> tuple[int, int]:
    dl, dr = drive_edges(y)
    return int(np.floor(dl - COVER_PAD)), int(np.ceil(dr + COVER_PAD))


def is_old_paint(rgb: np.ndarray) -> bool:
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    if r > 148 and r > g + 32 and b > 64:
        return True
    if r > 188 and g > 118 and b > 138 and r >= g:
        return True
    return False


def pink_run(row: np.ndarray, x: int) -> int:
    if not is_old_paint(row[x]):
        return 0
    a = x
    while a > 0 and is_old_paint(row[a - 1]):
        a -= 1
    b = x
    while b < W - 1 and is_old_paint(row[b + 1]):
        b += 1
    return b - a + 1


def dash_mask() -> np.ndarray:
    """Perspective-scaled dashes: long near the camera, short toward the VP."""
    mask = np.zeros(H, dtype=bool)
    acc = 0.0
    state = True
    period_near, period_far = 52.0, 7.0
    duty = 0.46
    for y in range(H - 1, VY + 12, -1):
        t = (y - VY) / (H - VY)
        period = period_far + (period_near - period_far) * (t**1.2)
        chunk = period * (duty if state else 1.0 - duty)
        mask[y] = state
        acc += 1.0
        if acc >= chunk:
            acc = 0.0
            state = not state
    return mask


def band_width(t: float) -> float:
    """Wide cyber sidewalks in the mid-ground, like the reference plate."""
    return 12.0 + 210.0 * (max(t, 0.0) ** 0.5)


def can_paint_band(rgb: np.ndarray, y: int, x: int) -> bool:
    r, g, b = int(rgb[0]), int(rgb[1]), int(rgb[2])
    lum = r + g + b
    if lum > 360 and abs(r - g) < 42 and abs(g - b) < 42:
        return False
    if lum > 400 and r > 180 and b > 140:
        return False
    if y < 800 and lum > 280 and (b > 100 or g > 80) and (x < 200 or x > 520):
        return False
    return True


def band_px(x: int, y: int, t: float, u_inner: float) -> tuple[int, int, int]:
    if t < 0.28:
        base = np.array(lerp_rgb(BAND_FAR, BAND_MID, t / 0.28), dtype=np.float64)
    else:
        base = np.array(lerp_rgb(BAND_MID, BAND_NEAR, min(1.0, (t - 0.28) / 0.50)), dtype=np.float64)
    hot = np.array(lerp_rgb(base, BAND_HOT, 0.55 + 0.35 * t), dtype=np.float64)
    n = float(BAYER8[(y * 3) & 7, x & 7])
    h = hash01(x + 17, y * 3)
    # Stretch grain vertically so the band feels like it's rushing past.
    v = 0.55 * n + 0.45 * h
    u = max(0.0, min(1.0, u_inner))
    c = base * (1.0 - 0.55 * u) + hot * (0.55 * u)
    if v < 0.22:
        c = c * 0.72
    elif v > 0.82:
        c = c * 0.78 + BAND_HOT * 0.22
    # Outer lip fades into the shoulder instead of a hard slab.
    if u < 0.12:
        c = c * (0.35 + 5.4 * u)
    return (
        int(max(0, min(255, c[0]))),
        int(max(0, min(255, c[1]))),
        int(max(0, min(255, c[2]))),
    )


def paint_band(px: np.ndarray, y: int, t: float, x_inner: float, x_outer: float, side: int) -> None:
    a = max(0, int(np.floor(min(x_inner, x_outer))))
    b = min(W - 1, int(np.ceil(max(x_inner, x_outer))))
    if b < a:
        return
    span = max(1, b - a)
    for x in range(a, b + 1):
        if not can_paint_band(px[y, x], y, x):
            continue
        u = (x - a) / span if side < 0 else (b - x) / span
        px[y, x] = band_px(x, y, t, u)


def paint_span(px: np.ndarray, y: int, xc: float, half: float, rgb: tuple[int, int, int]) -> None:
    x0 = max(0, int(np.floor(xc - half)))
    x1 = min(W - 1, int(np.ceil(xc + half)))
    if x1 < x0:
        return
    px[y, x0 : x1 + 1] = rgb
    # 1px lighter core when the stroke is thick enough
    if half >= 1.6:
        core = lerp_rgb(np.array(rgb, dtype=np.float64), NEAR_CORE, 0.45)
        cx0 = max(0, int(round(xc - max(0.4, half * 0.28))))
        cx1 = min(W - 1, int(round(xc + max(0.4, half * 0.28))))
        if cx1 >= cx0:
            px[y, cx0 : cx1 + 1] = core


def paint_road(base: Image.Image, nitro: bool = False) -> Image.Image:
    px = np.array(base.convert("RGB"))
    dashes = dash_mask()
    for y in range(VY + 3, H):
        t = (y - VY) / (H - VY)
        c0, c1 = cover_edges(y)
        c0 = max(0, c0)
        c1 = min(W - 1, c1)
        dl, dr = drive_edges(y)

        # 1) scrape leftover 2-lane paint (thin strokes only — keep railings / lamps)
        if y >= VY + 16:
            row = px[y]
            kill = np.zeros(W, dtype=bool)
            for x in range(W):
                if not is_old_paint(row[x]):
                    continue
                if y < 790 and (x < 270 or x > 450):
                    continue
                run = pink_run(row, x)
                # Railings live high and wide on the sides. Old lane edges are thinner.
                railing_zone = y < 870 and (x < 110 or x > 610)
                if railing_zone and run >= 18:
                    continue
                if run >= 90:
                    continue
                kill[x] = True
            for x in np.flatnonzero(kill):
                px[y, x] = asphalt_px(int(x), y, t, shoulder=True)

        # 2) rebuild only the driving surface (sharp trapezoid to the VP)
        for x in range(c0, c1 + 1):
            px[y, x] = asphalt_px(x, y, t, shoulder=(x < dl or x > dr))

        if nitro and t > 0.045:
            bw = band_width(t)
            paint_band(px, y, t, dl - 1.0, dl - bw, -1)
            paint_band(px, y, t, dr + 1.0, dr + bw, 1)

        curb_half = 1.0 + 5.5 * (t**1.05)
        dash_half = 0.55 + 2.2 * (t**1.15)
        rgb = line_color(min(1.0, t * (1.08 if nitro else 1.0)))

        if 0 <= dl < W:
            paint_span(px, y, dl, curb_half, rgb)
        if 0 <= dr < W:
            paint_span(px, y, dr, curb_half, rgb)

        if t > 0.07 and dashes[y]:
            paint_span(px, y, dl + (dr - dl) / 3.0, dash_half, rgb)
            paint_span(px, y, dl + 2.0 * (dr - dl) / 3.0, dash_half, rgb)
    return Image.fromarray(px, "RGB")


def composite_car(scene: Image.Image) -> Image.Image:
    car = Image.open(CAR).convert("RGBA")
    target_w = int(round(W * 0.24))
    scale = target_w / car.size[0]
    target_h = int(round(car.size[1] * scale))
    car = car.resize((target_w, target_h), Image.Resampling.NEAREST)
    x = (W - target_w) // 2
    y = CAR_Y - target_h
    out = scene.convert("RGBA")
    out.alpha_composite(car, (x, y))
    print(f"car {target_w}x{target_h} at ({x},{y}) bottom={y+target_h}")
    print(f"mouth {MOUTH_L:.1f}..{MOUTH_R:.1f} t_car={T_CAR:.3f}")
    print(f"drive at car: {drive_edges(CAR_Y)}")
    return out.convert("RGB")


def paint_debug() -> Image.Image:
    px = np.zeros((H, W, 3), dtype=np.uint8)
    dashes = dash_mask()
    for y in range(VY + 3, H):
        t = (y - VY) / (H - VY)
        dl, dr = drive_edges(y)
        curb_half = 1.0 + 5.5 * (t**1.05)
        dash_half = 0.55 + 2.2 * (t**1.15)
        paint_span(px, y, dl, curb_half, (255, 80, 180))
        paint_span(px, y, dr, curb_half, (255, 80, 180))
        if t > 0.055 and dashes[y]:
            paint_span(px, y, dl + (dr - dl) / 3.0, dash_half, (255, 220, 80))
            paint_span(px, y, dl + 2.0 * (dr - dl) / 3.0, dash_half, (255, 220, 80))
    return Image.fromarray(px, "RGB")


def main() -> None:
    src = Image.open(SRC)
    empty = paint_road(src, nitro=False)
    empty.save(OUT_EMPTY, quality=94, subsampling=0)
    composite_car(empty).save(OUT_PLAY, quality=94, subsampling=0)
    nitro_empty = paint_road(src, nitro=True)
    nitro_empty.save(OUT_NITRO_EMPTY, quality=94, subsampling=0)
    composite_car(nitro_empty).save(OUT_NITRO, quality=94, subsampling=0)
    paint_debug().save(OUT_DEBUG)
    print("wrote", OUT_EMPTY)
    print("wrote", OUT_PLAY)
    print("wrote", OUT_NITRO_EMPTY)
    print("wrote", OUT_NITRO)


if __name__ == "__main__":
    main()
