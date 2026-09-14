from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from event_horizon.fields import soft_horizon
from event_horizon.utils import save_rgb_image


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v002_horizon_masks.png"


def coordinate_grids(width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    x_values = np.linspace(-1.0, 1.0, width)
    y_values = np.linspace(1.0, -1.0, height)
    return np.meshgrid(x_values, y_values)


def radial_fields(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
) -> tuple[np.ndarray, np.ndarray]:
    r1 = np.sqrt((x + a) ** 2 + y**2)
    r2 = np.sqrt((x - a) ** 2 + y**2)
    return r1, r2


def ring_field(
    r1: np.ndarray,
    r2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
) -> np.ndarray:
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2)
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2)
    return a1 + a2


def shadow_field(
    r1: np.ndarray,
    r2: np.ndarray,
    horizon_radius: float = 0.14,
    horizon_edge: float = 0.015,
) -> np.ndarray:
    h1 = soft_horizon(r1, horizon_radius, horizon_edge)
    h2 = soft_horizon(r2, horizon_radius, horizon_edge)
    return np.maximum(h1, h2)


def v002_field(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    horizon_edge: float = 0.015,
) -> np.ndarray:
    r1, r2 = radial_fields(x, y, a=a)
    rings = ring_field(r1, r2, ring_radius=ring_radius, sharpness=sharpness)
    shadow = shadow_field(r1, r2, horizon_radius=horizon_radius, horizon_edge=horizon_edge)
    return rings * (1.0 - shadow)


def v002_rgb(
    width: int,
    height: int,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    horizon_edge: float = 0.015,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v002_field(
        x,
        y,
        a=a,
        ring_radius=ring_radius,
        sharpness=sharpness,
        horizon_radius=horizon_radius,
        horizon_edge=horizon_edge,
    )

    red = np.clip(1.10 * f, 0.0, 1.0)
    green = np.clip(0.58 * f, 0.0, 1.0)
    blue = np.clip(0.18 * f, 0.0, 1.0)

    return np.round(np.dstack([red, green, blue]) * 255.0).astype(np.uint8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render v002 - horizon masks.")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=1200)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    parser.add_argument("--horizon-radius", type=float, default=0.14)
    parser.add_argument("--horizon-edge", type=float, default=0.015)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rgb = v002_rgb(
        width=args.width,
        height=args.height,
        a=args.a,
        ring_radius=args.ring_radius,
        sharpness=args.sharpness,
        horizon_radius=args.horizon_radius,
        horizon_edge=args.horizon_edge,
    )
    output_path = save_rgb_image(args.output, rgb)
    print(f"saved {output_path}")


if __name__ == "__main__":
    main()
