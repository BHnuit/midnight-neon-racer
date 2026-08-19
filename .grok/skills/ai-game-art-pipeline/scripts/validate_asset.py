#!/usr/bin/env python3
"""Validate deterministic properties of a game-art PNG.

This script checks file facts only. It cannot judge composition, style, semantics,
or whether a background was correctly removed.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:  # pragma: no cover - environment error
    raise SystemExit("Pillow is required: python3 -m pip install Pillow") from exc


def parse_size(value: str) -> tuple[int, int]:
    try:
        width, height = (int(part) for part in value.lower().split("x", 1))
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected WIDTHxHEIGHT, for example 64x96") from exc
    if width < 1 or height < 1:
        raise argparse.ArgumentTypeError("size must be positive")
    return width, height


def parse_palette(value: str) -> set[tuple[int, int, int]]:
    colors: set[tuple[int, int, int]] = set()
    for raw in value.split(","):
        item = raw.strip().lstrip("#")
        if len(item) != 6:
            raise argparse.ArgumentTypeError("palette colors must be six-digit hex values")
        try:
            colors.add(tuple(int(item[index : index + 2], 16) for index in (0, 2, 4)))
        except ValueError as exc:
            raise argparse.ArgumentTypeError(f"invalid palette color: {raw}") from exc
    return colors


def validate(args: argparse.Namespace) -> tuple[list[str], list[str], dict[str, object]]:
    errors: list[str] = []
    warnings: list[str] = []
    path = Path(args.image)
    if not path.is_file():
        return [f"file not found: {path}"], warnings, {}

    try:
        image = Image.open(path)
        image.load()
    except Exception as exc:
        return [f"cannot read image: {exc}"], warnings, {}

    width, height = image.size
    if args.size and (width, height) != args.size:
        errors.append(f"size is {width}x{height}, expected {args.size[0]}x{args.size[1]}")

    if args.grid and (width % args.grid or height % args.grid):
        errors.append(f"size {width}x{height} is not divisible by grid {args.grid}")

    if image.format != "PNG":
        errors.append(f"format is {image.format or 'unknown'}, expected PNG")

    has_alpha = "A" in image.getbands() or "transparency" in image.info
    if args.require_alpha and not has_alpha:
        errors.append("image has no alpha channel or transparency table")

    rgba = image.convert("RGBA")
    pixel_reader = getattr(rgba, "get_flattened_data", None)
    pixels = list(pixel_reader() if pixel_reader else rgba.getdata())
    alpha_values = {pixel[3] for pixel in pixels}
    partial_alpha_pixels = sum(0 < pixel[3] < 255 for pixel in pixels)
    if partial_alpha_pixels and not args.allow_partial_alpha:
        errors.append("partial alpha found; pass --allow-partial-alpha only for approved FX")

    visible_colors = {pixel[:3] for pixel in pixels if pixel[3] > 0}
    if args.palette:
        outside = sorted(visible_colors - args.palette)
        if outside:
            errors.append(f"{len(outside)} visible RGB colors are outside the declared palette")

    if args.max_colors is not None and len(visible_colors) > args.max_colors:
        errors.append(f"visible color count is {len(visible_colors)}, max is {args.max_colors}")

    transparent_rgb = {pixel[:3] for pixel in pixels if pixel[3] == 0}
    if transparent_rgb and len(transparent_rgb) > 1:
        warnings.append("transparent pixels contain multiple RGB matte colors; inspect for fringe risk")

    details = {
        "file": str(path),
        "format": image.format,
        "mode": image.mode,
        "size": {"width": width, "height": height},
        "visible_color_count": len(visible_colors),
        "has_alpha": has_alpha,
        "alpha_values": sorted(alpha_values),
        "partial_alpha_pixel_count": partial_alpha_pixels,
    }
    return errors, warnings, details


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("image", help="PNG to validate")
    parser.add_argument("--size", type=parse_size, help="required pixel size, for example 64x96")
    parser.add_argument("--grid", type=int, default=0, help="require width and height to divide evenly by this grid")
    parser.add_argument("--palette", type=parse_palette, help="comma-separated allowed RGB hex colors")
    parser.add_argument("--max-colors", type=int, help="maximum number of visible RGB colors")
    parser.add_argument("--require-alpha", action="store_true", help="require an alpha channel or transparency table")
    parser.add_argument("--allow-partial-alpha", action="store_true", help="allow partial alpha for an approved FX layer")
    parser.add_argument("--json", action="store_true", help="emit machine-readable output")
    args = parser.parse_args()
    errors, warnings, details = validate(args)

    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings, "details": details}, indent=2))
    else:
        for warning in warnings:
            print(f"[WARN] {warning}")
        for error in errors:
            print(f"[ERROR] {error}")
        if not errors:
            print(f"[OK] {args.image}: {details['size']['width']}x{details['size']['height']} PNG")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
