from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
PIECE_DIR = PROJECT_ROOT / "pieces" / "001_last_orbit"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

spec = importlib.util.spec_from_file_location("last_orbit_equations", PIECE_DIR / "equations.py")
equations = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(equations)

v001_spec = importlib.util.spec_from_file_location(
    "last_orbit_v001",
    PIECE_DIR / "experiments" / "v001_two_radial_fields.py",
)
v001 = importlib.util.module_from_spec(v001_spec)
assert v001_spec.loader is not None
v001_spec.loader.exec_module(v001)


def test_field_dimensions_and_finite_values() -> None:
    fields = equations.evaluate_fields(width=80, height=64)

    scalar_names = [
        "x",
        "y",
        "r1",
        "r2",
        "theta1",
        "theta2",
        "horizon1",
        "horizon2",
        "horizon_field",
        "accretion_placeholder",
        "spiral_placeholder",
        "tidal_placeholder",
    ]
    for name in scalar_names:
        assert fields[name].shape == (64, 80)
        assert np.isfinite(fields[name]).all()

    assert fields["horizon_mask"].shape == (64, 80)
    assert fields["horizon_mask"].dtype == bool


def test_equal_mass_centers_are_symmetric() -> None:
    center1, center2 = equations.black_hole_centers(separation=0.72, orbit_phase=0.0)

    assert np.allclose(center1, -center2)
    assert np.allclose(0.5 * (center1 + center2), np.array([0.0, 0.0]))


def test_equal_mass_radial_fields_mirror_across_centerline() -> None:
    fields = equations.evaluate_fields(width=81, height=65, orbit_phase=0.0)

    assert np.allclose(fields["r1"], np.fliplr(fields["r2"]))
    assert np.allclose(fields["horizon1"], np.fliplr(fields["horizon2"]))


def test_preview_intensity_is_finite_and_symmetric() -> None:
    fields = equations.evaluate_fields(width=81, height=65, orbit_phase=0.0)
    intensity = equations.preview_intensity(fields)

    assert intensity.shape == (65, 81)
    assert np.isfinite(intensity).all()
    assert np.allclose(intensity, np.fliplr(intensity))


def test_v001_expression_is_finite_and_symmetric() -> None:
    x, y = v001.coordinate_grids(width=81, height=65)
    field = v001.v001_field(x, y)
    rgb = v001.v001_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert np.allclose(field, np.fliplr(field))

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8
    assert np.array_equal(rgb, np.fliplr(rgb))
