from __future__ import annotations

import numpy as np

from .fields import normalized_grid, polar_angle


def coordinate_grids(width: int, height: int) -> tuple[np.ndarray, np.ndarray]:
    return normalized_grid(width=width, height=height, xlim=(-1.0, 1.0), ylim=(-1.0, 1.0))


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
