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
from event_horizon.cli import experiment_parser, save_and_report
from event_horizon.color import warm_rgb
from event_horizon.geometry import angular_fields, black_hole_centers, coordinate_grids, grid_spacing, radial_fields, wrap_angle


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v007_structured_light.png"


def angular_weight(theta: np.ndarray, anisotropy: float = 0.20) -> np.ndarray:
    if not -1.0 <= anisotropy <= 1.0:
        raise ValueError("anisotropy must lie in [-1, 1]")
    return 1.0 + float(anisotropy) * np.cos(theta)


def harmonic_weight(
    theta: np.ndarray,
    order: int = 4,
    harmonic: float = 0.30,
) -> np.ndarray:
    if int(order) < 1:
        raise ValueError("order must be a positive integer")
    if not -1.0 <= harmonic <= 1.0:
        raise ValueError("harmonic must lie in [-1, 1]")
    return 1.0 + float(harmonic) * np.cos(int(order) * theta)


ORBITAL_OFFSET = -0.5 * np.pi


def doppler_factor(
    theta: np.ndarray,
    beta: float = 0.28,
    exponent: float = 2.0,
    offset: float = ORBITAL_OFFSET,
) -> np.ndarray:
    if not 0.0 <= beta < 1.0:
        raise ValueError("beta must lie in [0, 1)")
    if exponent < 0.0:
        raise ValueError("exponent must be non-negative")

    return (1.0 / (1.0 - float(beta) * np.cos(theta - float(offset)))) ** float(exponent)


def ring_weight(
    theta: np.ndarray,
    anisotropy: float = 0.20,
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
    offset: float = ORBITAL_OFFSET,
    samples: int = 4096,
) -> np.ndarray:
    def profile(angle: np.ndarray) -> np.ndarray:
        return (
            angular_weight(angle, anisotropy)
            * harmonic_weight(angle, order, harmonic)
            * doppler_factor(angle, beta, exponent, offset)
        )

    turn = np.linspace(-np.pi, np.pi, int(samples), endpoint=False)
    return profile(theta) / float(np.mean(profile(turn)))


def ring_field(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    anisotropy: float = 0.20,
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
) -> np.ndarray:
    w1 = ring_weight(theta1, anisotropy, order, harmonic, beta, exponent)
    w2 = ring_weight(theta2, anisotropy, order, harmonic, beta, exponent)
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


def v007_field(
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
    order: int = 4,
    harmonic: float = 0.30,
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
        order=order,
        harmonic=harmonic,
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


def v007_rgb(
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
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v007_field(
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
        order=order,
        harmonic=harmonic,
        beta=beta,
        exponent=exponent,
    )

    return warm_rgb(f)


def parse_args() -> argparse.Namespace:
    parser = experiment_parser("Render v007 - structured light.", DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    parser.add_argument("--horizon-radius", type=float, default=0.14)
    parser.add_argument("--edge-pixels", type=float, default=1.0)
    parser.add_argument("--glow", type=float, default=0.30)
    parser.add_argument("--falloff", type=float, default=3.5)
    parser.add_argument("--gate-width", type=float, default=0.03)
    parser.add_argument("--anisotropy", type=float, default=0.20)
    parser.add_argument("--order", type=int, default=4)
    parser.add_argument("--harmonic", type=float, default=0.30)
    parser.add_argument("--beta", type=float, default=0.28)
    parser.add_argument("--exponent", type=float, default=2.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    rgb = v007_rgb(
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
        order=args.order,
        harmonic=args.harmonic,
        beta=args.beta,
        exponent=args.exponent,
    )
    save_and_report(args.output, rgb)


if __name__ == "__main__":
    main()
