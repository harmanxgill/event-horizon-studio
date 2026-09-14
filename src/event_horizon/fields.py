from __future__ import annotations

from collections.abc import Sequence

import numpy as np


def normalized_grid(
    width: int,
    height: int,
    xlim: tuple[float, float] = (-1.0, 1.0),
    ylim: tuple[float, float] = (-1.0, 1.0),
) -> tuple[np.ndarray, np.ndarray]:
    if width <= 0 or height <= 0:
        raise ValueError("width and height must be positive")

    xs = np.linspace(float(xlim[0]), float(xlim[1]), int(width))
    ys = np.linspace(float(ylim[1]), float(ylim[0]), int(height))
    return np.meshgrid(xs, ys)


def radial_distance(
    x: np.ndarray,
    y: np.ndarray,
    center: Sequence[float],
    softening: float = 0.0,
) -> np.ndarray:
    cx, cy = float(center[0]), float(center[1])
    return np.sqrt((x - cx) ** 2 + (y - cy) ** 2 + float(softening) ** 2)


def polar_angle(x: np.ndarray, y: np.ndarray, center: Sequence[float]) -> np.ndarray:
    cx, cy = float(center[0]), float(center[1])
    return np.arctan2(y - cy, x - cx)


def soft_horizon(r: np.ndarray, radius: float, edge_width: float) -> np.ndarray:
    if radius <= 0:
        raise ValueError("radius must be positive")
    if edge_width <= 0:
        raise ValueError("edge_width must be positive")

    z = np.clip((r - float(radius)) / float(edge_width), -60.0, 60.0)
    return 1.0 / (1.0 + np.exp(z))
