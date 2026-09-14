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


v002_spec = importlib.util.spec_from_file_location(
    "last_orbit_v002",
    PIECE_DIR / "experiments" / "v002_horizon_masks.py",
)
v002 = importlib.util.module_from_spec(v002_spec)
assert v002_spec.loader is not None
v002_spec.loader.exec_module(v002)


v003_spec = importlib.util.spec_from_file_location(
    "last_orbit_v003",
    PIECE_DIR / "experiments" / "v003_sharp_horizons.py",
)
v003 = importlib.util.module_from_spec(v003_spec)
assert v003_spec.loader is not None
v003_spec.loader.exec_module(v003)


v004_spec = importlib.util.spec_from_file_location(
    "last_orbit_v004",
    PIECE_DIR / "experiments" / "v004_outer_glow.py",
)
v004 = importlib.util.module_from_spec(v004_spec)
assert v004_spec.loader is not None
v004_spec.loader.exec_module(v004)


v005_spec = importlib.util.spec_from_file_location(
    "last_orbit_v005",
    PIECE_DIR / "experiments" / "v005_angular_fields.py",
)
v005 = importlib.util.module_from_spec(v005_spec)
assert v005_spec.loader is not None
v005_spec.loader.exec_module(v005)


v006_spec = importlib.util.spec_from_file_location(
    "last_orbit_v006",
    PIECE_DIR / "experiments" / "v006_beamed_rings.py",
)
v006 = importlib.util.module_from_spec(v006_spec)
assert v006_spec.loader is not None
v006_spec.loader.exec_module(v006)


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


def test_v002_expression_is_finite_and_symmetric() -> None:
    x, y = v002.coordinate_grids(width=81, height=65)
    field = v002.v002_field(x, y)
    rgb = v002.v002_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert np.allclose(field, np.fliplr(field))

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8
    assert np.array_equal(rgb, np.fliplr(rgb))


def test_v002_horizon_centers_are_dark() -> None:
    x, y = v002.coordinate_grids(width=81, height=65)
    r1, r2 = v002.radial_fields(x, y)
    field = v002.v002_field(x, y)

    inside = (r1 <= 0.5 * 0.14) | (r2 <= 0.5 * 0.14)
    assert inside.any()
    assert field[inside].max() < 1.0e-3


def test_v002_masks_the_v001_ring_only_near_the_centers() -> None:
    x, y = v002.coordinate_grids(width=81, height=65)
    r1, r2 = v002.radial_fields(x, y)

    rings = v002.ring_field(r1, r2)
    masked = v002.v002_field(x, y)

    assert np.all(masked <= rings + 1.0e-12)

    far = (r1 > 4.0 * 0.14) & (r2 > 4.0 * 0.14)
    assert far.any()
    assert np.allclose(masked[far], rings[far])


def test_v003_expression_is_finite_and_symmetric() -> None:
    x, y = v003.coordinate_grids(width=81, height=65)
    field = v003.v003_field(x, y)
    rgb = v003.v003_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert np.allclose(field, np.fliplr(field))

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8
    assert np.array_equal(rgb, np.fliplr(rgb))


def test_v003_silhouettes_are_solid_black() -> None:
    x, y = v003.coordinate_grids(width=400, height=400)
    r1, r2 = v003.radial_fields(x, y)
    field = v003.v003_field(x, y)

    margin = 6.0 * v003.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v003_leaves_the_rings_untouched_away_from_the_horizons() -> None:
    x, y = v003.coordinate_grids(width=400, height=400)
    r1, r2 = v003.radial_fields(x, y)

    rings = v003.ring_field(r1, r2)
    masked = v003.v003_field(x, y)

    assert np.all(masked <= rings + 1.0e-12)

    far = (r1 > 2.0 * 0.14) & (r2 > 2.0 * 0.14)
    assert far.any()
    assert np.allclose(masked[far], rings[far])


def test_v003_boundary_is_sharper_than_v002() -> None:
    x, y = v003.coordinate_grids(width=400, height=400)
    r1, r2 = v003.radial_fields(x, y)

    soft = v003.silhouette_field(r1, r2, horizon_edge=0.015)
    sharp = v003.silhouette_field(r1, r2, horizon_edge=v003.grid_spacing(x, y))

    soft_band = int(((soft > 0.01) & (soft < 0.99)).sum())
    sharp_band = int(((sharp > 0.01) & (sharp < 0.99)).sum())

    assert sharp_band > 0
    assert sharp_band < soft_band


def test_v003_edge_stays_one_pixel_wide_at_any_resolution() -> None:
    widths = (200, 400, 800)
    bands = []
    for width in widths:
        x, y = v003.coordinate_grids(width=width, height=width)
        r1, r2 = v003.radial_fields(x, y)
        silhouette = v003.silhouette_field(r1, r2, v003.grid_spacing(x, y))
        bands.append(int(((silhouette > 0.01) & (silhouette < 0.99)).sum()))

    for coarse, fine, width_coarse, width_fine in zip(bands, bands[1:], widths, widths[1:]):
        expected = coarse * (width_fine / width_coarse)
        assert abs(fine - expected) < 0.25 * expected


