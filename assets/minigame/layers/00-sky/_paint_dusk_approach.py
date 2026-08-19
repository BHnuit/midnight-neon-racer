#!/usr/bin/env python3
"""傍晚进城天空：直接抽 ref-5 扫描暮色 + ref-3 暖边，不再手切色卡条。"""
from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
REF5 = ROOT / "assets/minigame/refs/ref-5.png"
REF3 = ROOT / "assets/minigame/refs/ref-3.png"
PLAY = ROOT / "assets/minigame/previews/play-night-3lane.jpg"
OUT_DUSK = HERE / "dusk.png"
OUT_SUN = HERE / "prop-sun-dusk.png"
OUT_PLAY = ROOT / "assets/minigame/previews/play-dusk-approach.jpg"

W, H = 720, 1280
# Historical A preview baseline. Runtime and new production assets use A-2 (VY=700).
VY = 797
# 城楼大约从 y=560 冒头；天空铺到这里即可
SKY_END = 720

# 扁落日坐在橙带里，避开路尖
SUN = dict(cx=210, cy=430, rx=78, ry=28)


def sample_rows(img: np.ndarray, y0: int, y1: int, x0: int, x1: int) -> np.ndarray:
    return np.median(img[y0:y1, x0:x1], axis=1).astype(np.float32)


def build_sky() -> np.ndarray:
    r5 = np.asarray(Image.open(REF5).convert("RGB"))
    r3 = np.asarray(Image.open(REF3).convert("RGB"))
    # ref-5：山线大约 y=192，上面全是 1px 扫描暮色
    c5 = sample_rows(r5, 0, 186, 60, 440)
    c3 = sample_rows(r3, 0, 250, 280, 920)

    sky = np.zeros((H, W, 4), np.uint8)
    n5, n3 = len(c5), len(c3)
    for y in range(SKY_END):
        t = y / max(SKY_END - 1, 1)
        # 上段多留夜紫，下段跟 ref-5 走到橙，再掺一点 ref-3 的进城暖
        if t < 0.22:
            u = t / 0.22 * 0.22
            src = c5[int(u * (n5 - 1))]
        else:
            u = (t - 0.22) / 0.78
            i5 = int(np.clip(u, 0, 1) * (n5 - 1))
            i3 = int(np.clip((u * 0.55 + 0.45), 0, 1) * (n3 - 1))
            src = c5[i5] * 0.72 + c3[i3] * 0.28
        # 保留 ref-5 的奇偶扫线：亮一行、暗一行
        scan = 1.06 if (y % 2 == 0) else 0.90
        row = np.clip(src * scan, 0, 255)
        # 横向轻微 1px 噪，来自参考行里真实起伏
        jitter = r5[min(n5 - 1, int(t * (n5 - 1))), 60:60 + W]
        if jitter.shape[0] < W:
            jitter = np.resize(jitter, (W, 3))
        mix = row[None, :] * 0.88 + jitter.astype(np.float32) * 0.12
        sky[y, :, :3] = np.clip(mix, 0, 255).astype(np.uint8)
        sky[y, :, 3] = 255
    return sky


def paint_sun(sky: np.ndarray) -> np.ndarray:
    """落日用周围橙带的色，晕是同带品红点阵，不另画一圈甜甜圈。"""
    cx, cy, rx, ry = SUN["cx"], SUN["cy"], SUN["rx"], SUN["ry"]
    local = sky[cy, cx, :3].astype(np.float32)
    amber = np.array([250, 191, 55], np.float32)
    magenta = np.array([233, 12, 190], np.float32)
    core = amber * 0.72 + local * 0.28
    y0, y1 = max(0, cy - ry - 18), min(H, cy + ry + 18)
    x0, x1 = max(0, cx - rx - 18), min(W, cx + rx + 18)
    yy, xx = np.mgrid[y0:y1, x0:x1]
    e = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    sl = sky[y0:y1, x0:x1]
    bayer = ((xx & 1) ^ (yy & 1)).astype(bool)
    halo = (e > 0.85) & (e <= 1.35) & bayer
    mid = (e > 0.42) & (e <= 0.85)
    body = e <= 0.42
    sl[halo, :3] = (magenta * 0.45 + sl[halo, :3].astype(np.float32) * 0.55).astype(np.uint8)
    sl[mid, :3] = np.where(
        bayer[mid, None],
        (core * 0.7 + magenta * 0.3).astype(np.uint8),
        core.astype(np.uint8),
    )
    sl[body, :3] = core.astype(np.uint8)
    sl[halo | mid | body, 3] = 255
    sky[y0:y1, x0:x1] = sl
    return sky


def crop_sun(sky: np.ndarray) -> Image.Image:
    cx, cy, rx, ry = SUN["cx"], SUN["cy"], SUN["rx"], SUN["ry"]
    pad = 22
    x0, y0 = cx - rx - pad, cy - ry - pad
    x1, y1 = cx + rx + pad, cy + ry + pad
    tile = sky[y0:y1, x0:x1].copy()
    yy, xx = np.mgrid[0 : tile.shape[0], 0 : tile.shape[1]]
    e = ((xx - (cx - x0)) / rx) ** 2 + ((yy - (cy - y0)) / ry) ** 2
    tile[e > 1.35, 3] = 0
    return Image.fromarray(tile, "RGBA")


def is_empty_navy(rgb: np.ndarray) -> np.ndarray:
    """只换原底板那块匀净夜空，不动楼墙。"""
    r = rgb[..., 0].astype(np.int16)
    g = rgb[..., 1].astype(np.int16)
    b = rgb[..., 2].astype(np.int16)
    return (r <= 20) & (g <= 28) & (b >= 40) & (b <= 78) & (np.abs(r - g) <= 16)


def composite(play: Image.Image, sky: np.ndarray) -> Image.Image:
    base = np.array(play.convert("RGB"))
    out = base.copy()
    navy = is_empty_navy(base)
    for y in range(min(VY, SKY_END + 40)):
        src = sky[y]
        if src[:, 3].max() == 0:
            continue
        mask = navy[y] & (src[:, 3] > 0)
        if mask.any():
            out[y, mask] = src[mask, :3]
    return Image.fromarray(out, "RGB")


def empty_run(img: Image.Image) -> int:
    a = np.asarray(img.convert("RGB")).astype(np.int16)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)
    content = ((sat > 40) & (lum > 50)).sum(axis=1)
    run = best = 0
    for y in range(H):
        run = run + 1 if content[y] < 30 else 0
        best = max(best, run)
    return best


def main() -> None:
    sky = paint_sun(build_sky())
    Image.fromarray(sky, "RGBA").save(OUT_DUSK)
    crop_sun(sky).save(OUT_SUN)
    play = composite(Image.open(PLAY), sky)
    play.save(OUT_PLAY, quality=94, subsampling=0)
    print("wrote", OUT_DUSK)
    print("wrote", OUT_SUN)
    print("wrote", OUT_PLAY)
    print(f"empty-sky run {empty_run(play)}px")


if __name__ == "__main__":
    main()
