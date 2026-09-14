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
from event_horizon.fields import polar_angle
from event_horizon.geometry import angular_fields, black_hole_centers, coordinate_grids, grid_spacing, radial_fields, wrap_angle


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "v017_outgoing_wave.png"


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


def phased_angles(
    theta1: np.ndarray,
    theta2: np.ndarray,
    phase: float = 0.0,
) -> tuple[np.ndarray, np.ndarray]:
    return wrap_angle(theta1 - float(phase)), wrap_angle(theta2 - float(phase))


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


def global_polar(x: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return np.sqrt(x**2 + y**2), np.arctan2(y, x)


def wave_phase(
    rho: np.ndarray,
    phase: float = 0.0,
    k_g: float = 28.0,
    omega_g: float = 2.0,
) -> np.ndarray:
    return float(k_g) * rho - float(omega_g) * float(phase)


def outgoing_wave(
    rho: np.ndarray,
    phase: float = 0.0,
    k_g: float = 28.0,
    omega_g: float = 2.0,
) -> np.ndarray:
    return np.cos(wave_phase(rho, phase=phase, k_g=k_g, omega_g=omega_g))


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


def radial_decay(r: np.ndarray, decay: float = 2.0) -> np.ndarray:
    if decay < 0.0:
        raise ValueError("decay must be non-negative")
    return np.exp(-float(decay) * r)


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
    pitch: float | None = None,
    decay: float = 2.0,
) -> np.ndarray:
    if pitch is None:
        pitch = natural_pitch(order, sharpness, ring_radius)

    phi1 = spiral_phase(theta1, r1, ring_radius, pitch)
    phi2 = spiral_phase(theta2, r2, ring_radius, pitch)
    w1 = ring_weight(phi1, anisotropy, order, harmonic, beta, exponent)
    w2 = ring_weight(phi2, anisotropy, order, harmonic, beta, exponent)
    a1 = np.exp(-sharpness * (r1 - ring_radius) ** 2) * w1 * radial_decay(r1, decay)
    a2 = np.exp(-sharpness * (r2 - ring_radius) ** 2) * w2 * radial_decay(r2, decay)
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


def v017_field(
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
    k_g: float = 28.0,
    omega_g: float = 2.0,
    lambda_w: float = 0.05,
) -> np.ndarray:
    if edge_pixels <= 0.0:
        raise ValueError("edge_pixels must be positive")

    r1, r2 = radial_fields(x, y, a=a)
    theta1, theta2 = angular_fields(x, y, a=a)
    d1, d2 = distorted_radii(r1, r2, theta1, theta2, distortion)
    theta1, theta2 = phased_angles(theta1, theta2, phase)
    rings = ring_field(
        d1,
        d2,
        theta1,
        theta2,
        ring_radius=ring_radius,
        sharpness=sharpness,
        anisotropy=anisotropy,
        order=order,
        harmonic=harmonic,
        beta=beta,
        exponent=exponent,
        pitch=pitch,
        decay=decay,
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

    potential = lambda_p * potential_weight(
        r1, r2, kappa=kappa_phi, epsilon=epsilon_phi
    )

    rho, _theta_global = global_polar(x, y)
    wave = lambda_w * outgoing_wave(rho, phase=phase, k_g=k_g, omega_g=omega_g)

    horizon_edge = float(edge_pixels) * grid_spacing(x, y)
    silhouette = silhouette_field(r1, r2, horizon_edge, horizon_radius=horizon_radius)
    return (rings + halo + bridge + tail + potential + wave) * (1.0 - silhouette)


def v017_rgb(
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
    k_g: float = 28.0,
    omega_g: float = 2.0,
    lambda_w: float = 0.05,
) -> np.ndarray:
    x, y = coordinate_grids(width, height)
    f = v017_field(
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
        pitch=pitch,
        decay=decay,
        phase=phase,
        distortion=distortion,
        alpha_i=alpha_i,
        beta_i=beta_i,
        strength=strength,
        alpha_t=alpha_t,
        beta_t=beta_t,
        eta_t=eta_t,
        k_t=k_t,
        bridge_phase=bridge_phase,
        alpha_q=alpha_q,
        radius_q=radius_q,
        c_q=c_q,
        beta_q=beta_q,
        tails=tails,
        taper=taper,
        kappa_phi=kappa_phi,
        epsilon_phi=epsilon_phi,
        lambda_p=lambda_p,
        k_g=k_g,
        omega_g=omega_g,
        lambda_w=lambda_w,
    )

    return warm_rgb(f)


def phase_series(
    width: int,
    height: int,
    phases: tuple[float, ...] = (0.0, 0.5 * np.pi, np.pi, 1.5 * np.pi),
    gap: int = 8,
    **kwargs,
) -> np.ndarray:
    if len(phases) != 4:
        raise ValueError("phase_series expects four phases")

    tiles = [v017_rgb(width, height, phase=phase, **kwargs) for phase in phases]
    rule = np.zeros((height, gap, 3), dtype=np.uint8)
    top = np.hstack([tiles[0], rule, tiles[1]])
    bottom = np.hstack([tiles[2], rule, tiles[3]])
    spacer = np.zeros((gap, top.shape[1], 3), dtype=np.uint8)
    return np.vstack([top, spacer, bottom])


def parse_args() -> argparse.Namespace:
    parser = experiment_parser("Render v017 - outgoing wave phase.", DEFAULT_OUTPUT)
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
    parser.add_argument("--pitch-degrees", type=float, default=None)
    parser.add_argument("--decay", type=float, default=2.0)
    parser.add_argument("--phase-degrees", type=float, default=0.0)
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
    parser.add_argument("--k-g", type=float, default=28.0)
    parser.add_argument("--omega-g", type=float, default=2.0)
    parser.add_argument("--lambda-w", type=float, default=0.05)
    parser.add_argument("--series", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    render = phase_series if args.series else v017_rgb
    rgb = render(
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
        pitch=None if args.pitch_degrees is None else np.radians(args.pitch_degrees),
        decay=args.decay,
        distortion=args.distortion,
        alpha_i=args.alpha_i,
        beta_i=args.beta_i,
        strength=args.strength,
        alpha_t=args.alpha_t,
        beta_t=args.beta_t,
        eta_t=args.eta_t,
        k_t=args.k_t,
        bridge_phase=args.bridge_phase,
        alpha_q=args.alpha_q,
        radius_q=args.radius_q,
        c_q=args.c_q,
        beta_q=args.beta_q,
        tails=args.tails,
        taper=args.taper,
        kappa_phi=args.kappa_phi,
        epsilon_phi=args.epsilon_phi,
        lambda_p=args.lambda_p,
        k_g=args.k_g,
        omega_g=args.omega_g,
        lambda_w=args.lambda_w,
        **({} if args.series else {"phase": np.radians(args.phase_degrees)}),
    )
    save_and_report(args.output, rgb)


if __name__ == "__main__":
    main()