def test_v003_rejects_a_degenerate_grid() -> None:
    import pytest

    x, y = v003.coordinate_grids(width=1, height=1)
    with pytest.raises(ValueError):
        v003.grid_spacing(x, y)

    x, y = v003.coordinate_grids(width=16, height=16)
    with pytest.raises(ValueError):
        v003.v003_field(x, y, edge_pixels=0.0)


def test_v004_expression_is_finite_and_symmetric() -> None:
    x, y = v004.coordinate_grids(width=81, height=65)
    field = v004.v004_field(x, y)
    rgb = v004.v004_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert np.allclose(field, np.fliplr(field))

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8
    assert np.array_equal(rgb, np.fliplr(rgb))


def test_v004_glow_starts_outside_the_ring() -> None:
    onset = v004.glow_onset()

    assert onset > 0.25
    assert np.isclose(onset, 0.25 + 1.0 / np.sqrt(80.0))

    inside = np.linspace(0.0, 0.25, 64)
    assert v004.outer_glow(inside, onset).max() < 0.02


def test_v004_glow_peaks_outside_then_decays() -> None:
    onset = v004.glow_onset()
    r = np.linspace(0.0, 2.0, 4000)
    glow = v004.outer_glow(r, onset)

    peak = float(r[glow.argmax()])
    assert peak > onset

    tail = glow[r >= peak]
    assert np.all(np.diff(tail) < 0.0)
    assert float(glow[-1]) < 0.05 * float(glow.max())


def test_v004_only_adds_light_to_v003() -> None:
    x, y = v004.coordinate_grids(width=400, height=400)
    field3 = v003.v003_field(x, y)
    field4 = v004.v004_field(x, y)

    assert np.all(field4 >= field3 - 1.0e-12)

    r1, r2 = v004.radial_fields(x, y)
    outer = (r1 > 0.6) & (r2 > 0.6)
    assert outer.any()
    assert field4[outer].mean() > 2.0 * field3[outer].mean()


def test_v004_keeps_the_silhouettes_solid() -> None:
    x, y = v004.coordinate_grids(width=400, height=400)
    r1, r2 = v004.radial_fields(x, y)
    field = v004.v004_field(x, y)

    margin = 6.0 * v004.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v004_rejects_invalid_glow_parameters() -> None:
    import pytest

    r = np.linspace(0.1, 1.0, 16)
    with pytest.raises(ValueError):
        v004.outer_glow(r, 0.36, glow=-0.1)
    with pytest.raises(ValueError):
        v004.outer_glow(r, 0.36, falloff=0.0)
    with pytest.raises(ValueError):
        v004.glow_onset(sharpness=0.0)


def test_v005_expression_is_finite_and_symmetric() -> None:
    x, y = v005.coordinate_grids(width=81, height=65)
    field = v005.v005_field(x, y)
    rgb = v005.v005_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert np.allclose(field, np.fliplr(field))

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8
    assert np.array_equal(rgb, np.fliplr(rgb))


def test_v005_angles_are_wrapped_and_centered_on_each_hole() -> None:
    x, y = v005.coordinate_grids(width=201, height=201)
    theta1, theta2 = v005.angular_fields(x, y)

    for theta in (theta1, theta2):
        assert theta.shape == (201, 201)
        assert np.isfinite(theta).all()
        assert theta.min() >= -np.pi - 1.0e-12
        assert theta.max() <= np.pi + 1.0e-12

    center1, center2 = v005.black_hole_centers()
    assert center1 == (-0.36, 0.0)
    assert center2 == (0.36, 0.0)


def test_v005_zero_angle_points_at_the_companion() -> None:
    center1, center2 = v005.black_hole_centers()

    toward2 = np.array([[center1[0] + 0.1]]), np.array([[0.0]])
    toward1 = np.array([[center2[0] - 0.1]]), np.array([[0.0]])

    theta1, _ = v005.angular_fields(*toward2)
    _, theta2 = v005.angular_fields(*toward1)

    assert np.allclose(theta1, 0.0)
    assert np.allclose(theta2, 0.0)

    away2 = np.array([[center1[0] - 0.1]]), np.array([[0.0]])
    away1 = np.array([[center2[0] + 0.1]]), np.array([[0.0]])

    theta1_away, _ = v005.angular_fields(*away2)
    _, theta2_away = v005.angular_fields(*away1)

    assert np.allclose(np.abs(theta1_away), np.pi)
    assert np.allclose(np.abs(theta2_away), np.pi)


def test_v005_wrap_angle_folds_into_a_single_turn() -> None:
    theta = np.linspace(-9.0, 9.0, 512)
    wrapped = v005.wrap_angle(theta)

    assert wrapped.min() >= -np.pi - 1.0e-12
    assert wrapped.max() <= np.pi + 1.0e-12
    assert np.allclose(np.cos(wrapped), np.cos(theta))
    assert np.allclose(np.sin(wrapped), np.sin(theta))
    assert np.allclose(v005.wrap_angle(wrapped), wrapped)


