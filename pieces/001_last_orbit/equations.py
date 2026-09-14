from __future__ import annotations

import numpy as np

from event_horizon.fields import normalized_grid, polar_angle, radial_distance, soft_horizon


DEFAULT_PARAMETERS = {
    "extent": 1.25,
    "separation": 0.72,
    "orbit_phase": 0.0,
    "horizon_radius": 0.14,
    "horizon_edge": 0.015,
    "softening": 1.0e-6,
}


def coordinate_grids(
    width: int,
    height: int,
    extent: float = DEFAULT_PARAMETERS["extent"],
) -> tuple[np.ndarray, np.ndarray]:
    return normalized_grid(
        width=width,
        height=height,
        xlim=(-float(extent), float(extent)),
        ylim=(-float(extent), float(extent)),
    )


def black_hole_centers(
    separation: float = DEFAULT_PARAMETERS["separation"],
    orbit_phase: float = DEFAULT_PARAMETERS["orbit_phase"],
) -> tuple[np.ndarray, np.ndarray]:
    half = 0.5 * float(separation)
    direction = np.array([np.cos(orbit_phase), np.sin(orbit_phase)], dtype=float)
    return -half * direction, half * direction


def horizon_fields(
    r1: np.ndarray,
    r2: np.ndarray,
    horizon_radius: float = DEFAULT_PARAMETERS["horizon_radius"],
    horizon_edge: float = DEFAULT_PARAMETERS["horizon_edge"],
) -> dict[str, np.ndarray]:
    horizon1 = soft_horizon(r1, horizon_radius, horizon_edge)
    horizon2 = soft_horizon(r2, horizon_radius, horizon_edge)
    horizon_mask = (r1 <= horizon_radius) | (r2 <= horizon_radius)
    return {
        "horizon1": horizon1,
        "horizon2": horizon2,
        "horizon_field": np.maximum(horizon1, horizon2),
        "horizon_mask": horizon_mask,
    }


def accretion_placeholder(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    return np.zeros_like(x + y, dtype=float)


def spiral_placeholder(
    r1: np.ndarray,
    r2: np.ndarray,
    theta1: np.ndarray,
    theta2: np.ndarray,
) -> np.ndarray:
    return np.zeros_like(r1 + r2 + theta1 + theta2, dtype=float)


def tidal_placeholder(r1: np.ndarray, r2: np.ndarray) -> np.ndarray:
    return np.zeros_like(r1 + r2, dtype=float)


def evaluate_fields(
    width: int,
    height: int,
    extent: float = DEFAULT_PARAMETERS["extent"],
    separation: float = DEFAULT_PARAMETERS["separation"],
    orbit_phase: float = DEFAULT_PARAMETERS["orbit_phase"],
    horizon_radius: float = DEFAULT_PARAMETERS["horizon_radius"],
    horizon_edge: float = DEFAULT_PARAMETERS["horizon_edge"],
    softening: float = DEFAULT_PARAMETERS["softening"],
) -> dict[str, np.ndarray]:
    x, y = coordinate_grids(width=width, height=height, extent=extent)
    center1, center2 = black_hole_centers(separation=separation, orbit_phase=orbit_phase)

    r1 = radial_distance(x, y, center1, softening=softening)
    r2 = radial_distance(x, y, center2, softening=softening)
    theta1 = polar_angle(x, y, center1)
    theta2 = polar_angle(x, y, center2)

    fields = {
        "x": x,
        "y": y,
        "center1": center1,
        "center2": center2,
        "r1": r1,
        "r2": r2,
        "theta1": theta1,
        "theta2": theta2,
    }
    fields.update(horizon_fields(r1, r2, horizon_radius=horizon_radius, horizon_edge=horizon_edge))
    fields["accretion_placeholder"] = accretion_placeholder(x, y)
    fields["spiral_placeholder"] = spiral_placeholder(r1, r2, theta1, theta2)
    fields["tidal_placeholder"] = tidal_placeholder(r1, r2)
    return fields


def preview_intensity(fields: dict[str, np.ndarray]) -> np.ndarray:
    r_min = np.minimum(fields["r1"], fields["r2"])
    center_glow = np.exp(-5.0 * r_min)
    bridge = np.exp(-3.0 * (fields["r1"] + fields["r2"]))
    shadow = fields["horizon_field"]
    return center_glow + 0.35 * bridge - 0.85 * shadow
