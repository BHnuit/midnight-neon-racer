#!/usr/bin/env python3
"""Measure the acceptance numbers in docs/art-bible-revision-01.md §9.

Reads the road constants from _paint_3lane.py so there is one source of truth
for the vanishing point. Prints one line per check and exits non-zero on FAIL.

    python3 _check_perspective.py [plate.jpg] [play.jpg]

Not covered here (needs a human to pick the lines): §4.1, picking 5 roadside
strokes and confirming they extrapolate through the vanishing point.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _paint_3lane import CAR_Y, DRIVE_HALF_AT_CAR, H, VX, VY, W, drive_edges  # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
PLATE = ROOT / "assets/minigame/previews/bg-night-empty.jpg"
PLAY = ROOT / "assets/minigame/previews/play-night-3lane.jpg"
SPRITE = ROOT / "assets/minigame/cars/paoche/paoche-rear.png"

ROAD_SLOPE = DRIVE_HALF_AT_CAR / (CAR_Y - VY)  # 半路宽 px/行
SHOULDER = 30  # §4.2 的 d
failures: list[str] = []


def check(name: str, ok: bool, detail: str) -> None:
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    if not ok:
        failures.append(name)


def magenta_score(a: np.ndarray) -> np.ndarray:
    raw = a[..., 0] + a[..., 2] - 2 * a[..., 1]
    return np.apply_along_axis(lambda r: np.convolve(r, np.ones(5) / 5, mode="same"), 1, raw)


def outer_pair(score_row: np.ndarray, thresh: float = 110.0) -> tuple[float, float] | None:
    """Centres of the outermost pair of magenta strokes in one row."""
    cols = np.where(score_row > thresh)[0]
    if len(cols) < 2:
        return None
    groups: list[list[int]] = []
    for x in cols:
        if groups and x - groups[-1][-1] <= 6:
            groups[-1].append(int(x))
        else:
            groups.append([int(x)])
    groups = [g for g in groups if len(g) >= 3]
    if len(groups) < 2:
        return None
    lo = (groups[0][0] + groups[0][-1]) / 2
    hi = (groups[-1][0] + groups[-1][-1]) / 2
    return (lo, hi) if hi - lo >= 120 else None


def fit_plate_ground(path: Path) -> tuple[float, float, float]:
    """Vanishing point and curb angle of whatever ground the plate itself has."""
    a = np.asarray(Image.open(path).convert("RGB")).astype(float)
    score = magenta_score(a)
    rows = []
    for y in range(850, 1000, 6):
        pair = outer_pair(score[y])
        if pair:
            rows.append((y, (pair[0] + pair[1]) / 2, (pair[1] - pair[0]) / 2))
    if len(rows) < 6:
        raise SystemExit("底板路缘识别失败，改不了阈值就手工量")
    mids = np.array([r[1] for r in rows])
    cand = [r for r in rows if abs(r[1] - np.median(mids)) <= 25]
    if len(cand) < 6:
        raise SystemExit("底板路缘识别失败，改不了阈值就手工量")
    # 护栏是断开的，少数行会给出垃圾配对。RANSAC 取共识，并要求半路宽随 y 增大。
    best: tuple[int, float, float] = (0, 0.0, 0.0)
    for i in range(len(cand)):
        for j in range(i + 1, len(cand)):
            dy = cand[j][0] - cand[i][0]
            if dy < 24:
                continue
            slope = (cand[j][2] - cand[i][2]) / dy
            if slope <= 0.1:
                continue
            intercept = cand[i][2] - slope * cand[i][0]
            inliers = sum(1 for r in cand if abs(slope * r[0] + intercept - r[2]) <= 6)
            if inliers > best[0]:
                best = (inliers, slope, intercept)
    if best[0] < 6:
        raise SystemExit("底板路缘拟合无共识，手工量")
    _, slope, intercept = best
    keep = [r for r in cand if abs(slope * r[0] + intercept - r[2]) <= 6]
    ys = np.array([r[0] for r in keep], float)
    slope, intercept = np.polyfit(ys, np.array([r[2] for r in keep], float), 1)
    print(f"  (底板拟合用 {len(keep)}/{len(rows)} 行，y {keep[0][0]}..{keep[-1][0]})")
    return float(np.median([r[1] for r in keep])), float(-intercept / slope), float(slope)


def match_car(a: np.ndarray) -> tuple[int, int, int, int, float]:
    """Sweep sprite size and position to measure how the car was actually placed.

    Returns the winning width, height, bottom row, centre column and error.
    Sweeping the size matters: pinning the template to the contract size would
    make the width check assert itself instead of measuring anything.
    """
    sp = Image.open(SPRITE).convert("RGBA")
    alpha = np.asarray(sp)[..., 3]
    ys, xs = np.where(alpha > 8)
    sp = sp.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    ratio = sp.height / sp.width
    road = np.array([19.0, 9.0, 39.0])

    def tile_for(w: int, h: int) -> np.ndarray:
        t = np.asarray(sp.resize((w, h), Image.NEAREST)).astype(float)
        al = t[..., 3:] / 255.0
        return t[..., :3] * al + road * (1 - al)

    def scan(w: int, h: int, cx: int, cy: int, span: int) -> tuple[int, int, float]:
        tile = tile_for(w, h)
        best = (cx, cy, 1e9)
        for oy in range(cy - span, cy + span + 1):
            for ox in range(cx - span, cx + span + 1):
                if oy < 0 or ox < 0 or oy + h > H or ox + w > W:
                    continue
                err = float(np.abs(a[oy : oy + h, ox : ox + w] - tile).mean())
                if err < best[2]:
                    best = (ox, oy, err)
        return best

    cw = round(W * 0.24)
    ch = round(cw * ratio)
    ox, oy, _ = scan(cw, ch, (W - cw) // 2, CAR_Y - ch, 30)
    best = (cw, ch, ox, oy, 1e9)
    for w in range(cw - 8, cw + 9, 4):
        for dh in range(-8, 9, 4):
            h = round(w * ratio) + dh
            bx, by, err = scan(w, h, ox + (cw - w) // 2, oy + (ch - h), 4)
            if err < best[4]:
                best = (w, h, bx, by, err)
    w, h, bx, by, err = best
    return w, h, by + h, bx + w // 2, err


def road_std(lum: np.ndarray, y0: int, y1: int) -> float:
    """Median 24x24 dither contrast, sampled only inside the drive surface."""
    out = []
    for y in range(y0, min(y1, H - 24), 24):
        dl, dr = drive_edges(y)
        lo, hi = int(max(dl + 8, 0)), int(min(dr - 8, W - 24))
        for x in range(lo, hi, 24):
            out.append(lum[y : y + 24, x : x + 24].std())
    return float(np.median(out)) if out else 0.0


def main() -> None:
    plate = Path(sys.argv[1]) if len(sys.argv) > 1 else PLATE
    play = Path(sys.argv[2]) if len(sys.argv) > 2 else PLAY
    a = np.asarray(Image.open(play).convert("RGB")).astype(float)
    lum = a.mean(axis=2)
    sat = a.max(axis=2) - a.min(axis=2)

    print(f"脚本地面: 消失点 ({VX}, {VY})  半宽斜率 {ROAD_SLOPE:.3f}  "
          f"路缘 {np.degrees(np.arctan2(1, ROAD_SLOPE)):.1f}°")

    print("\n§1 两套地面")
    px, py, pk = fit_plate_ground(plate)
    p_ang = np.degrees(np.arctan2(1, pk))
    s_ang = np.degrees(np.arctan2(1, ROAD_SLOPE))
    print(f"  底板地面: 消失点 ({px:.0f}, {py:.0f})  半宽斜率 {pk:.3f}  路缘 {p_ang:.1f}°")
    check("消失点对齐", abs(py - VY) <= 20 and abs(px - VX) <= 20,
          f"Δy={py - VY:+.0f}px Δx={px - VX:+.0f}px (限 ±20)")
    check("路缘夹角对齐", abs(p_ang - s_ang) <= 3.0,
          f"Δ={p_ang - s_ang:+.1f}° (限 ±3)")

    print("\n§4.2 城市底边")
    cyan = (a[..., 2] > a[..., 0] + 25) & (a[..., 1] > a[..., 0] + 10) & (lum > 60)
    devs = []
    for x0 in range(0, W, 60):
        col = [y for y in range(500, 1100) if cyan[y, x0 : x0 + 60].sum() >= 2]
        dl, _ = drive_edges(x0 + 30)
        if not col or abs(x0 + 30 - VX) < 60:
            continue
        want = VY + max(abs(x0 + 30 - VX) - SHOULDER, 0) / ROAD_SLOPE
        devs.append((x0, max(col), want - max(col)))
    for x0, got, dev in devs:
        print(f"  x {x0:3d}-{x0 + 60:3d}: 底边 y={got}  应在 y={got + dev:.0f}  差 {dev:+.0f}px")
    worst = max(abs(d) for _, _, d in devs) if devs else 0.0
    check("底边落位", worst <= 15, f"最大偏差 {worst:.0f}px (限 15)")
    # 镜像逐对比，取均值会把「一侧齐、一侧乱」抹平
    by_x = {x: d for x, _, d in devs}
    pairs = [(x, by_x[x], by_x[m]) for x in by_x
             if (m := W - 60 - x) in by_x and x + 30 < VX]
    if pairs:
        gap = max(abs(l - r) for _, l, r in pairs)
        for x, l, r in pairs:
            print(f"  镜像 x {x:3d} vs {W - 60 - x:3d}: {l:+.0f}px vs {r:+.0f}px")
        check("左右路肩同宽", gap <= 15, f"镜像最大差 {gap:.0f}px (限 15)")

    print("\n§2 车位")
    w, h, bottom, cx, err = match_car(a)
    sp = Image.open(SPRITE)
    alpha = np.asarray(sp.convert("RGBA"))[..., 3]
    sy, sx = np.where(alpha > 8)
    ratio = (sy.max() - sy.min() + 1) / (sx.max() - sx.min() + 1)
    print(f"  最佳匹配 {w}×{h} 车底 y={bottom} 中心 x={cx} 误差 {err:.1f}")
    check("车宽 24%", abs(w / W - 0.24) <= 0.012, f"{w}px = {w / W * 100:.1f}%")
    check("车底 80%", abs(bottom / H - 0.80) <= 0.012, f"y={bottom} = {bottom / H * 100:.1f}%")
    check("居中", abs(cx - W / 2) <= 6, f"中心 x={cx}（中线 {W // 2}）")
    check("等比缩放", abs(h - w * ratio) <= 5,
          f"高 {h}px，等比应 {w * ratio:.0f}px，差 {h - w * ratio:+.0f}px (限 ±5)")

    print("\n§5 车接地")
    cl, cr = (W - w) // 2, (W + w) // 2
    under = lum[bottom + 32, cl + 10 : cr - 10].mean()
    beside = lum[bottom + 32, max(cl - 110, 0) : cl - 30].mean()
    check("尾灯落光/接地", under - beside >= 12.0,
          f"车底+32px 正下方 {under:.1f} − 车外 {beside:.1f} = {under - beside:+.1f} (限 +12)")

    print("\n§7 点阵梯度")
    far, near = road_std(lum, VY + 20, 850), road_std(lum, 1000, H)
    ratio = near / far if far else 0.0
    check("近处对比更强", ratio >= 1.5, f"近 {near:.1f} ÷ 远 {far:.1f} = {ratio:.2f} (限 1.5)")

    print("\n§8 空天")
    content = ((sat > 40) & (lum > 50)).sum(axis=1)
    run = best = 0
    for y in range(H):
        run = run + 1 if content[y] < 30 else 0
        best = max(best, run)
    check("最大连续空天", best <= 320, f"{best}px = 画高 {best / H * 100:.1f}% (限 320px)")

    print(f"\n{len(failures)} 项未过" + (f": {', '.join(failures)}" if failures else ""))
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
