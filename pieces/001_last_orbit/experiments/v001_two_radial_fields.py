from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from event_horizon.cli import experiment_parser, save_and_report
from event_horizon.color import warm_rgb
from event_horizon.geometry import coordinate_grids, radial_fields


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v001_two_radial_fields.png"


def v001_field(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
) -> np.ndarray:
    r1, r2 = radial_fields(x, y, a=a)
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2)
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2)
    return a1 + a2


def v001_rgb(
    width: int,
    height: int,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v001_field(x, y, a=a, ring_radius=ring_radius, sharpness=sharpness)

    return warm_rgb(f)


def parse_args() -> argparse.Namespace:
    parser = experiment_parser("Render v001 - two radial fields.", DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rgb = v001_rgb(
        width=args.width,
        height=args.height,
        a=args.a,
        ring_radius=args.ring_radius,
        sharpness=args.sharpness,
    )
    save_and_report(args.output, rgb)


if __name__ == "__main__":
    main()
