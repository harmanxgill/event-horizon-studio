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
from event_horizon.fields import polar_angle, soft_horizon
from event_horizon.geometry import (
    angular_fields,
    black_hole_centers,
    coordinate_grids,
    radial_fields,
    wrap_angle,
)


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v026_final_equation.png"

ORBITAL_OFFSET = -0.5 * np.pi


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


def natural_pitch(
    order: int = 4,
    sharpness: float = 80.0,
    ring_radius: float = 0.25,
) -> float:
    if int(order) < 1:
        raise ValueError("order must be a positive integer")
    if sharpness <= 0.0:
        raise ValueError("sharpness must be positive")
    if ring_radius <= 0.0:
        raise ValueError("ring_radius must be positive")
    return float(np.arctan(int(order) / (np.pi * np.sqrt(sharpness) * float(ring_radius))))


def spiral_phase(
    theta: np.ndarray,
    r: np.ndarray,
    ring_radius: float = 0.25,
    pitch: float | None = None,
    softening: float = 0.02,
) -> np.ndarray:
    if pitch is None:
        pitch = natural_pitch(ring_radius=ring_radius)
    if not 0.0 < pitch <= 0.5 * np.pi:
        raise ValueError("pitch must lie in (0, pi/2]")
    if softening < 0.0:
        raise ValueError("softening must be non-negative")

    softened = np.sqrt(r**2 + float(softening) ** 2)
    winding = 1.0 / np.tan(float(pitch))
    return theta - winding * np.log(softened / float(ring_radius))


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
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
    offset: float = ORBITAL_OFFSET,
    samples: int = 4096,
) -> np.ndarray:
    def profile(angle: np.ndarray) -> np.ndarray:
        return harmonic_weight(angle, order, harmonic) * doppler_factor(angle, beta, exponent, offset)

    turn = np.linspace(-np.pi, np.pi, int(samples), endpoint=False)
    return profile(theta) / float(np.mean(profile(turn)))


def radial_decay(r: np.ndarray, decay: float = 2.0) -> np.ndarray:
    if decay < 0.0:
        raise ValueError("decay must be non-negative")
    return np.exp(-float(decay) * r)


def ring_components(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
    pitch: float | None = None,
    decay: float = 2.0,
) -> tuple[np.ndarray, np.ndarray]:
    if pitch is None:
        pitch = natural_pitch(order, sharpness, ring_radius)

    phi1 = spiral_phase(theta1, r1, ring_radius, pitch)
    phi2 = spiral_phase(theta2, r2, ring_radius, pitch)
    w1 = ring_weight(phi1, order, harmonic, beta, exponent)
    w2 = ring_weight(phi2, order, harmonic, beta, exponent)
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2) * w1 * radial_decay(r1, decay)
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2) * w2 * radial_decay(r2, decay)
    return a1, a2


def fine_structure(
    r: np.ndarray,
    theta: np.ndarray,
    epsilon_n: float = 0.35,
    k_r: float = 90.0,
    m_n: int = 24,
    c_n: float = 6.0,
    soft_n: float = 0.02,
) -> np.ndarray:
    if not 0.0 <= epsilon_n <= 1.0:
        raise ValueError("epsilon_n must lie in [0, 1]")
    if float(m_n) != int(m_n):
        # m_n multiplies an angle that jumps at +-pi; only whole numbers keep it continuous
        raise ValueError("m_n must be an integer")
    if soft_n <= 0.0:
        raise ValueError("soft_n must be positive")

    phase = float(k_r) * r + int(m_n) * theta
    return 1.0 + float(epsilon_n) * np.sin(phase + float(c_n) * np.log(r + float(soft_n)))


def doppler_factor_inspired(
    velocity: np.ndarray,
    beta_d: float = 0.30,
    p_d: float = 3.0,
) -> np.ndarray:
    if not 0.0 <= beta_d < 1.0:
        raise ValueError("beta_d must lie in [0, 1)")
    if p_d < 0.0:
        raise ValueError("p_d must be non-negative")
    return (1.0 + float(beta_d) * velocity) ** float(p_d)


