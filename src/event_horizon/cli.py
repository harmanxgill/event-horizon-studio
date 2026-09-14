from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np

from .utils import save_rgb_image


def experiment_parser(description: str, default_output: Path) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--width", type=int, default=1200)
    parser.add_argument("--height", type=int, default=1200)
    parser.add_argument("--output", type=Path, default=default_output)
    return parser


def save_and_report(path: str | Path, rgb: np.ndarray) -> Path:
    output_path = save_rgb_image(path, rgb)
    print(f"saved {output_path}")
    return output_path