def test_v005_angular_weight_is_bounded_and_averages_to_one() -> None:
    theta = np.linspace(-np.pi, np.pi, 4096, endpoint=False)

    for anisotropy in (0.0, 0.35, -0.35, 1.0):
        weight = v005.angular_weight(theta, anisotropy)
        assert weight.min() >= 1.0 - abs(anisotropy) - 1.0e-12
        assert weight.max() <= 1.0 + abs(anisotropy) + 1.0e-12
        assert np.isclose(weight.mean(), 1.0, atol=1.0e-6)
        assert np.all(weight >= 0.0)


def test_v005_brightens_the_facing_sides_of_each_ring() -> None:
    x, y = v005.coordinate_grids(width=600, height=600)
    r1, r2 = v005.radial_fields(x, y)
    field = v005.v005_field(x, y)

    on_ring1 = np.abs(r1 - 0.25) < 0.02
    facing = on_ring1 & (x > -0.36)
    away = on_ring1 & (x < -0.36)

    assert facing.any() and away.any()
    assert field[facing].mean() > field[away].mean()


def test_v005_reduces_to_v004_without_anisotropy() -> None:
    x, y = v005.coordinate_grids(width=200, height=200)

    assert np.allclose(v005.v005_field(x, y, anisotropy=0.0), v004.v004_field(x, y))


def test_v005_rejects_out_of_range_anisotropy() -> None:
    import pytest

    theta = np.linspace(-np.pi, np.pi, 16)
    for bad in (1.5, -1.5):
        with pytest.raises(ValueError):
            v005.angular_weight(theta, bad)


def test_v006_expression_is_finite() -> None:
    x, y = v006.coordinate_grids(width=81, height=65)
    field = v006.v006_field(x, y)
    rgb = v006.v006_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v006_trades_mirror_symmetry_for_rotation_symmetry() -> None:
    x, y = v006.coordinate_grids(width=201, height=201)
    field = v006.v006_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v006_beaming_is_normalised_and_peaks_along_the_orbit() -> None:
    theta = np.linspace(-np.pi, np.pi, 4096, endpoint=False)
    weight = v006.beaming_weight(theta)

    assert np.isclose(weight.mean(), 1.0, atol=1.0e-6)
    assert np.all(weight > 0.0)
    assert np.isclose(float(theta[weight.argmax()]), v006.ORBITAL_OFFSET, atol=1.0e-2)
    assert np.isclose(float(theta[weight.argmin()]), v006.ORBITAL_OFFSET + np.pi, atol=1.0e-2)
    assert weight.max() / weight.min() > 2.0


def test_v006_doppler_mean_matches_the_closed_form() -> None:
    for beta in (0.0, 0.15, 0.28, 0.5, 0.8):
        assert np.isclose(v006.doppler_mean(beta, 1.0), 1.0 / np.sqrt(1.0 - beta**2), rtol=1.0e-4)


def test_v006_modulations_are_orthogonal() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    for anisotropy in (0.0, 0.2, 0.5, -0.4):
        combined = v006.angular_weight(theta, anisotropy) * v006.beaming_weight(theta)
        assert np.isclose(combined.mean(), 1.0, atol=1.0e-6)


def test_v006_reduces_to_v005_without_beaming() -> None:
    x, y = v006.coordinate_grids(width=200, height=200)

    assert np.allclose(v006.beaming_weight(np.linspace(-np.pi, np.pi, 64), beta=0.0), 1.0)
    assert np.allclose(
        v006.v006_field(x, y, anisotropy=0.35, beta=0.0),
        v005.v005_field(x, y),
    )


def test_v006_rings_are_less_uniform_than_v005() -> None:
    x, y = v006.coordinate_grids(width=600, height=600)
    r1, _ = v006.radial_fields(x, y)
    on_ring = np.abs(r1 - 0.25) < 0.02
    assert on_ring.any()

    spread5 = v005.v005_field(x, y)[on_ring]
    spread6 = v006.v006_field(x, y)[on_ring]

    assert spread6.max() / spread6.min() > spread5.max() / spread5.min()


def test_v006_keeps_the_silhouettes_solid() -> None:
    x, y = v006.coordinate_grids(width=400, height=400)
    r1, r2 = v006.radial_fields(x, y)
    field = v006.v006_field(x, y)

    margin = 6.0 * v006.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v006_rejects_invalid_beaming_parameters() -> None:
    import pytest

    theta = np.linspace(-np.pi, np.pi, 16)
    for bad_beta in (-0.1, 1.0, 1.5):
        with pytest.raises(ValueError):
            v006.beaming_weight(theta, beta=bad_beta)
    with pytest.raises(ValueError):
        v006.beaming_weight(theta, exponent=-1.0)
