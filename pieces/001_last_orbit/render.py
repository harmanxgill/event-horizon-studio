from __future__ import annotations

import argparse
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

import equations
from event_horizon.color import paint_mask, scalar_to_rgb
from event_horizon.utils import save_rgb_image


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "output" / "last_orbit_preview.png"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render 001 - The Last Orbit.")
    parser.add_argument("--width", type=int, default=1200, help="Rendered image width in pixels.")
    parser.add_argument("--height", type=int, default=1200, help="Rendered image height in pixels.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="PNG output path.")
    parser.add_argument("--extent", type=float, default=equations.DEFAULT_PARAMETERS["extent"])
    parser.add_argument("--separation", type=float, default=equations.DEFAULT_PARAMETERS["separation"])
    parser.add_argument("--orbit-phase", type=float, default=equations.DEFAULT_PARAMETERS["orbit_phase"])
    parser.add_argument("--horizon-radius", type=float, default=equations.DEFAULT_PARAMETERS["horizon_radius"])
    parser.add_argument("--horizon-edge", type=float, default=equations.DEFAULT_PARAMETERS["horizon_edge"])
    return parser.parse_args()


def render(args: argparse.Namespace) -> Path:
    fields = equations.evaluate_fields(
        width=args.width,
        height=args.height,
        extent=args.extent,
        separation=args.separation,
        orbit_phase=args.orbit_phase,
        horizon_radius=args.horizon_radius,
        horizon_edge=args.horizon_edge,
    )
    scalar = equations.preview_intensity(fields)
    rgb = scalar_to_rgb(scalar, cmap="magma")
    rgb = paint_mask(rgb, fields["horizon_mask"], color=(0, 0, 0))
    return save_rgb_image(args.output, rgb)


def main() -> None:
    output_path = render(parse_args())
    print(f"saved {output_path}")


if __name__ == "__main__":
    main()
