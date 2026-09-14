from __future__ import annotations

import numpy as np
from matplotlib import colormaps


def normalize01(
    values: np.ndarray,
    vmin: float | None = None,
    vmax: float | None = None,
    percentiles: tuple[float, float] = (1.0, 99.0),
) -> np.ndarray:
    field = np.asarray(values, dtype=float)
    finite = np.isfinite(field)
    if not finite.any():
        return np.zeros_like(field, dtype=float)

    finite_values = field[finite]
    if vmin is None:
        vmin = float(np.percentile(finite_values, percentiles[0]))
    if vmax is None:
        vmax = float(np.percentile(finite_values, percentiles[1]))

    if not np.isfinite(vmin) or not np.isfinite(vmax) or vmax <= vmin:
        return np.zeros_like(field, dtype=float)

    normalized = (field - vmin) / (vmax - vmin)
    normalized = np.nan_to_num(normalized, nan=0.0, posinf=1.0, neginf=0.0)
    return np.clip(normalized, 0.0, 1.0)


def scalar_to_rgb(
    values: np.ndarray,
    cmap: str = "magma",
    vmin: float | None = None,
    vmax: float | None = None,
) -> np.ndarray:
    normalized = normalize01(values, vmin=vmin, vmax=vmax)
    rgba = colormaps.get_cmap(cmap)(normalized)
    return np.round(rgba[..., :3] * 255.0).astype(np.uint8)


def paint_mask(
    rgb: np.ndarray,
    mask: np.ndarray,
    color: tuple[int, int, int] = (0, 0, 0),
) -> np.ndarray:
    result = np.array(rgb, copy=True)
    result[np.asarray(mask, dtype=bool)] = np.asarray(color, dtype=result.dtype)
    return result
