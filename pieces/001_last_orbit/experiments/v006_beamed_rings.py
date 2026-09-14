from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from event_horizon.fields import polar_angle, soft_horizon
from event_horizon.utils import save_rgb_image


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v006_beamed_rings.png"


def coordinate_grids(width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    x_values = np.linspace(-1.0, 1.0, width)
    y_values = np.linspace(1.0, -1.0, height)
    return np.meshgrid(x_values, y_values)


def grid_spacing(x: np.ndarray, y: np.ndarray) -> float:
    dx = abs(float(x[0, 1] - x[0, 0])) if x.shape[1] > 1 else 0.0
    dy = abs(float(y[1, 0] - y[0, 0])) if y.shape[0] > 1 else 0.0
    spacing = max(dx, dy)
    if spacing <= 0.0:
        raise ValueError("grid must sample more than one point along an axis")
    return spacing


def black_hole_centers(a: float = 0.36) -> tuple[tuple[float, float], tuple[float, float]]:
    return (-float(a), 0.0), (float(a), 0.0)


def radial_fields(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
) -> tuple[np.ndarray, np.ndarray]:
    r1 = np.sqrt((x + a) ** 2 + y**2)
    r2 = np.sqrt((x - a) ** 2 + y**2)
    return r1, r2


def wrap_angle(theta: np.ndarray) -> np.ndarray:
    return np.arctan2(np.sin(theta), np.cos(theta))


def angular_fields(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
) -> tuple[np.ndarray, np.ndarray]:
    center1, center2 = black_hole_centers(a=a)
    theta1 = polar_angle(x, y, center1)
    theta2 = wrap_angle(polar_angle(x, y, center2) - np.pi)
    return theta1, theta2


def angular_weight(theta: np.ndarray, anisotropy: float = 0.20) -> np.ndarray:
    if not -1.0 <= anisotropy <= 1.0:
        raise ValueError("anisotropy must lie in [-1, 1]")
    return 1.0 + float(anisotropy) * np.cos(theta)


ORBITAL_OFFSET = -0.5 * np.pi


def doppler_mean(beta: float, exponent: float, samples: int = 4096) -> float:
    turn = np.linspace(-np.pi, np.pi, samples, endpoint=False)
    return float(np.mean((1.0 / (1.0 - beta * np.cos(turn))) ** exponent))


def beaming_weight(
    theta: np.ndarray,
    beta: float = 0.28,
    exponent: float = 2.0,
    offset: float = ORBITAL_OFFSET,
) -> np.ndarray:
    if not 0.0 <= beta < 1.0:
        raise ValueError("beta must lie in [0, 1)")
    if exponent < 0.0:
        raise ValueError("exponent must be non-negative")

    doppler = 1.0 / (1.0 - float(beta) * np.cos(theta - float(offset)))
    return doppler ** float(exponent) / doppler_mean(float(beta), float(exponent))


def ring_field(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    anisotropy: float = 0.20,
    beta: float = 0.28,
    exponent: float = 2.0,
) -> np.ndarray:
    w1 = angular_weight(theta1, anisotropy) * beaming_weight(theta1, beta, exponent)
    w2 = angular_weight(theta2, anisotropy) * beaming_weight(theta2, beta, exponent)
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2) * w1
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2) * w2
    return a1 + a2


def glow_onset(ring_radius: float = 0.25, sharpness: float = 80.0) -> float:
    if sharpness <= 0.0:
        raise ValueError("sharpness must be positive")
    return float(ring_radius) + 1.0 / np.sqrt(float(sharpness))


def outer_glow(
    r: np.ndarray,
    onset: float,
    glow: float = 0.30,
    falloff: float = 3.5,
    gate_width: float = 0.03,
) -> np.ndarray:
    if glow < 0.0:
        raise ValueError("glow must be non-negative")
    if falloff <= 0.0:
        raise ValueError("falloff must be positive")

    outside = 1.0 - soft_horizon(r, onset, gate_width)
    return float(glow) * outside * np.exp(-float(falloff) * (r - float(onset)))


