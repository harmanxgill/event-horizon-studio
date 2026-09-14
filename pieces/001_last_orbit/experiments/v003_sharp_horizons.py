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
from event_horizon.cli import experiment_parser, save_and_report
from event_horizon.color import warm_rgb
from event_horizon.geometry import coordinate_grids, grid_spacing, radial_fields


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v003_sharp_horizons.png"


def ring_field(
    r1: np.ndarray,
    r2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
) -> np.ndarray:
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2)
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2)
    return a1 + a2


def silhouette_field(
    r1: np.ndarray,
    r2: np.ndarray,
    horizon_edge: float,
    horizon_radius: float = 0.14,
) -> np.ndarray:
    h1 = soft_horizon(r1, horizon_radius, horizon_edge)
    h2 = soft_horizon(r2, horizon_radius, horizon_edge)
    return np.maximum(h1, h2)


def v003_field(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    edge_pixels: float = 1.0,
) -> np.ndarray:
    if edge_pixels <= 0.0:
        raise ValueError("edge_pixels must be positive")

    r1, r2 = radial_fields(x, y, a=a)
    rings = ring_field(r1, r2, ring_radius=ring_radius, sharpness=sharpness)
    horizon_edge = float(edge_pixels) * grid_spacing(x, y)
    silhouette = silhouette_field(r1, r2, horizon_edge, horizon_radius=horizon_radius)
    return rings * (1.0 - silhouette)


def v003_rgb(
    width: int,
    height: int,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    edge_pixels: float = 1.0,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v003_field(
        x,
        y,
        a=a,
        ring_radius=ring_radius,
        sharpness=sharpness,
        horizon_radius=horizon_radius,
        edge_pixels=edge_pixels,
    )

    return warm_rgb(f)


def parse_args() -> argparse.Namespace:
    parser = experiment_parser("Render v003 - sharp horizons.", DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    parser.add_argument("--horizon-radius", type=float, default=0.14)
    parser.add_argument("--edge-pixels", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rgb = v003_rgb(
        width=args.width,
        height=args.height,
        a=args.a,
        ring_radius=args.ring_radius,
        sharpness=args.sharpness,
        horizon_radius=args.horizon_radius,
        edge_pixels=args.edge_pixels,
    )
    save_and_report(args.output, rgb)


if __name__ == "__main__":
    main()
