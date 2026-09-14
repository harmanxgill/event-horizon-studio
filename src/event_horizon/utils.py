from __future__ import annotations

from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt


def ensure_directory(path: str | Path) -> Path:
    directory = Path(path)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def save_rgb_image(path: str | Path, rgb: np.ndarray) -> Path:
    output_path = Path(path)
    ensure_directory(output_path.parent)
    plt.imsave(output_path, np.asarray(rgb))
    return output_path