def halo_field(
    r1: np.ndarray,
    r2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    glow: float = 0.30,
    falloff: float = 3.5,
    gate_width: float = 0.03,
) -> np.ndarray:
    onset = glow_onset(ring_radius=ring_radius, sharpness=sharpness)
    g1 = outer_glow(r1, onset, glow=glow, falloff=falloff, gate_width=gate_width)
    g2 = outer_glow(r2, onset, glow=glow, falloff=falloff, gate_width=gate_width)
    return g1 + g2


def silhouette_field(
    r1: np.ndarray,
    r2: np.ndarray,
    horizon_edge: float,
    horizon_radius: float = 0.14,
) -> np.ndarray:
    h1 = soft_horizon(r1, horizon_radius, horizon_edge)
    h2 = soft_horizon(r2, horizon_radius, horizon_edge)
    return np.maximum(h1, h2)


def v006_field(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    edge_pixels: float = 1.0,
    glow: float = 0.30,
    falloff: float = 3.5,
    gate_width: float = 0.03,
    anisotropy: float = 0.20,
    beta: float = 0.28,
    exponent: float = 2.0,
) -> np.ndarray:
    if edge_pixels <= 0.0:
        raise ValueError("edge_pixels must be positive")

    r1, r2 = radial_fields(x, y, a=a)
    theta1, theta2 = angular_fields(x, y, a=a)
    rings = ring_field(
        r1,
        r2,
        theta1,
        theta2,
        ring_radius=ring_radius,
        sharpness=sharpness,
        anisotropy=anisotropy,
        beta=beta,
        exponent=exponent,
    )
    halo = halo_field(
        r1,
        r2,
        ring_radius=ring_radius,
        sharpness=sharpness,
        glow=glow,
        falloff=falloff,
        gate_width=gate_width,
    )

    horizon_edge = float(edge_pixels) * grid_spacing(x, y)
    silhouette = silhouette_field(r1, r2, horizon_edge, horizon_radius=horizon_radius)
    return (rings + halo) * (1.0 - silhouette)


def v006_rgb(
    width: int,
    height: int,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    edge_pixels: float = 1.0,
    glow: float = 0.30,
    falloff: float = 3.5,
    gate_width: float = 0.03,
    anisotropy: float = 0.20,
    beta: float = 0.28,
    exponent: float = 2.0,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v006_field(
        x,
        y,
        a=a,
        ring_radius=ring_radius,
        sharpness=sharpness,
        horizon_radius=horizon_radius,
        edge_pixels=edge_pixels,
        glow=glow,
        falloff=falloff,
        gate_width=gate_width,
        anisotropy=anisotropy,
        beta=beta,
        exponent=exponent,
    )

    red = np.clip(1.10 * f, 0.0, 1.0)
    green = np.clip(0.58 * f, 0.0, 1.0)
    blue = np.clip(0.18 * f, 0.0, 1.0)

    return np.round(np.dstack([red, green, blue]) * 255.0).astype(np.uint8)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render v006 - beamed rings.")
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=1200)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    parser.add_argument("--horizon-radius", type=float, default=0.14)
    parser.add_argument("--edge-pixels", type=float, default=1.0)
    parser.add_argument("--glow", type=float, default=0.30)
    parser.add_argument("--falloff", type=float, default=3.5)
    parser.add_argument("--gate-width", type=float, default=0.03)
    parser.add_argument("--anisotropy", type=float, default=0.20)
    parser.add_argument("--beta", type=float, default=0.28)
    parser.add_argument("--exponent", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rgb = v006_rgb(
        width=args.width,
        height=args.height,
        a=args.a,
        ring_radius=args.ring_radius,
        sharpness=args.sharpness,
        horizon_radius=args.horizon_radius,
        edge_pixels=args.edge_pixels,
        glow=args.glow,
        falloff=args.falloff,
        gate_width=args.gate_width,
        anisotropy=args.anisotropy,
        beta=args.beta,
        exponent=args.exponent,
    )
    output_path = save_rgb_image(args.output, rgb)
    print(f"saved {output_path}")


if __name__ == "__main__":
    main()