def phased_angles(
    theta1: np.ndarray,
    theta2: np.ndarray,
    phase: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    return wrap_angle(theta1 - float(phase)), wrap_angle(theta2 - float(phase))


def companion_distortion(theta: np.ndarray, distortion: float = -0.30) -> np.ndarray:
    if not -1.0 < distortion < 1.0:
        raise ValueError("distortion must lie in (-1, 1)")
    return 1.0 + float(distortion) * np.cos(theta)


def distorted_radii(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
    distortion: float = -0.30,
) -> tuple[np.ndarray, np.ndarray]:
    return (
        r1 * companion_distortion(theta1, distortion),
        r2 * companion_distortion(theta2, distortion),
    )


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


def interaction_field(
    r1: np.ndarray,
    r2: np.ndarray,
    a: float = 0.36,
    alpha_i: float = 1.5,
    beta_i: float = 3.0,
    strength: float = 1.00,
) -> np.ndarray:
    if alpha_i < 0.0:
        raise ValueError("alpha_i must be non-negative")
    if beta_i < 0.0:
        raise ValueError("beta_i must be non-negative")
    if strength < 0.0:
        raise ValueError("strength must be non-negative")

    balance = np.exp(-float(alpha_i) * (r1 - r2) ** 2)
    confinement = np.exp(-float(beta_i) * (r1 + r2 - 2.0 * float(a)))
    return float(strength) * balance * confinement


def tidal_bridge(
    x: np.ndarray,
    y: np.ndarray,
    r1: np.ndarray,
    r2: np.ndarray,
    a: float = 0.36,
    alpha_i: float = 1.5,
    beta_i: float = 3.0,
    strength: float = 1.00,
    alpha_t: float = 120.0,
    beta_t: float = 25.0,
    eta_t: float = 0.50,
    k_t: float = 32.0,
    bridge_phase: float = 0.0,
) -> np.ndarray:
    if alpha_t < 0.0 or beta_t < 0.0:
        raise ValueError("alpha_t and beta_t must be non-negative")
    if not -1.0 <= eta_t <= 1.0:
        raise ValueError("eta_t must lie in [-1, 1]")

    interaction = interaction_field(
        r1, r2, a=a, alpha_i=alpha_i, beta_i=beta_i, strength=strength
    )
    envelope = np.exp(-float(alpha_t) * y**2) * np.exp(-float(beta_t) * x**4)
    structure = 1.0 + float(eta_t) * np.cos(float(k_t) * x + float(bridge_phase))
    return interaction * envelope * structure


def plain_angles(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
) -> tuple[np.ndarray, np.ndarray]:
    center1, center2 = black_hole_centers(a=a)
    return polar_angle(x, y, center1), polar_angle(x, y, center2)


def tail_taper(theta: np.ndarray, taper: float = 0.5) -> np.ndarray:
    if taper < 0.0:
        raise ValueError("taper must be non-negative")
    if taper == 0.0:
        return np.ones_like(theta)
    return 1.0 - np.exp(-(((np.pi - np.abs(theta)) / float(taper)) ** 2))


def tidal_tails(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
    alpha_q: float = 150.0,
    radius_q: float = 0.45,
    c_q: float = 0.25,
    beta_q: float = 1.5,
    tails: float = 0.60,
    taper: float = 0.5,
) -> np.ndarray:
    if alpha_q < 0.0 or beta_q < 0.0:
        raise ValueError("alpha_q and beta_q must be non-negative")
    if tails < 0.0:
        raise ValueError("tails must be non-negative")

    q1 = np.exp(-float(alpha_q) * (r1 - float(radius_q) - float(c_q) * theta1) ** 2)
    q2 = np.exp(-float(alpha_q) * (r2 - float(radius_q) + float(c_q) * theta2) ** 2)

    q1 = q1 * tail_taper(theta1, taper)
    q2 = q2 * tail_taper(theta2, taper)

    return float(tails) * (
        q1 * np.exp(-float(beta_q) * r1) + q2 * np.exp(-float(beta_q) * r2)
    )


def binary_potential(
    r1: np.ndarray,
    r2: np.ndarray,
    m1: float = 1.0,
    m2: float = 1.0,
    epsilon: float = 0.05,
) -> np.ndarray:
    if epsilon <= 0.0:
        raise ValueError("epsilon must be positive")
    return -(float(m1) / (r1 + float(epsilon)) + float(m2) / (r2 + float(epsilon)))


def potential_weight(
    r1: np.ndarray,
    r2: np.ndarray,
    kappa: float = 0.15,
    m1: float = 1.0,
    m2: float = 1.0,
    epsilon: float = 0.05,
) -> np.ndarray:
    if kappa < 0.0:
        raise ValueError("kappa must be non-negative")
    potential = binary_potential(r1, r2, m1=m1, m2=m2, epsilon=epsilon)
    return 1.0 - np.exp(-float(kappa) * np.abs(potential))


def horizon_suppression(
    r1: np.ndarray,
    r2: np.ndarray,
    k_h: float = 600.0,
    horizon_radius: float = 0.14,
) -> np.ndarray:
    if k_h <= 0.0:
        raise ValueError("k_h must be positive")
    if horizon_radius <= 0.0:
        raise ValueError("horizon_radius must be positive")

    # clipped like soft_horizon so a very sharp k_h cannot overflow the exponential
    z1 = np.clip(-float(k_h) * (r1 - float(horizon_radius)), -60.0, 60.0)
    z2 = np.clip(-float(k_h) * (r2 - float(horizon_radius)), -60.0, 60.0)
    return (1.0 / (1.0 + np.exp(z1))) * (1.0 / (1.0 + np.exp(z2)))


def colour_equations(
    level: np.ndarray,
    rate_r: float = 4.0,
    rate_g: float = 2.0,
    rate_b: float = 0.7,
) -> np.ndarray:
    if min(rate_r, rate_g, rate_b) <= 0.0:
        raise ValueError("channel rates must be positive")

    red = 1.0 - np.exp(-float(rate_r) * level)
    green = 1.0 - np.exp(-float(rate_g) * level)
    blue = 1.0 - np.exp(-float(rate_b) * level)
    return np.clip(np.dstack([red, green, blue]), 0.0, 1.0)


def to_pixels(colour: np.ndarray) -> np.ndarray:
    return np.round(np.clip(colour, 0.0, 1.0) * 255.0).astype(np.uint8)


def v026_field(
    x: np.ndarray,
    y: np.ndarray,
    a: float = 0.36,
    ring_radius: float = 0.25,
    sharpness: float = 80.0,
    horizon_radius: float = 0.14,
    k_h: float = 600.0,
    glow: float = 0.30,
    falloff: float = 3.5,
    gate_width: float = 0.03,
    order: int = 4,
    harmonic: float = 0.30,
    beta: float = 0.28,
    exponent: float = 2.0,
    pitch: float | None = None,
    decay: float = 2.0,
    phase: float = 0.0,
    distortion: float = -0.30,
    alpha_i: float = 1.5,
    beta_i: float = 3.0,
    strength: float = 1.00,
    alpha_t: float = 120.0,
    beta_t: float = 25.0,
    eta_t: float = 0.50,
    k_t: float = 32.0,
    bridge_phase: float = 0.0,
    alpha_q: float = 150.0,
    radius_q: float = 0.45,
    c_q: float = 0.25,
    beta_q: float = 1.5,
    tails: float = 0.60,
    taper: float = 0.5,
    kappa_phi: float = 0.15,
    epsilon_phi: float = 0.05,
    lambda_p: float = 0.25,
    beta_d: float = 0.30,
    p_d: float = 3.0,
    epsilon_n: float = 0.35,
    k_r: float = 90.0,
    m_n: int = 24,
    c_n: float = 6.0,
    soft_n: float = 0.02,
    gamma_l: float = 0.25,
) -> np.ndarray:
    if gamma_l <= 0.0:
        raise ValueError("gamma_l must be positive")

    r1, r2 = radial_fields(x, y, a=a)
    theta1, theta2 = angular_fields(x, y, a=a)
    d1, d2 = distorted_radii(r1, r2, theta1, theta2, distortion)
    theta1, theta2 = phased_angles(theta1, theta2, phase)

    s1, s2 = ring_components(
        d1,
        d2,
        theta1,
        theta2,
        ring_radius=ring_radius,
        sharpness=sharpness,
        order=order,
        harmonic=harmonic,
        beta=beta,
        exponent=exponent,
        pitch=pitch,
        decay=decay,
    )
    n1 = fine_structure(d1, theta1, epsilon_n=epsilon_n, k_r=k_r, m_n=m_n, c_n=c_n, soft_n=soft_n)
    n2 = fine_structure(d2, theta2, epsilon_n=epsilon_n, k_r=k_r, m_n=m_n, c_n=c_n, soft_n=soft_n)
    doppler1 = doppler_factor_inspired(np.cos(theta1), beta_d=beta_d, p_d=p_d)
    doppler2 = doppler_factor_inspired(np.cos(theta2), beta_d=beta_d, p_d=p_d)
    rings = doppler1 * s1 * n1 + doppler2 * s2 * n2

    halo = halo_field(
        r1,
        r2,
        ring_radius=ring_radius,
        sharpness=sharpness,
        glow=glow,
        falloff=falloff,
        gate_width=gate_width,
    )
    bridge = tidal_bridge(
        x,
        y,
        r1,
        r2,
        a=a,
        alpha_i=alpha_i,
        beta_i=beta_i,
        strength=strength,
        alpha_t=alpha_t,
        beta_t=beta_t,
        eta_t=eta_t,
        k_t=k_t,
        bridge_phase=bridge_phase,
    )
    sweep1, sweep2 = plain_angles(x, y, a=a)
    tail = tidal_tails(
        r1,
        r2,
        sweep1,
        sweep2,
        alpha_q=alpha_q,
        radius_q=radius_q,
        c_q=c_q,
        beta_q=beta_q,
        tails=tails,
        taper=taper,
    )
    potential = lambda_p * potential_weight(r1, r2, kappa=kappa_phi, epsilon=epsilon_phi)

    suppression = horizon_suppression(r1, r2, k_h=k_h, horizon_radius=horizon_radius)
    intensity = suppression * (rings + halo + bridge + tail + potential)
    return 1.0 - np.exp(-float(gamma_l) * intensity)


def v026_rgb(
    width: int,
    height: int,
    rate_r: float = 4.0,
    rate_g: float = 2.0,
    rate_b: float = 0.7,
    **field_parameters,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    level = v026_field(x, y, **field_parameters)
    return to_pixels(colour_equations(level, rate_r=rate_r, rate_g=rate_g, rate_b=rate_b))


def phase_series(
    width: int,
    height: int,
    phases: tuple[float, ...] = (0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi),
    gap: int = 8,
    **kwargs,
) -> np.ndarray:
    if len(phases) != 4:
        raise ValueError("phase_series expects four phases")

    tiles = [v026_rgb(width, height, phase=phase, **kwargs) for phase in phases]
    rule = np.zeros((height, gap, 3), dtype=np.uint8)
    top = np.hstack([tiles[0], rule, tiles[1]])
    bottom = np.hstack([tiles[2], rule, tiles[3]])
    spacer = np.zeros((gap, top.shape[1], 3), dtype=np.uint8)
    return np.vstack([top, spacer, bottom])


def parse_args() -> argparse.Namespace:
    parser = experiment_parser("Render v026 - final equation.", DEFAULT_OUTPUT)
    parser.add_argument("--a", type=float, default=0.36)
    parser.add_argument("--ring-radius", type=float, default=0.25)
    parser.add_argument("--sharpness", type=float, default=80.0)
    parser.add_argument("--horizon-radius", type=float, default=0.14)
    parser.add_argument("--k-h", type=float, default=600.0)
    parser.add_argument("--glow", type=float, default=0.30)
    parser.add_argument("--falloff", type=float, default=3.5)
    parser.add_argument("--gate-width", type=float, default=0.03)
    parser.add_argument("--order", type=int, default=4)
    parser.add_argument("--harmonic", type=float, default=0.30)
    parser.add_argument("--beta", type=float, default=0.28)
    parser.add_argument("--exponent", type=float, default=2.0)
    parser.add_argument("--decay", type=float, default=2.0)
    parser.add_argument("--distortion", type=float, default=-0.30)
    parser.add_argument("--alpha-i", type=float, default=1.5)
    parser.add_argument("--beta-i", type=float, default=3.0)
    parser.add_argument("--strength", type=float, default=1.00)
    parser.add_argument("--alpha-t", type=float, default=120.0)
    parser.add_argument("--beta-t", type=float, default=25.0)
    parser.add_argument("--eta-t", type=float, default=0.50)
    parser.add_argument("--k-t", type=float, default=32.0)
    parser.add_argument("--bridge-phase", type=float, default=0.0)
    parser.add_argument("--alpha-q", type=float, default=150.0)
    parser.add_argument("--radius-q", type=float, default=0.45)
    parser.add_argument("--c-q", type=float, default=0.25)
    parser.add_argument("--beta-q", type=float, default=1.5)
    parser.add_argument("--tails", type=float, default=0.60)
    parser.add_argument("--taper", type=float, default=0.5)
    parser.add_argument("--kappa-phi", type=float, default=0.15)
    parser.add_argument("--epsilon-phi", type=float, default=0.05)
    parser.add_argument("--lambda-p", type=float, default=0.25)
    parser.add_argument("--beta-d", type=float, default=0.30)
    parser.add_argument("--p-d", type=float, default=3.0)
    parser.add_argument("--epsilon-n", type=float, default=0.35)
    parser.add_argument("--k-r", type=float, default=90.0)
    parser.add_argument("--m-n", type=int, default=24)
    parser.add_argument("--c-n", type=float, default=6.0)
    parser.add_argument("--soft-n", type=float, default=0.02)
    parser.add_argument("--gamma-l", type=float, default=0.25)
    parser.add_argument("--pitch-degrees", type=float, default=None)
    parser.add_argument("--phase-degrees", type=float, default=0.0)
    parser.add_argument("--rate-r", type=float, default=4.0)
    parser.add_argument("--rate-g", type=float, default=2.0)
    parser.add_argument("--rate-b", type=float, default=0.7)
    parser.add_argument("--series", action="store_true")
    return parser.parse_args()


def main() -> None:
    options = vars(parse_args())
    width = options.pop("width")
    height = options.pop("height")
    output = options.pop("output")
    series = options.pop("series")

    pitch_degrees = options.pop("pitch_degrees")
    options["pitch"] = None if pitch_degrees is None else np.radians(pitch_degrees)
    phase = np.radians(options.pop("phase_degrees"))

    if series:
        rgb = phase_series(width, height, **options)
    else:
        rgb = v026_rgb(width, height, phase=phase, **options)
    save_and_report(output, rgb)


if __name__ == "__main__":
    main()
