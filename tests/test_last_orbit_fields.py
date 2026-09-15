from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np
import pytest


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


v007_spec = importlib.util.spec_from_file_location(
    "last_orbit_v007",
    PIECE_DIR / "experiments" / "v007_structured_light.py",
)
v007 = importlib.util.module_from_spec(v007_spec)
assert v007_spec.loader is not None
v007_spec.loader.exec_module(v007)


v008_spec = importlib.util.spec_from_file_location(
    "last_orbit_v008",
    PIECE_DIR / "experiments" / "v008_coupled_radius.py",
)
v008 = importlib.util.module_from_spec(v008_spec)
assert v008_spec.loader is not None
v008_spec.loader.exec_module(v008)


v009_spec = importlib.util.spec_from_file_location(
    "last_orbit_v009",
    PIECE_DIR / "experiments" / "v009_log_spiral.py",
)
v009 = importlib.util.module_from_spec(v009_spec)
assert v009_spec.loader is not None
v009_spec.loader.exec_module(v009)


v010_spec = importlib.util.spec_from_file_location(
    "last_orbit_v010",
    PIECE_DIR / "experiments" / "v010_spiral_decay.py",
)
v010 = importlib.util.module_from_spec(v010_spec)
assert v010_spec.loader is not None
v010_spec.loader.exec_module(v010)


v011_spec = importlib.util.spec_from_file_location(
    "last_orbit_v011",
    PIECE_DIR / "experiments" / "v011_orbital_phase.py",
)
v011 = importlib.util.module_from_spec(v011_spec)
assert v011_spec.loader is not None
v011_spec.loader.exec_module(v011)


v012_spec = importlib.util.spec_from_file_location(
    "last_orbit_v012",
    PIECE_DIR / "experiments" / "v012_companion_distortion.py",
)
v012 = importlib.util.module_from_spec(v012_spec)
assert v012_spec.loader is not None
v012_spec.loader.exec_module(v012)


v013_spec = importlib.util.spec_from_file_location(
    "last_orbit_v013",
    PIECE_DIR / "experiments" / "v013_interaction_field.py",
)
v013 = importlib.util.module_from_spec(v013_spec)
assert v013_spec.loader is not None
v013_spec.loader.exec_module(v013)


v014_spec = importlib.util.spec_from_file_location(
    "last_orbit_v014",
    PIECE_DIR / "experiments" / "v014_tidal_bridge.py",
)
v014 = importlib.util.module_from_spec(v014_spec)
assert v014_spec.loader is not None
v014_spec.loader.exec_module(v014)


v015_spec = importlib.util.spec_from_file_location(
    "last_orbit_v015",
    PIECE_DIR / "experiments" / "v015_tidal_tails.py",
)
v015 = importlib.util.module_from_spec(v015_spec)
assert v015_spec.loader is not None
v015_spec.loader.exec_module(v015)


v016_spec = importlib.util.spec_from_file_location(
    "last_orbit_v016",
    PIECE_DIR / "experiments" / "v016_global_potential.py",
)
v016 = importlib.util.module_from_spec(v016_spec)
assert v016_spec.loader is not None
v016_spec.loader.exec_module(v016)


v017_spec = importlib.util.spec_from_file_location(
    "last_orbit_v017",
    PIECE_DIR / "experiments" / "v017_outgoing_wave.py",
)
v017 = importlib.util.module_from_spec(v017_spec)
assert v017_spec.loader is not None
v017_spec.loader.exec_module(v017)


v018_spec = importlib.util.spec_from_file_location(
    "last_orbit_v018",
    PIECE_DIR / "experiments" / "v018_quadrupolar_field.py",
)
v018 = importlib.util.module_from_spec(v018_spec)
assert v018_spec.loader is not None
v018_spec.loader.exec_module(v018)


v019_spec = importlib.util.spec_from_file_location(
    "last_orbit_v019",
    PIECE_DIR / "experiments" / "v019_velocity_field.py",
)
v019 = importlib.util.module_from_spec(v019_spec)
assert v019_spec.loader is not None
v019_spec.loader.exec_module(v019)


v020_spec = importlib.util.spec_from_file_location(
    "last_orbit_v020",
    PIECE_DIR / "experiments" / "v020_doppler_luminosity.py",
)
v020 = importlib.util.module_from_spec(v020_spec)
assert v020_spec.loader is not None
v020_spec.loader.exec_module(v020)


v021_spec = importlib.util.spec_from_file_location(
    "last_orbit_v021",
    PIECE_DIR / "experiments" / "v021_nonlinear_intensity.py",
)
v021 = importlib.util.module_from_spec(v021_spec)
assert v021_spec.loader is not None
v021_spec.loader.exec_module(v021)


v022_spec = importlib.util.spec_from_file_location(
    "last_orbit_v022",
    PIECE_DIR / "experiments" / "v022_rgb_equations.py",
)
v022 = importlib.util.module_from_spec(v022_spec)
assert v022_spec.loader is not None
v022_spec.loader.exec_module(v022)


v023_spec = importlib.util.spec_from_file_location(
    "last_orbit_v023",
    PIECE_DIR / "experiments" / "v023_mathematical_background.py",
)
v023 = importlib.util.module_from_spec(v023_spec)
assert v023_spec.loader is not None
v023_spec.loader.exec_module(v023)


v024_spec = importlib.util.spec_from_file_location(
    "last_orbit_v024",
    PIECE_DIR / "experiments" / "v024_fine_structure.py",
)
v024 = importlib.util.module_from_spec(v024_spec)
assert v024_spec.loader is not None
v024_spec.loader.exec_module(v024)


v025_spec = importlib.util.spec_from_file_location(
    "last_orbit_v025",
    PIECE_DIR / "experiments" / "v025_horizon_suppression.py",
)
v025 = importlib.util.module_from_spec(v025_spec)
assert v025_spec.loader is not None
v025_spec.loader.exec_module(v025)


v026_spec = importlib.util.spec_from_file_location(
    "last_orbit_v026",
    PIECE_DIR / "experiments" / "v026_final_equation.py",
)
v026 = importlib.util.module_from_spec(v026_spec)
assert v026_spec.loader is not None
v026_spec.loader.exec_module(v026)


v027_spec = importlib.util.spec_from_file_location(
    "last_orbit_v027",
    PIECE_DIR / "experiments" / "v027_horizon_lensing.py",
)
v027 = importlib.util.module_from_spec(v027_spec)
assert v027_spec.loader is not None
v027_spec.loader.exec_module(v027)


v028_spec = importlib.util.spec_from_file_location(
    "last_orbit_v028",
    PIECE_DIR / "experiments" / "v028_evolving_ripples.py",
)
v028 = importlib.util.module_from_spec(v028_spec)
assert v028_spec.loader is not None
v028_spec.loader.exec_module(v028)


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


def test_v007_expression_is_finite() -> None:
    x, y = v007.coordinate_grids(width=81, height=65)
    field = v007.v007_field(x, y)
    rgb = v007.v007_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v007_keeps_the_half_turn_symmetry() -> None:
    x, y = v007.coordinate_grids(width=201, height=201)
    field = v007.v007_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v007_harmonic_has_the_requested_number_of_lobes() -> None:
    theta = np.linspace(-np.pi, np.pi, 20000, endpoint=False)

    for order in (1, 2, 3, 4, 5, 8):
        weight = v007.harmonic_weight(theta, order=order, harmonic=0.5)
        peaks = (weight > np.roll(weight, 1)) & (weight > np.roll(weight, -1))
        assert int(peaks.sum()) == order


def test_v007_ring_weight_is_brightness_neutral_at_every_order() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    for order in range(1, 9):
        for harmonic in (0.0, 0.3, 0.6, -0.3):
            weight = v007.ring_weight(theta, order=order, harmonic=harmonic)
            assert np.isclose(weight.mean(), 1.0, atol=1.0e-9)
            assert np.all(weight > 0.0)


def test_v007_harmonic_deepens_the_ring_structure() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    flat = v007.ring_weight(theta, harmonic=0.0)
    structured = v007.ring_weight(theta, harmonic=0.3)

    assert structured.max() / structured.min() > flat.max() / flat.min()


def test_v007_reduces_to_v006_without_the_harmonic() -> None:
    x, y = v007.coordinate_grids(width=200, height=200)

    assert np.allclose(v007.v007_field(x, y, harmonic=0.0), v006.v006_field(x, y))


def test_v007_doppler_factor_is_the_unnormalised_beaming_term() -> None:
    theta = np.linspace(-np.pi, np.pi, 4096, endpoint=False)

    factor = v007.doppler_factor(theta)
    assert np.allclose(factor / factor.mean(), v006.beaming_weight(theta), rtol=1.0e-6)


def test_v007_keeps_the_silhouettes_solid() -> None:
    x, y = v007.coordinate_grids(width=400, height=400)
    r1, r2 = v007.radial_fields(x, y)
    field = v007.v007_field(x, y)

    margin = 6.0 * v007.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v007_rejects_invalid_harmonic_parameters() -> None:
    import pytest

    theta = np.linspace(-np.pi, np.pi, 16)
    for bad_order in (0, -1):
        with pytest.raises(ValueError):
            v007.harmonic_weight(theta, order=bad_order)
    for bad_harmonic in (1.5, -1.5):
        with pytest.raises(ValueError):
            v007.harmonic_weight(theta, harmonic=bad_harmonic)


def test_v008_expression_is_finite() -> None:
    x, y = v008.coordinate_grids(width=81, height=65)
    field = v008.v008_field(x, y)
    rgb = v008.v008_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v008_keeps_the_half_turn_symmetry() -> None:
    x, y = v008.coordinate_grids(width=201, height=201)
    field = v008.v008_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v008_coupling_vanishes_on_the_ring_and_grows_with_radius() -> None:
    theta = np.linspace(-np.pi, np.pi, 256)
    on_ring = np.full_like(theta, 0.25)

    assert np.allclose(v008.coupled_angle(theta, on_ring), theta)

    for r in (0.15, 0.35, 0.50):
        shifted = v008.coupled_angle(theta, np.full_like(theta, r))
        assert np.allclose(shifted - theta, 7.0 * (r - 0.25))


def test_v008_natural_twist_shears_half_a_lobe_per_ring_width() -> None:
    for order in (2, 3, 4, 6):
        for sharpness in (40.0, 80.0, 160.0):
            twist = v008.natural_twist(order=order, sharpness=sharpness)
            ring_width = 1.0 / np.sqrt(sharpness)
            lobe_spacing = 2.0 * np.pi / order

            assert np.isclose(twist * ring_width, 0.5 * lobe_spacing)


def test_v008_twist_preserves_brightness_at_every_radius() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    for r in (0.10, 0.25, 0.40, 0.75):
        phi = v008.coupled_angle(theta, np.full_like(theta, r))
        assert np.isclose(v008.ring_weight(phi).mean(), 1.0, atol=1.0e-9)


def test_v008_reduces_to_v007_without_twist() -> None:
    x, y = v008.coordinate_grids(width=200, height=200)

    assert np.allclose(v008.v008_field(x, y, twist=0.0), v007.v007_field(x, y))


def test_v008_bends_the_lobes_off_the_radial_direction() -> None:
    x, y = v008.coordinate_grids(width=700, height=700)
    r1, _ = v008.radial_fields(x, y)
    theta1, _ = v008.angular_fields(x, y)

    straight = v008.v008_field(x, y, twist=0.0)
    bent = v008.v008_field(x, y)

    inner = np.abs(r1 - 0.20) < 0.01
    outer = np.abs(r1 - 0.32) < 0.01
    assert inner.any() and outer.any()

    def brightest_angle(field: np.ndarray, shell: np.ndarray) -> float:
        return float(theta1[shell][field[shell].argmax()])

    straight_shift = abs(brightest_angle(straight, outer) - brightest_angle(straight, inner))
    bent_shift = abs(brightest_angle(bent, outer) - brightest_angle(bent, inner))

    assert straight_shift < 0.05
    assert bent_shift > 0.4


def test_v008_keeps_the_silhouettes_solid() -> None:
    x, y = v008.coordinate_grids(width=400, height=400)
    r1, r2 = v008.radial_fields(x, y)
    field = v008.v008_field(x, y)

    margin = 6.0 * v008.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v008_rejects_invalid_twist_parameters() -> None:
    import pytest

    for bad_order in (0, -2):
        with pytest.raises(ValueError):
            v008.natural_twist(order=bad_order)
    with pytest.raises(ValueError):
        v008.natural_twist(sharpness=0.0)


def _local_pitch(phase, radius: float, step: float = 1.0e-6) -> float:
    theta = np.array([0.0])
    r = np.array([radius])

    d_theta = (phase(theta + step, r) - phase(theta - step, r)) / (2.0 * step)
    d_r = (phase(theta, r + step) - phase(theta, r - step)) / (2.0 * step)

    return float(np.degrees(np.arctan(np.abs(d_theta / d_r) / radius)[0]))


def test_v009_expression_is_finite() -> None:
    x, y = v009.coordinate_grids(width=81, height=65)
    field = v009.v009_field(x, y)
    rgb = v009.v009_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v009_keeps_the_half_turn_symmetry() -> None:
    x, y = v009.coordinate_grids(width=201, height=201)
    field = v009.v009_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v009_pitch_angle_is_the_same_at_every_radius() -> None:
    for pitch_degrees in (15.0, 29.66, 45.0):
        pitch = np.radians(pitch_degrees)
        phase = lambda t, r: v009.spiral_phase(t, r, pitch=pitch, softening=0.0)

        measured = [_local_pitch(phase, radius) for radius in (0.15, 0.25, 0.40, 0.70)]

        assert np.allclose(measured, pitch_degrees, atol=1.0e-3)


def test_v009_pitch_is_constant_where_v008_twist_is_not() -> None:
    radii = (0.15, 0.25, 0.40, 0.55)

    linear = [_local_pitch(lambda t, r: v008.coupled_angle(t, r), radius) for radius in radii]
    logarithmic = [
        _local_pitch(lambda t, r: v009.spiral_phase(t, r, softening=0.0), radius)
        for radius in radii
    ]

    assert max(linear) - min(linear) > 20.0
    assert max(logarithmic) - min(logarithmic) < 1.0e-3


def test_v009_phase_traces_a_logarithmic_spiral() -> None:
    pitch = np.radians(29.66)
    winding = 1.0 / np.tan(pitch)

    theta = np.linspace(0.0, 4.0 * np.pi, 512)
    r = 0.25 * np.exp(np.tan(pitch) * theta)

    phase = v009.spiral_phase(theta, r, pitch=pitch, softening=0.0)

    assert np.allclose(phase, phase[0])
    assert np.isclose(winding, 1.0 / np.tan(pitch))


def test_v009_natural_pitch_winds_half_a_lobe_per_ring_width() -> None:
    for order in (2, 4, 6):
        for sharpness in (40.0, 80.0):
            pitch = v009.natural_pitch(order=order, sharpness=sharpness, ring_radius=0.25)

            log_span = (1.0 / np.sqrt(sharpness)) / 0.25
            winding = log_span / np.tan(pitch)

            assert np.isclose(winding, np.pi / order)


def test_v009_reduces_to_v007_at_a_right_angle_pitch() -> None:
    x, y = v009.coordinate_grids(width=200, height=200)

    assert np.allclose(v009.v009_field(x, y, pitch=0.5 * np.pi), v007.v007_field(x, y))


def test_v009_softening_keeps_the_phase_finite_at_the_origin() -> None:
    theta = np.zeros(1)

    assert np.isfinite(v009.spiral_phase(theta, np.zeros(1))).all()

    with np.errstate(divide="ignore"):
        unguarded = v009.spiral_phase(theta, np.zeros(1), softening=0.0)
    assert not np.isfinite(unguarded).all()


def test_v009_twist_preserves_brightness_at_every_radius() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    for r in (0.10, 0.25, 0.40, 0.75):
        phi = v009.spiral_phase(theta, np.full_like(theta, r))
        assert np.isclose(v009.ring_weight(phi).mean(), 1.0, atol=1.0e-9)


def test_v009_keeps_the_silhouettes_solid() -> None:
    x, y = v009.coordinate_grids(width=400, height=400)
    r1, r2 = v009.radial_fields(x, y)
    field = v009.v009_field(x, y)

    margin = 6.0 * v009.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v009_rejects_invalid_spiral_parameters() -> None:
    import pytest

    theta = np.zeros(4)
    r = np.full(4, 0.3)

    for bad_pitch in (0.0, -0.2, 2.0):
        with pytest.raises(ValueError):
            v009.spiral_phase(theta, r, pitch=bad_pitch)
    with pytest.raises(ValueError):
        v009.spiral_phase(theta, r, softening=-0.1)
    with pytest.raises(ValueError):
        v009.natural_pitch(order=0)


def test_v010_expression_is_finite() -> None:
    x, y = v010.coordinate_grids(width=81, height=65)
    field = v010.v010_field(x, y)
    rgb = v010.v010_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v010_keeps_the_half_turn_symmetry() -> None:
    x, y = v010.coordinate_grids(width=201, height=201)
    field = v010.v010_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v010_decay_is_a_falling_exponential() -> None:
    r = np.linspace(0.0, 2.0, 512)

    assert np.allclose(v010.radial_decay(r, 0.0), 1.0)
    assert np.allclose(v010.radial_decay(r, 2.0), np.exp(-2.0 * r))

    for decay in (0.5, 2.0, 5.0):
        weight = v010.radial_decay(r, decay)
        assert np.all(np.diff(weight) < 0.0)
        assert np.isclose(weight[0], 1.0)
        assert weight[-1] < weight[0]


def test_v010_stronger_decay_suppresses_the_arms_monotonically() -> None:
    x, y = v010.coordinate_grids(width=400, height=400)
    r1, r2 = v010.radial_fields(x, y)
    theta1, theta2 = v010.angular_fields(x, y)

    previous = None
    for decay in (0.0, 1.0, 2.0, 5.0):
        arms = v010.ring_field(r1, r2, theta1, theta2, decay=decay)
        if previous is not None:
            assert np.all(arms <= previous + 1.0e-12)
        previous = arms


def test_v010_decay_pulls_the_arm_peak_inward() -> None:
    r = np.linspace(0.14, 0.9, 4000)
    envelope = np.exp(-80.0 * (r - 0.25) ** 2)

    peaks = [float(r[(envelope * v010.radial_decay(r, decay)).argmax()]) for decay in (0.0, 2.0, 5.0)]

    assert np.isclose(peaks[0], 0.25, atol=1.0e-3)
    assert peaks[2] < peaks[1] < peaks[0]
    for decay, peak in zip((2.0, 5.0), peaks[1:]):
        assert np.isclose(peak, 0.25 - decay / 160.0, atol=2.0e-3)


def test_v010_decay_leaves_the_halo_alone() -> None:
    x, y = v010.coordinate_grids(width=300, height=300)
    r1, r2 = v010.radial_fields(x, y)

    plain = v010.halo_field(r1, r2)
    assert np.allclose(v009.halo_field(r1, r2), plain)


def test_v010_reduces_to_v009_without_decay() -> None:
    x, y = v010.coordinate_grids(width=200, height=200)

    assert np.allclose(v010.v010_field(x, y, decay=0.0), v009.v009_field(x, y))
    assert np.array_equal(v010.v010_rgb(120, 120, decay=0.0), v009.v009_rgb(120, 120))


def test_v010_keeps_the_silhouettes_solid() -> None:
    x, y = v010.coordinate_grids(width=400, height=400)
    r1, r2 = v010.radial_fields(x, y)
    field = v010.v010_field(x, y)

    margin = 6.0 * v010.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v010_rejects_negative_decay() -> None:
    import pytest

    with pytest.raises(ValueError):
        v010.radial_decay(np.linspace(0.1, 1.0, 8), -0.5)


def test_v011_expression_is_finite() -> None:
    x, y = v011.coordinate_grids(width=81, height=65)
    field = v011.v011_field(x, y)
    rgb = v011.v011_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v011_matches_the_plain_angle_specification() -> None:
    x, y = v011.coordinate_grids(width=101, height=101)
    a = 0.36

    for phase in (0.0, 0.7, np.pi, 4.9):
        tilde1, tilde2 = v011.phased_angles(*v011.angular_fields(x, y, a=a), phase)

        plain1 = np.arctan2(y, x + a)
        plain2 = np.arctan2(y, x - a)

        assert np.allclose(np.cos(tilde1), np.cos(plain1 - phase))
        assert np.allclose(np.sin(tilde1), np.sin(plain1 - phase))
        assert np.allclose(np.cos(tilde2), np.cos(plain2 - phase - np.pi))
        assert np.allclose(np.sin(tilde2), np.sin(plain2 - phase - np.pi))


def test_v011_both_frames_follow_one_parameter() -> None:
    x, y = v011.coordinate_grids(width=201, height=201)

    r1, r2 = v011.radial_fields(x, y)
    defined = (r1 > 1.0e-12) & (r2 > 1.0e-12)

    for phase in (0.0, 1.1, np.pi, 5.5):
        tilde1, tilde2 = v011.phased_angles(*v011.angular_fields(x, y), phase)
        partner = np.rot90(tilde2, 2)

        assert np.allclose(np.cos(tilde1)[defined], np.cos(partner)[defined])
        assert np.allclose(np.sin(tilde1)[defined], np.sin(partner)[defined])


def test_v011_keeps_the_half_turn_symmetry_at_every_phase() -> None:
    x, y = v011.coordinate_grids(width=201, height=201)

    for degrees in (0, 37, 90, 180, 263):
        field = v011.v011_field(x, y, phase=np.radians(degrees))
        assert np.allclose(field, np.rot90(field, 2))
        assert not np.allclose(field, np.fliplr(field))


def test_v011_is_periodic_in_the_phase() -> None:
    x, y = v011.coordinate_grids(width=150, height=150)

    base = v011.v011_field(x, y, phase=0.9)
    assert np.allclose(v011.v011_field(x, y, phase=0.9 + 2.0 * np.pi), base)
    assert np.allclose(v011.v011_field(x, y, phase=0.9 - 2.0 * np.pi), base)


def test_v011_phase_conserves_total_brightness() -> None:
    x, y = v011.coordinate_grids(width=300, height=300)

    means = [v011.v011_field(x, y, phase=np.radians(d)).mean() for d in range(0, 360, 20)]

    assert np.allclose(means, means[0], rtol=1.0e-6)


def test_v011_reduces_to_v010_at_zero_phase() -> None:
    x, y = v011.coordinate_grids(width=200, height=200)

    assert np.allclose(v011.v011_field(x, y, phase=0.0), v010.v010_field(x, y))
    assert np.array_equal(v011.v011_rgb(120, 120), v010.v010_rgb(120, 120))


def test_v011_phase_series_tiles_four_renders() -> None:
    gap = 4
    series = v011.phase_series(40, 30, gap=gap)

    assert series.shape == (2 * 30 + gap, 2 * 40 + gap, 3)
    assert series.dtype == np.uint8

    assert np.array_equal(series[:30, :40], v011.v011_rgb(40, 30, phase=0.0))
    assert np.array_equal(series[:30, 40 + gap :], v011.v011_rgb(40, 30, phase=0.5 * np.pi))
    assert np.array_equal(series[30 + gap :, :40], v011.v011_rgb(40, 30, phase=np.pi))


def test_v011_keeps_the_silhouettes_solid() -> None:
    x, y = v011.coordinate_grids(width=400, height=400)
    r1, r2 = v011.radial_fields(x, y)

    margin = 6.0 * v011.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    for degrees in (0, 90, 215):
        field = v011.v011_field(x, y, phase=np.radians(degrees))
        assert field[inside].max() < 1.0e-2


def test_v011_phase_series_requires_four_phases() -> None:
    import pytest

    with pytest.raises(ValueError):
        v011.phase_series(20, 20, phases=(0.0, np.pi))


def test_v011_angle_singularity_sits_inside_the_horizon() -> None:
    x, y = v011.coordinate_grids(width=201, height=201)
    r1, r2 = v011.radial_fields(x, y)

    singular = (r1 < 1.0e-12) | (r2 < 1.0e-12)
    assert singular.sum() == 2

    assert np.all(np.minimum(r1, r2)[singular] < 0.14)

    field = v011.v011_field(x, y, phase=1.1)
    assert np.all(field[singular] < 1.0e-6)
    assert np.allclose(field, np.rot90(field, 2))


def test_v012_expression_is_finite() -> None:
    x, y = v012.coordinate_grids(width=81, height=65)
    field = v012.v012_field(x, y)
    rgb = v012.v012_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v012_matches_the_plain_angle_specification() -> None:
    x, y = v012.coordinate_grids(width=101, height=101)
    a = 0.36

    r1, r2 = v012.radial_fields(x, y, a=a)
    theta1, theta2 = v012.angular_fields(x, y, a=a)

    plain1 = np.arctan2(y, x + a)
    plain2 = np.arctan2(y, x - a)

    for epsilon in (-0.3, 0.0, 0.25):
        d1, d2 = v012.distorted_radii(r1, r2, theta1, theta2, epsilon)

        assert np.allclose(d1, r1 * (1.0 + epsilon * np.cos(plain1)))
        assert np.allclose(d2, r2 * (1.0 - epsilon * np.cos(plain2)))


def test_v012_keeps_the_half_turn_symmetry() -> None:
    x, y = v012.coordinate_grids(width=201, height=201)

    for epsilon in (-0.3, 0.0, 0.25):
        field = v012.v012_field(x, y, distortion=epsilon)
        assert np.allclose(field, np.rot90(field, 2))
        if epsilon != 0.0:
            assert not np.allclose(field, np.fliplr(field))


def test_v012_moves_the_ring_by_the_predicted_factor() -> None:
    theta = np.array([0.0, np.pi])

    for epsilon in (-0.3, -0.1, 0.25):
        d = v012.companion_distortion(theta, epsilon)

        assert np.isclose(0.25 / d[0], 0.25 / (1.0 + epsilon))
        assert np.isclose(0.25 / d[1], 0.25 / (1.0 - epsilon))

        toward, away = 0.25 / d[0], 0.25 / d[1]
        if epsilon < 0.0:
            assert toward > away
        else:
            assert toward < away


def test_v012_leaves_the_horizons_circular() -> None:
    x, y = v012.coordinate_grids(width=600, height=600)
    spacing = v012.grid_spacing(x, y)
    center1, _ = v012.black_hole_centers()
    means: list[float] = []

    for epsilon in (-0.3, 0.0, 0.25):
        field = v012.v012_field(x, y, distortion=epsilon)

        edges = []
        for angle in np.linspace(-np.pi, np.pi, 16, endpoint=False):
            radii = np.linspace(0.02, 0.30, 800)
            px = center1[0] + radii * np.cos(angle)
            py = center1[1] + radii * np.sin(angle)

            col = np.clip(np.round((px + 1.0) / spacing).astype(int), 0, 599)
            row = np.clip(np.round((1.0 - py) / spacing).astype(int), 0, 599)

            lit = np.flatnonzero(field[row, col] > 1.0e-3)
            edges.append(radii[lit[0]])

        edges = np.array(edges)
        assert np.ptp(edges) < 3.0 * spacing
        means.append(float(edges.mean()))

    assert max(means) - min(means) < spacing


def test_v012_leaves_the_halo_undistorted() -> None:
    x, y = v012.coordinate_grids(width=300, height=300)
    r1, r2 = v012.radial_fields(x, y)

    assert np.allclose(v012.halo_field(r1, r2), v011.halo_field(r1, r2))


def test_v012_reduces_to_v011_without_distortion() -> None:
    x, y = v012.coordinate_grids(width=200, height=200)

    assert np.allclose(v012.v012_field(x, y, distortion=0.0), v011.v011_field(x, y))
    assert np.array_equal(v012.v012_rgb(120, 120, distortion=0.0), v011.v011_rgb(120, 120))


def test_v012_keeps_the_silhouettes_solid() -> None:
    x, y = v012.coordinate_grids(width=400, height=400)
    r1, r2 = v012.radial_fields(x, y)

    margin = 6.0 * v012.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    for epsilon in (-0.3, 0.0, 0.25):
        field = v012.v012_field(x, y, distortion=epsilon)
        assert field[inside].max() < 1.0e-2


def test_v012_rejects_a_degenerate_distortion() -> None:
    import pytest

    theta = np.linspace(-np.pi, np.pi, 16)
    for bad in (1.0, -1.0, 1.4):
        with pytest.raises(ValueError):
            v012.companion_distortion(theta, bad)


def test_v013_expression_is_finite() -> None:
    x, y = v013.coordinate_grids(width=81, height=65)
    field = v013.v013_field(x, y)
    rgb = v013.v013_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v013_matches_the_specified_product() -> None:
    x, y = v013.coordinate_grids(width=121, height=121)
    r1, r2 = v013.radial_fields(x, y)

    for alpha_i, beta_i in ((25.0, 3.0), (10.0, 1.5), (60.0, 5.0)):
        expected = np.exp(-alpha_i * (r1 - r2) ** 2) * np.exp(-beta_i * (r1 + r2))
        actual = v013.interaction_field(r1, r2, alpha_i=alpha_i, beta_i=beta_i, strength=1.0)

        assert np.allclose(actual, expected * np.exp(beta_i * 2.0 * 0.36))


def test_v013_peaks_at_the_midpoint_with_the_given_strength() -> None:
    x, y = v013.coordinate_grids(width=601, height=601)
    r1, r2 = v013.radial_fields(x, y)

    for strength in (0.2, 0.35, 1.0):
        interaction = v013.interaction_field(r1, r2, strength=strength)

        assert interaction.max() <= strength + 1.0e-12
        assert np.isclose(interaction.max(), strength, rtol=1.0e-3)

        row, col = np.unravel_index(interaction.argmax(), interaction.shape)
        assert abs(float(x[row, col])) < 0.01
        assert abs(float(y[row, col])) < 0.01


def test_v013_balance_term_selects_the_perpendicular_bisector() -> None:
    x, y = v013.coordinate_grids(width=401, height=401)
    r1, r2 = v013.radial_fields(x, y)

    balance = np.exp(-25.0 * (r1 - r2) ** 2)
    on_bisector = np.abs(x) < 1.0e-9

    assert on_bisector.any()
    assert np.allclose(balance[on_bisector], 1.0)

    row = int(np.argmin(np.abs(y[:, 0])))
    along_axis = balance[row]
    assert np.isclose(along_axis.max(), 1.0)
    assert np.isclose(float(x[row][along_axis.argmax()]), 0.0, atol=1.0e-9)
    assert along_axis[np.abs(x[row]) > 0.2].max() < 0.05

    # the level sets of r1 - r2 are hyperbolae asymptotic to lines through the
    # origin, so the selected region is a widening wedge rather than a strip
    far_out = (np.abs(x - 0.3) < 0.01) & (np.abs(y - 1.0) < 0.01)
    assert far_out.any()
    assert balance[far_out].max() > 0.3


def test_v013_confinement_is_what_bounds_the_bisector() -> None:
    x, y = v013.coordinate_grids(width=601, height=601)
    r1, r2 = v013.radial_fields(x, y)

    col = int(np.argmin(np.abs(x[0])))
    balance = np.exp(-25.0 * (r1 - r2) ** 2)[:, col]
    full = v013.interaction_field(r1, r2)[:, col]

    far = np.abs(y[:, col]) > 0.8

    assert balance[far].min() > 0.99
    assert full[far].max() < 0.05 * full.max()

    profile = full[y[:, col] >= 0.0]
    assert np.all(np.diff(profile[np.argmax(profile) :]) <= 1.0e-12)


def test_v013_interaction_is_symmetric_in_the_two_holes() -> None:
    x, y = v013.coordinate_grids(width=201, height=201)
    r1, r2 = v013.radial_fields(x, y)

    interaction = v013.interaction_field(r1, r2)

    assert np.allclose(interaction, v013.interaction_field(r2, r1))
    assert np.allclose(interaction, np.fliplr(interaction))
    assert np.allclose(interaction, np.rot90(interaction, 2))


def test_v013_keeps_the_half_turn_symmetry() -> None:
    x, y = v013.coordinate_grids(width=201, height=201)
    field = v013.v013_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v013_reduces_to_v012_without_strength() -> None:
    x, y = v013.coordinate_grids(width=200, height=200)

    assert np.allclose(v013.v013_field(x, y, strength=0.0), v012.v012_field(x, y))
    assert np.array_equal(v013.v013_rgb(120, 120, strength=0.0), v012.v012_rgb(120, 120))


def test_v013_keeps_the_silhouettes_solid() -> None:
    x, y = v013.coordinate_grids(width=400, height=400)
    r1, r2 = v013.radial_fields(x, y)
    field = v013.v013_field(x, y)

    margin = 6.0 * v013.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v013_rejects_negative_interaction_parameters() -> None:
    import pytest

    r = np.full(4, 0.5)
    for kwargs in ({"alpha_i": -1.0}, {"beta_i": -1.0}, {"strength": -0.1}):
        with pytest.raises(ValueError):
            v013.interaction_field(r, r, **kwargs)


def test_v014_expression_is_finite() -> None:
    x, y = v014.coordinate_grids(width=81, height=65)
    field = v014.v014_field(x, y)
    rgb = v014.v014_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v014_matches_the_specified_product() -> None:
    x, y = v014.coordinate_grids(width=121, height=121)
    r1, r2 = v014.radial_fields(x, y)

    for alpha_t, beta_t, eta_t, k_t in ((120.0, 25.0, 0.5, 32.0), (40.0, 10.0, 0.0, 8.0)):
        interaction = v014.interaction_field(r1, r2, alpha_i=1.5, beta_i=3.0, strength=1.0)
        expected = (
            np.exp(-alpha_t * y**2)
            * np.exp(-beta_t * x**4)
            * interaction
            * (1.0 + eta_t * np.cos(k_t * x))
        )
        actual = v014.tidal_bridge(
            x, y, r1, r2, alpha_i=1.5, beta_i=3.0, strength=1.0,
            alpha_t=alpha_t, beta_t=beta_t, eta_t=eta_t, k_t=k_t,
        )
        assert np.allclose(actual, expected)


def test_v014_bridge_is_wider_than_it_is_tall() -> None:
    x, y = v014.coordinate_grids(width=800, height=800)
    r1, r2 = v014.radial_fields(x, y)

    bridge = v014.tidal_bridge(x, y, r1, r2, eta_t=0.0)

    row = int(np.argmin(np.abs(y[:, 0])))
    col = int(np.argmin(np.abs(x[0])))

    across = x[row][bridge[row] > 0.5 * bridge[row].max()]
    up = y[:, col][bridge[:, col] > 0.5 * bridge[:, col].max()]

    assert across.max() > 2.5 * up.max()
    assert across.max() > 0.5 * 0.36


def test_v014_super_gaussian_is_flatter_than_a_gaussian() -> None:
    # compared at matched half-width, not matched coefficient: with the same
    # coefficient the quartic only overtakes the gaussian beyond x = 1
    half_width = (np.log(2.0) / 25.0) ** 0.25
    x = np.linspace(0.0, 2.0 * half_width, 4000)

    quartic = np.exp(-25.0 * x**4)
    gaussian = np.exp(-np.log(2.0) / half_width**2 * x**2)

    assert np.isclose(quartic[np.argmin(np.abs(x - half_width))], 0.5, atol=1.0e-3)
    assert np.isclose(gaussian[np.argmin(np.abs(x - half_width))], 0.5, atol=1.0e-3)

    inside = (x > 0.0) & (x < 0.95 * half_width)
    outside = x > 1.05 * half_width

    assert np.all(quartic[inside] > gaussian[inside])
    assert np.all(quartic[outside] < gaussian[outside])


def test_v014_internal_structure_makes_knots_along_the_bridge() -> None:
    x, y = v014.coordinate_grids(width=800, height=800)
    r1, r2 = v014.radial_fields(x, y)
    row = int(np.argmin(np.abs(y[:, 0])))

    def knots(eta_t: float) -> int:
        profile = v014.tidal_bridge(x, y, r1, r2, eta_t=eta_t)[row]
        interior = profile[1:-1]
        dips = (interior < profile[:-2]) & (interior < profile[2:])
        return int(dips[np.abs(x[row][1:-1]) < 0.4].sum())

    assert knots(0.0) == 0
    assert knots(0.5) >= 4


def test_v014_bridge_phase_slides_the_knots() -> None:
    x, y = v014.coordinate_grids(width=600, height=600)
    r1, r2 = v014.radial_fields(x, y)

    base = v014.tidal_bridge(x, y, r1, r2)
    shifted = v014.tidal_bridge(x, y, r1, r2, bridge_phase=np.pi)

    assert not np.allclose(base, shifted)
    assert np.allclose(base, v014.tidal_bridge(x, y, r1, r2, bridge_phase=2.0 * np.pi))


def test_v014_keeps_the_half_turn_symmetry() -> None:
    x, y = v014.coordinate_grids(width=201, height=201)
    field = v014.v014_field(x, y)

    assert np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v014_bridge_alone_is_mirror_symmetric() -> None:
    x, y = v014.coordinate_grids(width=201, height=201)
    r1, r2 = v014.radial_fields(x, y)

    bridge = v014.tidal_bridge(x, y, r1, r2)

    assert np.allclose(bridge, np.fliplr(bridge))
    assert np.allclose(bridge, np.flipud(bridge))


def test_v014_reduces_to_v013_geometry_without_strength() -> None:
    x, y = v014.coordinate_grids(width=200, height=200)

    assert np.allclose(
        v014.v014_field(x, y, strength=0.0),
        v013.v013_field(x, y, strength=0.0),
    )


def test_v014_keeps_the_silhouettes_solid() -> None:
    x, y = v014.coordinate_grids(width=400, height=400)
    r1, r2 = v014.radial_fields(x, y)
    field = v014.v014_field(x, y)

    margin = 6.0 * v014.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v014_rejects_invalid_bridge_parameters() -> None:
    import pytest

    x, y = v014.coordinate_grids(width=16, height=16)
    r1, r2 = v014.radial_fields(x, y)

    for kwargs in ({"alpha_t": -1.0}, {"beta_t": -1.0}, {"eta_t": 1.5}, {"eta_t": -1.5}):
        with pytest.raises(ValueError):
            v014.tidal_bridge(x, y, r1, r2, **kwargs)


def test_v015_expression_is_finite() -> None:
    x, y = v015.coordinate_grids(width=81, height=65)
    field = v015.v015_field(x, y)
    rgb = v015.v015_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v015_matches_the_specified_sum() -> None:
    x, y = v015.coordinate_grids(width=121, height=121)
    r1, r2 = v015.radial_fields(x, y)
    theta1, theta2 = v015.plain_angles(x, y)

    for alpha_q, radius_q, c_q, beta_q in ((150.0, 0.45, 0.25, 1.5), (60.0, 0.6, -0.4, 0.8)):
        q1 = np.exp(-alpha_q * (r1 - radius_q - c_q * theta1) ** 2) * np.exp(-beta_q * r1)
        q2 = np.exp(-alpha_q * (r2 - radius_q + c_q * theta2) ** 2) * np.exp(-beta_q * r2)

        actual = v015.tidal_tails(
            r1, r2, theta1, theta2,
            alpha_q=alpha_q, radius_q=radius_q, c_q=c_q, beta_q=beta_q,
            tails=1.0, taper=0.0,
        )
        assert np.allclose(actual, q1 + q2)


def test_v015_plain_angles_differ_from_the_anchored_ones_by_half_a_turn() -> None:
    x, y = v015.coordinate_grids(width=101, height=101)

    plain1, plain2 = v015.plain_angles(x, y)
    anchored1, anchored2 = v015.angular_fields(x, y)

    assert np.allclose(plain1, anchored1)
    assert np.allclose(np.cos(plain2), np.cos(anchored2 + np.pi))
    assert np.allclose(np.sin(plain2), np.sin(anchored2 + np.pi))


def test_v015_ridge_follows_an_archimedean_spiral() -> None:
    theta = np.linspace(-1.5, 3.0, 400)
    radius_q, c_q = 0.45, 0.25

    on_ridge = radius_q + c_q * theta
    argument = on_ridge - radius_q - c_q * theta

    assert np.allclose(argument, 0.0)
    assert np.allclose(np.diff(on_ridge) / np.diff(theta), c_q)


def test_v015_taper_removes_the_branch_cut_discontinuity() -> None:
    x, y = v015.coordinate_grids(width=1000, height=1000)
    r1, r2 = v015.radial_fields(x, y)
    theta1, theta2 = v015.plain_angles(x, y)

    col = int(np.argmin(np.abs(x[0] + 0.8)))
    row = int(np.argmin(np.abs(y[:, col])))

    def seam(taper: float) -> float:
        q = v015.tidal_tails(r1, r2, theta1, theta2, taper=taper)
        return abs(float(q[row - 1, col] - q[row + 1, col]))

    assert seam(0.0) > 0.03
    assert seam(0.5) < 1.0e-6


def test_v015_taper_vanishes_on_the_cut_and_is_inert_away_from_it() -> None:
    theta = np.linspace(-np.pi, np.pi, 2001)
    taper = v015.tail_taper(theta, 0.5)

    assert np.isclose(taper[0], 0.0, atol=1.0e-12)
    assert np.isclose(taper[-1], 0.0, atol=1.0e-12)
    assert taper[np.abs(theta) < np.pi - 1.5].min() > 0.99
    assert np.allclose(v015.tail_taper(theta, 0.0), 1.0)


def test_v015_tails_break_the_half_turn_symmetry() -> None:
    x, y = v015.coordinate_grids(width=301, height=301)
    r1, r2 = v015.radial_fields(x, y)
    theta1, theta2 = v015.plain_angles(x, y)

    tails = v015.tidal_tails(r1, r2, theta1, theta2)
    residual = np.abs(tails - np.rot90(tails, 2)).max()

    assert residual > 0.5 * tails.max()

    field = v015.v015_field(x, y)
    assert not np.allclose(field, np.rot90(field, 2))
    assert not np.allclose(field, np.fliplr(field))


def test_v015_anchored_angles_with_one_sign_would_restore_it() -> None:
    x, y = v015.coordinate_grids(width=301, height=301)
    r1, r2 = v015.radial_fields(x, y)
    anchored1, anchored2 = v015.angular_fields(x, y)

    def arm(r: np.ndarray, theta: np.ndarray) -> np.ndarray:
        ridge = np.exp(-150.0 * (r - 0.45 - 0.25 * theta) ** 2)
        return ridge * np.exp(-1.5 * r) * v015.tail_taper(theta, 0.5)

    symmetric = arm(r1, anchored1) + arm(r2, anchored2)

    assert np.allclose(symmetric, np.rot90(symmetric, 2), atol=1.0e-12)


def test_v015_reduces_to_v014_without_tails() -> None:
    x, y = v015.coordinate_grids(width=200, height=200)

    assert np.allclose(v015.v015_field(x, y, tails=0.0), v014.v014_field(x, y))
    assert np.array_equal(v015.v015_rgb(120, 120, tails=0.0), v014.v014_rgb(120, 120))


def test_v015_keeps_the_silhouettes_solid() -> None:
    x, y = v015.coordinate_grids(width=400, height=400)
    r1, r2 = v015.radial_fields(x, y)
    field = v015.v015_field(x, y)

    margin = 6.0 * v015.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v015_rejects_invalid_tail_parameters() -> None:
    import pytest

    r = np.full(4, 0.5)
    t = np.zeros(4)

    for kwargs in ({"alpha_q": -1.0}, {"beta_q": -1.0}, {"tails": -0.1}):
        with pytest.raises(ValueError):
            v015.tidal_tails(r, r, t, t, **kwargs)
    with pytest.raises(ValueError):
        v015.tail_taper(t, -0.5)


def test_v016_expression_is_finite() -> None:
    x, y = v016.coordinate_grids(width=81, height=65)
    field = v016.v016_field(x, y)
    rgb = v016.v016_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v016_matches_the_specified_potential() -> None:
    x, y = v016.coordinate_grids(width=121, height=121)
    r1, r2 = v016.radial_fields(x, y)

    for epsilon in (0.05, 0.2):
        expected = -(1.0 / (r1 + epsilon) + 1.0 / (r2 + epsilon))
        assert np.allclose(v016.binary_potential(r1, r2, epsilon=epsilon), expected)

        for kappa in (0.15, 0.6):
            assert np.allclose(
                v016.potential_weight(r1, r2, kappa=kappa, epsilon=epsilon),
                1.0 - np.exp(-kappa * np.abs(expected)),
            )


def test_v016_potential_is_negative_and_finite_at_the_centres() -> None:
    x, y = v016.coordinate_grids(width=201, height=201)
    r1, r2 = v016.radial_fields(x, y)

    potential = v016.binary_potential(r1, r2)

    assert np.all(potential < 0.0)
    assert np.isfinite(potential).all()

    deepest = float(np.abs(potential).max())
    assert deepest < 1.0 / 0.05 + 1.0 / 0.05


def test_v016_weight_is_bounded_and_deepest_at_the_holes() -> None:
    x, y = v016.coordinate_grids(width=401, height=401)
    r1, r2 = v016.radial_fields(x, y)

    weight = v016.potential_weight(r1, r2)

    assert weight.min() > 0.0
    assert weight.max() < 1.0

    near = np.minimum(r1, r2) < 0.2
    far = np.minimum(r1, r2) > 1.0
    assert weight[near].min() > weight[far].max()


def test_v016_weight_never_reaches_zero_inside_the_frame() -> None:
    x, y = v016.coordinate_grids(width=401, height=401)
    r1, r2 = v016.radial_fields(x, y)

    for kappa in (0.15, 0.3, 0.6):
        weight = v016.potential_weight(r1, r2, kappa=kappa)
        corner = (np.abs(x) > 0.9) & (np.abs(y) > 0.9)

        assert weight[corner].min() > 0.1
        assert weight.max() / weight[corner].mean() < 6.0


def test_v016_adds_a_pedestal_rather_than_scaling() -> None:
    x, y = v016.coordinate_grids(width=300, height=300)

    base = v015.v015_field(x, y)
    lifted = v016.v016_field(x, y)

    assert np.all(lifted >= base - 1.0e-12)

    # the pedestal lifts the dim background, but not the horizons: every pixel
    # the silhouette zeroes stays zeroed, because P is added inside the mask
    r1, r2 = v016.radial_fields(x, y)
    inside = np.minimum(r1, r2) < 0.10
    assert inside.any()
    assert lifted[inside].max() < 1.0e-2

    corner = (np.abs(x) > 0.9) & (np.abs(y) > 0.9)
    assert corner.any()
    assert lifted[corner].mean() > 2.0 * base[corner].mean()


def test_v016_smaller_kappa_gives_more_contrast() -> None:
    x, y = v016.coordinate_grids(width=301, height=301)
    r1, r2 = v016.radial_fields(x, y)
    corner = (np.abs(x) > 0.9) & (np.abs(y) > 0.9)

    ratios = []
    for kappa in (0.15, 0.3, 0.6):
        weight = v016.potential_weight(r1, r2, kappa=kappa)
        ratios.append(float(weight.max() / weight[corner].mean()))

    assert ratios[0] > ratios[1] > ratios[2]


def test_v016_reduces_to_v015_without_the_potential() -> None:
    x, y = v016.coordinate_grids(width=200, height=200)

    assert np.allclose(v016.v016_field(x, y, lambda_p=0.0), v015.v015_field(x, y))
    assert np.array_equal(v016.v016_rgb(120, 120, lambda_p=0.0), v015.v015_rgb(120, 120))


def test_v016_keeps_the_silhouettes_solid() -> None:
    x, y = v016.coordinate_grids(width=400, height=400)
    r1, r2 = v016.radial_fields(x, y)
    field = v016.v016_field(x, y)

    margin = 6.0 * v016.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v016_rejects_invalid_potential_parameters() -> None:
    import pytest

    r = np.full(4, 0.5)
    with pytest.raises(ValueError):
        v016.binary_potential(r, r, epsilon=0.0)
    with pytest.raises(ValueError):
        v016.potential_weight(r, r, kappa=-0.1)


def test_v017_expression_is_finite() -> None:
    x, y = v017.coordinate_grids(width=81, height=65)
    field = v017.v017_field(x, y)
    rgb = v017.v017_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v017_global_polar_is_centred_on_the_binary() -> None:
    x, y = v017.coordinate_grids(width=201, height=201)
    rho, theta = v017.global_polar(x, y)

    assert np.allclose(rho, np.sqrt(x**2 + y**2))
    assert np.allclose(theta, np.arctan2(y, x))

    assert rho.min() < 0.01
    assert np.isclose(rho.max(), np.sqrt(2.0), rtol=1.0e-3)

    centre = np.unravel_index(rho.argmin(), rho.shape)
    assert abs(float(x[centre])) < 0.01 and abs(float(y[centre])) < 0.01


def test_v017_phase_matches_the_specification() -> None:
    rho = np.linspace(0.0, 1.5, 256)

    for k_g, omega_g, phase in ((28.0, 2.0, 0.0), (10.0, 1.0, 0.7), (40.0, 3.0, 2.5)):
        assert np.allclose(
            v017.wave_phase(rho, phase=phase, k_g=k_g, omega_g=omega_g),
            k_g * rho - omega_g * phase,
        )
        assert np.allclose(
            v017.outgoing_wave(rho, phase=phase, k_g=k_g, omega_g=omega_g),
            np.cos(k_g * rho - omega_g * phase),
        )


def test_v017_wave_is_bounded_and_periodic_in_radius() -> None:
    rho = np.linspace(0.0, 2.0, 100000)
    wave = v017.outgoing_wave(rho)

    assert wave.min() >= -1.0 and wave.max() <= 1.0
    assert np.isclose(wave.min(), -1.0, atol=1.0e-4)
    assert np.isclose(wave.max(), 1.0, atol=1.0e-4)

    wavelength = 2.0 * np.pi / 28.0
    shifted = v017.outgoing_wave(rho + wavelength)
    assert np.allclose(wave, shifted, atol=1.0e-9)


def test_v017_crests_travel_outward_with_the_orbital_phase() -> None:
    rho = np.linspace(0.30, 0.55, 400000)

    def first_crest(phase: float) -> float:
        wave = v017.outgoing_wave(rho, phase=phase)
        peaks = np.flatnonzero((wave[1:-1] > wave[:-2]) & (wave[1:-1] > wave[2:])) + 1
        return float(rho[peaks[0]])

    speed = 2.0 / 28.0
    base = first_crest(0.0)

    for step in (0.2, 0.4, 0.6):
        assert np.isclose(first_crest(step) - base, speed * step, atol=1.0e-4)


def test_v017_wave_is_periodic_in_the_orbital_phase() -> None:
    rho = np.linspace(0.0, 1.4, 1000)

    # psi = k*rho - omega*phase, so the wave repeats every 2*pi/omega in phase
    for omega_g in (1.0, 2.0, 3.0):
        period = 2.0 * np.pi / omega_g
        base = v017.outgoing_wave(rho, phase=0.4, omega_g=omega_g)

        assert np.allclose(base, v017.outgoing_wave(rho, phase=0.4 + period, omega_g=omega_g))
        assert not np.allclose(
            base, v017.outgoing_wave(rho, phase=0.4 + 0.5 * period, omega_g=omega_g)
        )


def test_v017_theta_is_not_used_by_the_phase_yet() -> None:
    rho = np.full(64, 0.7)
    theta = np.linspace(-np.pi, np.pi, 64)

    wave = v017.outgoing_wave(rho)

    assert np.allclose(wave, wave[0])
    assert np.ptp(theta) > 0.0


def test_v017_is_rendered_weakly() -> None:
    x, y = v017.coordinate_grids(width=300, height=300)

    base = v016.v016_field(x, y)
    rippled = v017.v017_field(x, y)

    difference = np.abs(rippled - base)
    assert difference.max() <= 0.05 + 1.0e-12
    assert difference.max() > 0.0

    lit = base > 0.05
    assert np.median(difference[lit] / base[lit]) < 0.15


def test_v017_reduces_to_v016_without_the_wave() -> None:
    x, y = v017.coordinate_grids(width=200, height=200)

    assert np.allclose(v017.v017_field(x, y, lambda_w=0.0), v016.v016_field(x, y))
    assert np.array_equal(v017.v017_rgb(120, 120, lambda_w=0.0), v016.v016_rgb(120, 120))


def test_v017_keeps_the_silhouettes_solid() -> None:
    x, y = v017.coordinate_grids(width=400, height=400)
    r1, r2 = v017.radial_fields(x, y)
    field = v017.v017_field(x, y)

    margin = 6.0 * v017.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v018_expression_is_finite() -> None:
    x, y = v018.coordinate_grids(width=81, height=65)
    field = v018.v018_field(x, y)
    rgb = v018.v018_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v018_matches_the_boxed_formula() -> None:
    x, y = v018.coordinate_grids(width=121, height=121)
    rho, theta = v018.global_polar(x, y)

    for k_g, omega_g, gamma_w, phase in ((28.0, 2.0, 2.0, 0.0), (12.0, 1.0, 0.5, 1.3)):
        expected = np.cos(2.0 * theta - k_g * rho + omega_g * phase) / (1.0 + gamma_w * rho)
        actual = v018.quadrupole_wave(
            rho, theta, phase=phase, k_g=k_g, omega_g=omega_g, gamma_w=gamma_w
        )
        assert np.allclose(actual, expected)


def test_v018_amplitude_decays_monotonically() -> None:
    rho = np.linspace(0.0, 2.0, 1000)

    for gamma_w in (0.5, 2.0, 5.0):
        amplitude = v018.wave_amplitude(rho, gamma_w)

        assert np.isclose(amplitude[0], 1.0)
        assert np.all(np.diff(amplitude) < 0.0)
        assert np.allclose(amplitude, 1.0 / (1.0 + gamma_w * rho))

    assert np.allclose(v018.wave_amplitude(rho, 0.0), 1.0)


def test_v018_has_two_angular_lobes_at_every_radius() -> None:
    theta = np.linspace(-np.pi, np.pi, 20000, endpoint=False)

    for radius in (0.2, 0.5, 0.9, 1.3):
        rho = np.full_like(theta, radius)
        wave = v018.quadrupole_wave(rho, theta)

        crests = (wave > np.roll(wave, 1)) & (wave > np.roll(wave, -1))
        assert int(crests.sum()) == 2


def test_v018_wave_is_half_turn_symmetric() -> None:
    x, y = v018.coordinate_grids(width=201, height=201)
    rho, theta = v018.global_polar(x, y)

    wave = v018.quadrupole_wave(rho, theta)

    assert np.allclose(wave, np.rot90(wave, 2))


def test_v018_pattern_winds_as_a_two_armed_spiral() -> None:
    k_g = 28.0
    rho = np.linspace(0.3, 0.9, 5000)

    # a ridge satisfies 2*theta - k_g*rho = const, so theta advances at k_g / 2
    theta = 0.5 * (k_g * rho)
    wave = v018.quadrupole_wave(rho, theta, gamma_w=0.0)

    assert np.allclose(wave, 1.0, atol=1.0e-9)


def test_v018_modulation_cannot_create_light() -> None:
    x, y = v018.coordinate_grids(width=400, height=400)

    base = v016.v016_field(x, y)
    modulated = v018.v018_field(x, y)

    dark = base < 1.0e-4
    assert dark.any()
    assert modulated[dark].max() < 1.1e-4

    lit = base > 0.05
    ratio = modulated[lit] / base[lit]
    assert ratio.min() > 1.0 - 0.10 - 1.0e-9
    assert ratio.max() < 1.0 + 0.10 + 1.0e-9


def test_v018_is_a_small_perturbation() -> None:
    x, y = v018.coordinate_grids(width=300, height=300)

    base = v016.v016_field(x, y)
    lit = base > 0.05
    relative = np.abs(v018.v018_field(x, y) - base)[lit] / base[lit]

    assert relative.max() < 0.11
    assert np.median(relative) < 0.05


def test_v018_supersedes_the_v017_placeholder() -> None:
    x, y = v018.coordinate_grids(width=200, height=200)

    # F18 = F16 [1 + e_w W], so the additive v017 term is gone, not stacked
    assert np.allclose(v018.v018_field(x, y, epsilon_w=0.0), v016.v016_field(x, y))
    assert not np.allclose(v018.v018_field(x, y, epsilon_w=0.0), v017.v017_field(x, y))


def test_v018_keeps_the_silhouettes_solid() -> None:
    x, y = v018.coordinate_grids(width=400, height=400)
    r1, r2 = v018.radial_fields(x, y)
    field = v018.v018_field(x, y)

    margin = 6.0 * v018.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v018_rejects_invalid_wave_parameters() -> None:
    import pytest

    x, y = v018.coordinate_grids(width=16, height=16)

    with pytest.raises(ValueError):
        v018.wave_amplitude(np.linspace(0.1, 1.0, 8), -1.0)
    for bad in (1.0, -1.0, 2.5):
        with pytest.raises(ValueError):
            v018.v018_field(x, y, epsilon_w=bad)


def _v019_components(x: np.ndarray, y: np.ndarray, phase: float = 0.0):
    r1, r2 = v019.radial_fields(x, y)
    anchored = v019.angular_fields(x, y)
    theta1, theta2 = v019.phased_angles(*anchored, phase)
    d1, d2 = v019.distorted_radii(r1, r2, *anchored, -0.30)
    s1, s2 = v019.ring_components(d1, d2, theta1, theta2)
    return s1, s2, theta1, theta2


def test_v019_expression_is_finite() -> None:
    x, y = v019.coordinate_grids(width=81, height=65)
    field = v019.v019_field(x, y)
    rgb = v019.v019_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v019_ring_components_sum_to_the_ring_field() -> None:
    x, y = v019.coordinate_grids(width=150, height=150)
    s1, s2, theta1, theta2 = _v019_components(x, y)

    r1, r2 = v019.radial_fields(x, y)
    anchored = v019.angular_fields(x, y)
    d1, d2 = v019.distorted_radii(r1, r2, *anchored, -0.30)

    assert np.allclose(s1 + s2, v019.ring_field(d1, d2, theta1, theta2))
    assert np.allclose(s1 + s2, v018.ring_field(d1, d2, theta1, theta2))


def test_v019_matches_the_plain_angle_specification() -> None:
    x, y = v019.coordinate_grids(width=151, height=151)
    plain1, plain2 = v019.plain_angles(x, y)

    for phase in (0.0, 0.8, 2.9):
        s1, s2, theta1, theta2 = _v019_components(x, y, phase)
        expected = s1 * np.cos(plain1 - phase) - s2 * np.cos(plain2 - phase)

        assert np.allclose(v019.velocity_field(s1, s2, theta1, theta2), expected)


def test_v019_velocity_is_signed_and_bounded_by_the_disks() -> None:
    x, y = v019.coordinate_grids(width=401, height=401)
    s1, s2, theta1, theta2 = _v019_components(x, y)

    velocity = v019.velocity_field(s1, s2, theta1, theta2)

    assert velocity.max() > 0.0
    assert velocity.min() < 0.0
    assert np.all(np.abs(velocity) <= s1 + s2 + 1.0e-12)


def test_v019_approaching_between_the_holes_receding_outside() -> None:
    x, y = v019.coordinate_grids(width=601, height=601)
    s1, s2, theta1, theta2 = _v019_components(x, y)
    velocity = v019.velocity_field(s1, s2, theta1, theta2)

    row = int(np.argmin(np.abs(y[:, 0])))
    between = np.abs(x[row]) < 0.25
    outside = np.abs(x[row]) > 0.42

    assert velocity[row][between].min() > 0.0
    assert velocity[row][outside & (np.abs(x[row]) < 0.6)].max() < 0.0


def test_v019_sign_change_is_a_smooth_crossing() -> None:
    x, y = v019.coordinate_grids(width=600, height=600)
    s1, s2, theta1, theta2 = _v019_components(x, y)
    velocity = v019.velocity_field(s1, s2, theta1, theta2)

    jumps = np.abs(np.diff(velocity, axis=1))
    assert jumps.max() < 0.05 * np.abs(velocity).max()


def test_v019_phase_rotates_the_approaching_side() -> None:
    x, y = v019.coordinate_grids(width=301, height=301)

    base = v019.velocity_field(*_v019_components(x, y, 0.0))
    turned = v019.velocity_field(*_v019_components(x, y, np.pi))

    assert not np.allclose(base, turned)
    assert np.allclose(base, v019.velocity_field(*_v019_components(x, y, 2.0 * np.pi)))


def test_v019_is_a_small_signed_perturbation() -> None:
    x, y = v019.coordinate_grids(width=400, height=400)

    base = v018.v018_field(x, y)
    field = v019.v019_field(x, y)

    assert np.all(field >= 0.0)

    lit = base > 0.05
    relative = (field - base)[lit] / base[lit]
    assert relative.max() > 0.0 and relative.min() < 0.0
    assert np.abs(relative).max() < 0.08


def test_v019_reduces_to_v018_without_velocity() -> None:
    x, y = v019.coordinate_grids(width=200, height=200)

    assert np.allclose(v019.v019_field(x, y, lambda_v=0.0), v018.v018_field(x, y))
    assert np.array_equal(v019.v019_rgb(120, 120, lambda_v=0.0), v018.v018_rgb(120, 120))


def test_v019_signed_diagnostic_uses_both_colours() -> None:
    rgb = v019.velocity_rgb(200, 200)

    assert rgb.shape == (200, 200, 3)
    assert rgb.dtype == np.uint8

    warm = (rgb[..., 0] > rgb[..., 2] + 40).sum()
    cool = (rgb[..., 2] > rgb[..., 0] + 40).sum()
    assert warm > 0 and cool > 0


def test_v019_keeps_the_silhouettes_solid() -> None:
    x, y = v019.coordinate_grids(width=400, height=400)
    r1, r2 = v019.radial_fields(x, y)
    field = v019.v019_field(x, y)

    margin = 6.0 * v019.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v020_expression_is_finite() -> None:
    x, y = v020.coordinate_grids(width=81, height=65)
    field = v020.v020_field(x, y)
    rgb = v020.v020_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v020_factor_matches_the_specification() -> None:
    velocity = np.linspace(-1.0, 1.0, 513)

    for beta_d, p_d in ((0.3, 3.0), (0.5, 2.0), (0.0, 4.0)):
        assert np.allclose(
            v020.doppler_factor_inspired(velocity, beta_d, p_d),
            (1.0 + beta_d * velocity) ** p_d,
        )


def test_v020_disks_are_scaled_by_the_plain_angle_factors() -> None:
    x, y = v020.coordinate_grids(width=151, height=151)
    r1, r2 = v020.radial_fields(x, y)
    anchored = v020.angular_fields(x, y)
    plain1, plain2 = v020.plain_angles(x, y)

    for phase in (0.0, 1.2):
        theta1, theta2 = v020.phased_angles(*anchored, phase)
        d1, d2 = v020.distorted_radii(r1, r2, *anchored, -0.30)
        s1, s2 = v020.ring_components(d1, d2, theta1, theta2)

        v1 = np.cos(plain1 - phase)
        v2 = -np.cos(plain2 - phase)
        expected = (1.0 + 0.3 * v1) ** 3 * s1 + (1.0 + 0.3 * v2) ** 3 * s2

        actual = (
            v020.doppler_factor_inspired(np.cos(theta1)) * s1
            + v020.doppler_factor_inspired(np.cos(theta2)) * s2
        )
        assert np.allclose(actual, expected)


def test_v020_factor_is_positive_and_monotone_in_velocity() -> None:
    velocity = np.linspace(-1.0, 1.0, 1001)

    for beta_d in (0.1, 0.3, 0.9):
        factor = v020.doppler_factor_inspired(velocity, beta_d, 3.0)
        assert np.all(factor > 0.0)
        assert np.all(np.diff(factor) > 0.0)
        assert np.isclose(factor[500], 1.0)


def test_v020_mean_brightening_matches_the_closed_form() -> None:
    theta = np.linspace(-np.pi, np.pi, 8192, endpoint=False)

    for beta_d in (0.1, 0.3, 0.5):
        factor = v020.doppler_factor_inspired(np.cos(theta), beta_d, 3.0)
        assert np.isclose(factor.mean(), 1.0 + 1.5 * beta_d**2, rtol=1.0e-9)


def test_v020_approaching_side_outshines_the_receding_side() -> None:
    velocity = np.array([1.0, -1.0])
    factor = v020.doppler_factor_inspired(velocity)

    assert np.isclose(factor[0] / factor[1], (1.3 / 0.7) ** 3)
    assert factor[0] / factor[1] > 6.0


def test_v020_replaces_the_additive_velocity_term() -> None:
    x, y = v020.coordinate_grids(width=200, height=200)

    for kwargs in ({"beta_d": 0.0}, {"p_d": 0.0}):
        assert np.allclose(v020.v020_field(x, y, **kwargs), v018.v018_field(x, y))
    assert not np.allclose(v020.v020_field(x, y, beta_d=0.0), v019.v019_field(x, y))


def test_v020_leaves_bridge_tails_and_potential_untouched() -> None:
    x, y = v020.coordinate_grids(width=200, height=200)

    difference = v020.v020_field(x, y) - v018.v018_field(x, y)
    r1, r2 = v020.radial_fields(x, y)

    far_from_disks = np.minimum(r1, r2) > 0.75
    assert far_from_disks.any()
    assert np.abs(difference[far_from_disks]).max() < 1.0e-3


def test_v020_keeps_the_silhouettes_solid() -> None:
    x, y = v020.coordinate_grids(width=400, height=400)
    r1, r2 = v020.radial_fields(x, y)
    field = v020.v020_field(x, y)

    assert np.all(field >= 0.0)

    margin = 6.0 * v020.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert field[inside].max() < 1.0e-2


def test_v020_rejects_invalid_doppler_parameters() -> None:
    import pytest

    velocity = np.zeros(4)
    for bad in (-0.1, 1.0, 1.5):
        with pytest.raises(ValueError):
            v020.doppler_factor_inspired(velocity, beta_d=bad)
    with pytest.raises(ValueError):
        v020.doppler_factor_inspired(velocity, p_d=-1.0)


def test_v021_expression_is_finite() -> None:
    x, y = v021.coordinate_grids(width=81, height=65)

    for tone in v021.TONES:
        field = v021.v021_field(x, y, tone=tone)
        rgb = v021.v021_rgb(width=81, height=65, tone=tone)

        assert field.shape == (65, 81)
        assert np.isfinite(field).all()
        assert rgb.shape == (65, 81, 3)
        assert rgb.dtype == np.uint8


def test_v021_compressions_match_the_specification() -> None:
    field = np.linspace(0.0, 8.0, 4001)

    for gamma_l in (0.5, 1.4, 3.0):
        assert np.allclose(
            v021.compress_intensity(field, tone="exponential", gamma_l=gamma_l),
            1.0 - np.exp(-gamma_l * field),
        )
    for p_l, k_l in ((1.5, 0.56), (0.7, 2.0)):
        assert np.allclose(
            v021.compress_intensity(field, tone="hill", p_l=p_l, k_l=k_l),
            field**p_l / (field**p_l + k_l),
        )


def test_v021_compressions_are_bounded_monotone_and_fix_zero() -> None:
    field = np.linspace(0.0, 50.0, 20001)
    # the real field peaks near 6; 1 - exp(-1.4 F) only rounds to exactly 1.0
    # in float64 beyond F = 27, so strictness is checked over a realistic range
    realistic = field <= 10.0

    for tone in ("exponential", "hill"):
        level = v021.compress_intensity(field, tone=tone)

        assert level[0] == 0.0
        assert np.all(level <= 1.0)
        assert np.all(level[realistic] < 1.0)
        assert np.all(np.diff(level) >= 0.0)
        assert level[-1] > 0.95


def test_v021_hill_half_level_sits_at_k_to_the_one_over_p() -> None:
    for p_l, k_l in ((1.5, 0.56), (2.0, 0.25), (0.8, 3.0)):
        half = np.array([k_l ** (1.0 / p_l)])
        assert np.isclose(v021.compress_intensity(half, tone="hill", p_l=p_l, k_l=k_l)[0], 0.5)


def test_v021_linear_tone_reproduces_v020() -> None:
    x, y = v021.coordinate_grids(width=200, height=200)

    assert np.allclose(v021.v021_field(x, y, tone="linear"), v020.v020_field(x, y))
    assert np.array_equal(v021.v021_rgb(120, 120, tone="linear"), v020.v020_rgb(120, 120))


def test_v021_old_ramp_could_never_reach_white_from_a_compressed_field() -> None:
    from event_horizon.color import warm_rgb

    brightest = warm_rgb(np.array([[1.0]]))[0, 0]
    assert brightest[0] == 255 and brightest[2] < 60

    white = v021.tone_rgb(np.array([[1.0]]))[0, 0]
    assert np.all(white == 255)


def test_v021_tone_ramp_is_warm_monotone_and_black_at_zero() -> None:
    level = np.linspace(0.0, 1.0, 1001)[None, :]
    rgb = v021.tone_rgb(level)[0].astype(int)

    assert np.all(rgb[0] == 0)
    for channel in range(3):
        assert np.all(np.diff(rgb[:, channel]) >= 0)
    assert np.all(rgb[:, 0] >= rgb[:, 1])
    assert np.all(rgb[:, 1] >= rgb[:, 2])


def test_v021_bright_structure_whitens_without_flattening() -> None:
    from event_horizon.color import warm_rgb

    x, y = v021.coordinate_grids(width=600, height=600)
    r1, r2 = v021.radial_fields(x, y)
    lit = np.minimum(r1, r2) > 0.16

    raw = v020.v020_field(x, y)
    old = warm_rgb(raw)
    new = v021.v021_rgb(600, 600)

    def near_white(rgb: np.ndarray) -> float:
        return float(np.mean((rgb[lit] >= 250).all(axis=1)))

    def red_flat(rgb: np.ndarray) -> float:
        return float(np.mean(rgb[..., 0][lit] == 255))

    assert near_white(new) > 5.0 * near_white(old)
    assert red_flat(new) < 0.1 * red_flat(old)


def test_v021_keeps_the_faint_structure() -> None:
    from event_horizon.color import warm_rgb

    x, y = v021.coordinate_grids(width=600, height=600)
    r1, r2 = v021.radial_fields(x, y)
    lit = np.minimum(r1, r2) > 0.16

    raw = v020.v020_field(x, y)
    faint = lit & (raw < np.percentile(raw[lit], 50.0))

    old = warm_rgb(raw)[..., 0][faint]
    new = v021.v021_rgb(600, 600)[..., 0][faint]

    assert len(np.unique(new)) >= len(np.unique(old))
    assert new.mean() >= old.mean()


def test_v021_keeps_the_silhouettes_black() -> None:
    x, y = v021.coordinate_grids(width=400, height=400)
    r1, r2 = v021.radial_fields(x, y)

    margin = 6.0 * v021.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    for tone in ("exponential", "hill"):
        level = v021.v021_field(x, y, tone=tone)
        assert level[inside].max() < 1.0e-2


def test_v021_rejects_invalid_tone_parameters() -> None:
    import pytest

    field = np.linspace(0.0, 1.0, 8)
    with pytest.raises(ValueError):
        v021.compress_intensity(field, tone="gamma")
    with pytest.raises(ValueError):
        v021.compress_intensity(field, tone="exponential", gamma_l=0.0)
    for kwargs in ({"p_l": 0.0}, {"k_l": -1.0}):
        with pytest.raises(ValueError):
            v021.compress_intensity(field, tone="hill", **kwargs)


def test_v022_render_is_well_formed() -> None:
    rgb = v022.v022_rgb(width=81, height=65)

    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v022_colour_matches_the_specification() -> None:
    level = np.linspace(0.0, 1.0, 257)[None, :]
    wave = np.linspace(-1.0, 1.0, 257)[None, :]

    colour = v022.colour_equations(level, wave)

    red = 1.0 - np.exp(-4.0 * level)
    green = (1.0 - np.exp(-2.0 * level)) * (1.0 + 0.05 * wave)
    blue = (1.0 - np.exp(-0.7 * level)) * (1.0 + 0.10 * wave)

    assert np.allclose(colour[..., 0], np.clip(red, 0.0, 1.0))
    assert np.allclose(colour[..., 1], np.clip(green, 0.0, 1.0))
    assert np.allclose(colour[..., 2], np.clip(blue, 0.0, 1.0))


def test_v022_colour_is_clamped_to_the_unit_cube() -> None:
    level = np.linspace(-0.5, 20.0, 2001)[None, :]

    for wave in (-1.0, 0.0, 1.0):
        colour = v022.colour_equations(level, wave, shift_g=0.9, shift_b=0.9)
        assert colour.min() >= 0.0
        assert colour.max() <= 1.0


def test_v022_intensity_reduces_to_v021() -> None:
    x, y = v022.coordinate_grids(width=200, height=200)

    # v022 retunes the tone rate and tapers the wave core; undoing both
    # recovers v021's intensity exactly
    assert np.allclose(v022.v022_field(x, y, gamma_l=1.4, core_w=0.0), v021.v021_field(x, y))
    assert not np.allclose(v022.v022_field(x, y), v021.v021_field(x, y))


def test_v022_colour_equations_do_not_wash_out_the_background() -> None:
    x, y = v022.coordinate_grids(width=600, height=600)
    r1, r2 = v022.radial_fields(x, y)
    lit = np.minimum(r1, r2) > 0.16
    corner = (np.abs(x) > 0.85) & (np.abs(y) > 0.85)

    def luma(rgb: np.ndarray) -> np.ndarray:
        rgb = rgb.astype(float)
        return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]

    def contrast(rgb: np.ndarray) -> float:
        low, high = np.percentile(luma(rgb)[lit], [5.0, 99.0])
        return float(high / low)

    doubled = v022.v022_rgb(600, 600, gamma_l=1.4)
    tuned = v022.v022_rgb(600, 600)
    reference = v021.v021_rgb(600, 600)

    assert contrast(doubled) < 5.0
    assert contrast(tuned) > 10.0
    assert abs(luma(tuned)[corner].mean() - luma(reference)[corner].mean()) < 5.0
    assert luma(doubled)[corner].mean() > 3.0 * luma(tuned)[corner].mean()


def test_v022_core_taper_removes_the_pinch_at_the_origin() -> None:
    x, y = v022.coordinate_grids(width=600, height=600)
    rho, _ = v022.global_polar(x, y)
    near = (rho > 0.004) & (rho < 0.02)
    assert near.any()

    tapered = v022.v022_rgb(600, 600)[..., 2][near].astype(int)
    pinched = v022.v022_rgb(600, 600, core_w=0.0)[..., 2][near].astype(int)

    assert np.ptp(pinched) > 15
    assert np.ptp(tapered) < 6


def test_v022_core_taper_is_local() -> None:
    rho = np.linspace(0.0, 1.4, 5000)
    theta = np.linspace(-np.pi, np.pi, 5000)

    tapered = v022.quadrupole_wave(rho, theta)
    plain = v022.quadrupole_wave(rho, theta, core_w=0.0)

    assert tapered[0] == 0.0
    assert np.allclose(tapered[rho > 0.25], plain[rho > 0.25], atol=1.0e-9)
    assert np.all(np.abs(tapered) <= np.abs(plain) + 1.0e-12)

    import pytest

    with pytest.raises(ValueError):
        v022.quadrupole_wave(rho, theta, core_w=-0.1)


def test_v022_faint_hue_recovers_the_original_warm_ratios() -> None:
    faint = v022.colour_equations(np.array([[1.0e-4]]))[0, 0]

    assert np.isclose(faint[1] / faint[0], 2.0 / 4.0, rtol=1.0e-3)
    assert np.isclose(faint[2] / faint[0], 0.7 / 4.0, rtol=1.0e-3)
    assert abs(faint[1] / faint[0] - 0.58 / 1.10) < 0.05
    assert abs(faint[2] / faint[0] - 0.18 / 1.10) < 0.05


def test_v022_brightest_colour_is_gold_not_white() -> None:
    top = v022.to_pixels(v022.colour_equations(np.array([[1.0]])))[0, 0]

    assert tuple(int(c) for c in top) == (250, 220, 128)
    assert top[2] < 200


def test_v022_channels_are_ordered_and_monotone_without_the_wave() -> None:
    level = np.linspace(0.0, 1.0, 1001)[None, :]
    colour = v022.colour_equations(level)[0]

    for channel in range(3):
        assert np.all(np.diff(colour[:, channel]) >= 0.0)
    assert np.all(colour[:, 0] >= colour[:, 1])
    assert np.all(colour[:, 1] >= colour[:, 2])


def test_v022_wave_tints_green_and_blue_but_not_red() -> None:
    x, y = v022.coordinate_grids(width=300, height=300)
    level = v022.v022_field(x, y)
    rho, theta = v022.global_polar(x, y)
    wave = v022.quadrupole_wave(rho, theta)

    tinted = v022.colour_equations(level, wave)
    plain = v022.colour_equations(level, 0.0)

    assert np.allclose(tinted[..., 0], plain[..., 0])

    lit = plain[..., 2] > 0.05
    green_ratio = tinted[..., 1][lit] / plain[..., 1][lit]
    blue_ratio = tinted[..., 2][lit] / plain[..., 2][lit]

    assert np.abs(green_ratio - 1.0).max() <= 0.05 + 1.0e-9
    assert np.abs(blue_ratio - 1.0).max() <= 0.10 + 1.0e-9
    assert np.abs(blue_ratio - 1.0).max() > np.abs(green_ratio - 1.0).max()


def test_v022_render_uses_the_colour_equations() -> None:
    x, y = v022.coordinate_grids(width=120, height=120)
    level = v022.v022_field(x, y)
    rho, theta = v022.global_polar(x, y)

    expected = v022.to_pixels(v022.colour_equations(level, v022.quadrupole_wave(rho, theta)))
    assert np.array_equal(v022.v022_rgb(120, 120), expected)


def test_v022_keeps_the_horizons_black() -> None:
    x, y = v022.coordinate_grids(width=400, height=400)
    r1, r2 = v022.radial_fields(x, y)

    margin = 6.0 * v022.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    rgb = v022.v022_rgb(400, 400)
    assert rgb[inside].max() <= 10


def test_v022_rejects_invalid_colour_parameters() -> None:
    import pytest

    level = np.zeros((2, 2))
    for kwargs in ({"rate_r": 0.0}, {"rate_b": -1.0}, {"shift_g": 1.0}, {"shift_b": -1.2}):
        with pytest.raises(ValueError):
            v022.colour_equations(level, **kwargs)


def test_v023_render_is_well_formed() -> None:
    x, y = v023.coordinate_grids(width=81, height=65)
    field = v023.v023_field(x, y)
    rgb = v023.v023_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v023_background_matches_the_specification() -> None:
    x, y = v023.coordinate_grids(width=151, height=151)
    rho, theta = v023.global_polar(x, y)

    for epsilon_b, gamma_b, eta_b, k_b, m_b in ((0.003, 0.5, 0.5, 12.0, 5), (0.01, 2.0, 1.0, 4.0, 3)):
        expected = epsilon_b * np.exp(-gamma_b * rho) * (1.0 + eta_b * np.cos(k_b * rho + m_b * theta))
        actual = v023.mathematical_background(
            rho, theta, epsilon_b=epsilon_b, gamma_b=gamma_b, eta_b=eta_b, k_b=k_b, m_b=m_b
        )
        assert np.allclose(actual, expected)


def test_v023_background_is_non_negative_and_bounded() -> None:
    rho = np.linspace(0.0, 1.5, 3000)
    theta = np.linspace(-np.pi, np.pi, 3000)

    background = v023.mathematical_background(rho, theta)

    assert background.min() >= 0.0
    assert background.max() <= 0.003 * 1.5 + 1.0e-12


def test_v023_integer_m_keeps_the_pattern_continuous_across_the_cut() -> None:
    radius = np.full(2, 0.6)
    across = np.array([np.pi - 1.0e-9, -np.pi + 1.0e-9])

    continuous = v023.mathematical_background(radius, across, m_b=5)
    assert np.isclose(continuous[0], continuous[1], atol=1.0e-9)

    # the same check with a half-integer m, computed directly, shows the jump
    jump = 0.003 * np.exp(-0.5 * 0.6) * 0.5 * np.cos(12.0 * 0.6 + 2.5 * across)
    assert abs(jump[0] - jump[1]) > 1.0e-4

    import pytest

    with pytest.raises(ValueError):
        v023.mathematical_background(radius, across, m_b=2.5)


def test_v023_background_has_m_arms_at_every_radius() -> None:
    theta = np.linspace(-np.pi, np.pi, 20000, endpoint=False)

    for m_b in (3, 5):
        for radius in (0.3, 0.9):
            pattern = v023.mathematical_background(np.full_like(theta, radius), theta, m_b=m_b)
            crests = (pattern > np.roll(pattern, 1)) & (pattern > np.roll(pattern, -1))
            assert int(crests.sum()) == m_b


def test_v023_reduces_to_v022_without_a_background() -> None:
    x, y = v023.coordinate_grids(width=200, height=200)

    assert np.allclose(v023.v023_field(x, y, epsilon_b=0.0), v022.v022_field(x, y))
    assert np.array_equal(v023.v023_rgb(120, 120, epsilon_b=0.0), v022.v022_rgb(120, 120))


def test_v023_background_is_only_visible_on_close_inspection() -> None:
    new = v023.v023_rgb(600, 600).astype(int)
    old = v022.v022_rgb(600, 600).astype(int)
    difference = new - old

    assert difference.min() >= 0
    assert difference.max() <= 3
    assert difference.max() >= 1

    dark = old.max(axis=2) < 30
    assert np.median(difference[..., 0][dark]) <= 1


def test_v023_background_shows_mainly_in_the_dark() -> None:
    x, y = v023.coordinate_grids(width=600, height=600)
    rho, _ = v023.global_polar(x, y)

    difference = (v023.v023_rgb(600, 600).astype(int) - v022.v022_rgb(600, 600).astype(int))[..., 0]

    corner = (np.abs(x) > 0.85) & (np.abs(y) > 0.85)
    core = rho < 0.1

    assert difference[corner].mean() > difference[core].mean()


def test_v023_horizons_hide_the_background() -> None:
    x, y = v023.coordinate_grids(width=400, height=400)
    r1, r2 = v023.radial_fields(x, y)

    margin = 6.0 * v023.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    loud = v023.v023_field(x, y, epsilon_b=0.5)
    assert loud[inside].max() < 1.0e-2


def test_v023_rejects_invalid_background_parameters() -> None:
    import pytest

    rho = np.linspace(0.0, 1.0, 8)
    theta = np.zeros(8)
    for kwargs in ({"epsilon_b": -0.1}, {"gamma_b": -1.0}, {"eta_b": 1.5}, {"eta_b": -0.1}):
        with pytest.raises(ValueError):
            v023.mathematical_background(rho, theta, **kwargs)


def _v024_disks(n: int):
    x, y = v024.coordinate_grids(width=n, height=n)
    r1, r2 = v024.radial_fields(x, y)
    anchored = v024.angular_fields(x, y)
    theta1, theta2 = v024.phased_angles(*anchored, 0.0)
    d1, d2 = v024.distorted_radii(r1, r2, *anchored, -0.30)
    s1, s2 = v024.ring_components(d1, d2, theta1, theta2)
    return x, y, r1, r2, d1, d2, theta1, theta2, s1, s2


def test_v024_render_is_well_formed() -> None:
    x, y = v024.coordinate_grids(width=81, height=65)

    for structure in v024.STRUCTURES:
        field = v024.v024_field(x, y, structure=structure)
        rgb = v024.v024_rgb(width=81, height=65, structure=structure)

        assert np.isfinite(field).all()
        assert rgb.shape == (65, 81, 3)
        assert rgb.dtype == np.uint8


def test_v024_structure_matches_both_specified_forms() -> None:
    r = np.linspace(0.05, 1.2, 777)
    theta = np.linspace(-np.pi, np.pi, 777)

    product = v024.fine_structure(r, theta, structure="product")
    expected_product = 1.0 + 0.35 * np.sin(90.0 * r + 24 * theta) * np.sin(16 * theta)
    assert np.allclose(product, expected_product)

    logarithmic = v024.fine_structure(r, theta, structure="log")
    expected_log = 1.0 + 0.35 * np.sin(90.0 * r + 24 * theta + 6.0 * np.log(r + 0.02))
    assert np.allclose(logarithmic, expected_log)


def test_v024_structure_factor_is_bounded_and_non_negative() -> None:
    r = np.linspace(0.0, 1.5, 4000)
    theta = np.linspace(-np.pi, np.pi, 4000)

    for structure in v024.STRUCTURES:
        for epsilon_n in (0.35, 1.0):
            factor = v024.fine_structure(r, theta, structure=structure, epsilon_n=epsilon_n)
            assert factor.min() >= 1.0 - epsilon_n - 1.0e-12
            assert factor.max() <= 1.0 + epsilon_n + 1.0e-12
            assert factor.min() >= 0.0


def test_v024_log_term_varies_the_radial_frequency() -> None:
    r = np.array([0.15, 0.3, 0.6])
    k_r, c_n, soft_n = 90.0, 6.0, 0.02

    local = k_r + c_n / (r + soft_n)
    assert np.all(np.diff(local) < 0.0)
    assert local[0] / local[-1] > 1.1


def test_v024_integer_frequencies_keep_the_structure_continuous() -> None:
    radius = np.full(2, 0.3)
    across = np.array([np.pi - 1.0e-9, -np.pi + 1.0e-9])

    for structure in v024.STRUCTURES:
        factor = v024.fine_structure(radius, across, structure=structure)
        assert np.isclose(factor[0], factor[1], atol=1.0e-6)

    import pytest

    for kwargs in ({"m_n": 23.5}, {"k_theta": 7.5}):
        with pytest.raises(ValueError):
            v024.fine_structure(radius, across, **kwargs)


def test_v024_structure_lives_only_in_the_disks() -> None:
    x, y, r1, r2, _, _, _, _, s1, s2 = _v024_disks(600)

    new = v024.v024_rgb(600, 600).astype(int)
    old = v023.v023_rgb(600, 600).astype(int)
    difference = np.abs(new - old)

    dark_disks = np.maximum(s1, s2) < 1.0e-6
    lit_disks = (np.maximum(s1, s2) > 0.05) & (np.minimum(r1, r2) > 0.16)
    corner = (np.abs(x) > 0.85) & (np.abs(y) > 0.85)

    assert difference[dark_disks].max() <= 1
    assert difference[corner].max() == 0
    assert difference[..., 0][lit_disks].mean() > 2.0


def test_v024_structure_barely_moves_mean_brightness() -> None:
    x, y, r1, r2, _, _, _, _, s1, s2 = _v024_disks(600)
    lit = (np.maximum(s1, s2) > 0.02) & (np.minimum(r1, r2) > 0.16)

    before = v023.v023_field(x, y)[lit].mean()
    for structure in v024.STRUCTURES:
        after = v024.v024_field(x, y, structure=structure)[lit].mean()
        assert abs(after - before) < 0.01 * before


def test_v024_does_not_alias_at_small_render_sizes() -> None:
    k_r, m_n, c_n = 90.0, 24, 6.0

    for n in (512, 1200):
        x, y, r1, r2, d1, d2, theta1, _, s1, _ = _v024_disks(n)
        h = v024.grid_spacing(x, y)
        lit = (s1 > 0.02) & (np.minimum(r1, r2) > 0.14 + 3.0 * h)

        phase = k_r * d1 + m_n * theta1 + c_n * np.log(d1 + 0.02)
        gy_c, gx_c = np.gradient(np.cos(phase), h)
        gy_s, gx_s = np.gradient(np.sin(phase), h)
        gradient = np.hypot(
            np.cos(phase) * gx_s - np.sin(phase) * gx_c,
            np.cos(phase) * gy_s - np.sin(phase) * gy_c,
        )
        pixels_per_cycle = 2.0 * np.pi / (np.maximum(gradient, 1.0e-9) * h)

        assert np.percentile(pixels_per_cycle[lit], 0.5) > 4.0


def test_v024_reduces_to_v023_without_structure() -> None:
    x, y = v024.coordinate_grids(width=200, height=200)

    for structure in v024.STRUCTURES:
        assert np.allclose(
            v024.v024_field(x, y, structure=structure, epsilon_n=0.0), v023.v023_field(x, y)
        )
    assert np.array_equal(v024.v024_rgb(120, 120, epsilon_n=0.0), v023.v023_rgb(120, 120))


def test_v024_keeps_the_horizons_black() -> None:
    x, y = v024.coordinate_grids(width=400, height=400)
    r1, r2 = v024.radial_fields(x, y)

    margin = 6.0 * v024.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()
    assert v024.v024_rgb(400, 400)[inside].max() <= 10


def test_v024_rejects_invalid_structure_parameters() -> None:
    import pytest

    r = np.linspace(0.1, 1.0, 8)
    theta = np.zeros(8)
    for kwargs in ({"structure": "noise"}, {"epsilon_n": 1.5}, {"epsilon_n": -0.1}, {"soft_n": 0.0}):
        with pytest.raises(ValueError):
            v024.fine_structure(r, theta, **kwargs)


def test_v025_render_is_well_formed() -> None:
    x, y = v025.coordinate_grids(width=81, height=65)
    field = v025.v025_field(x, y)
    rgb = v025.v025_rgb(width=81, height=65)

    assert field.shape == (65, 81)
    assert np.isfinite(field).all()
    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v025_suppression_matches_the_specification() -> None:
    r1 = np.linspace(0.10, 0.20, 401)
    r2 = np.linspace(0.30, 0.13, 401)

    for k_h in (80.0, 300.0, 600.0):
        h1 = 1.0 / (1.0 + np.exp(-k_h * (r1 - 0.14)))
        h2 = 1.0 / (1.0 + np.exp(-k_h * (r2 - 0.14)))
        assert np.allclose(v025.horizon_suppression(r1, r2, k_h=k_h), h1 * h2)


def test_v025_product_equals_the_old_silhouette_complement() -> None:
    from event_horizon.fields import soft_horizon

    x, y = v025.coordinate_grids(width=600, height=600)
    r1, r2 = v025.radial_fields(x, y)

    for k_h in (150.0, 600.0):
        edge = 1.0 / k_h
        old = 1.0 - np.maximum(soft_horizon(r1, 0.14, edge), soft_horizon(r2, 0.14, edge))
        assert np.allclose(v025.horizon_suppression(r1, r2, k_h=k_h), old, atol=1.0e-12)


def test_v025_suppression_limits() -> None:
    k_h = 600.0
    radius = np.array([0.0, 0.14, 0.5])
    far = np.full(3, 2.0)

    h = v025.horizon_suppression(radius, far, k_h=k_h)
    assert h[0] < 1.0e-20
    assert np.isclose(h[1], 0.5)
    assert np.isclose(h[2], 1.0)


def test_v025_large_k_approaches_a_sharp_boundary() -> None:
    inside = np.array([0.14 - 1.0e-3])
    outside = np.array([0.14 + 1.0e-3])
    far = np.array([2.0])

    for k_h, tolerance in ((600.0, 0.4), (60000.0, 1.0e-12)):
        assert v025.horizon_suppression(inside, far, k_h=k_h)[0] < tolerance
        assert v025.horizon_suppression(outside, far, k_h=k_h)[0] > 1.0 - tolerance


def test_v025_sharp_k_does_not_overflow() -> None:
    import warnings

    r = np.linspace(0.0, 2.0, 64)
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        values = v025.horizon_suppression(r, r, k_h=1.0e6)
    assert np.isfinite(values).all()


def test_v025_edge_width_is_controlled_by_k() -> None:
    r = np.linspace(0.0, 0.3, 300001)
    far = np.full_like(r, 2.0)

    def width(k_h: float) -> float:
        h = v025.horizon_suppression(r, far, k_h=k_h)
        return float(r[np.argmax(h >= 0.9)] - r[np.argmax(h >= 0.1)])

    for k_h in (80.0, 300.0, 600.0):
        assert np.isclose(width(k_h), np.log(81.0) / k_h, rtol=1.0e-3)
    assert np.isclose(width(150.0) / width(600.0), 4.0, rtol=1.0e-2)


def test_v025_default_edge_matches_v003_at_full_size_but_not_smaller() -> None:
    edge_units = np.log(81.0) / 600.0

    for n, expected_pixels in ((1200, 4.4), (512, 1.9)):
        x, y = v025.coordinate_grids(width=n, height=n)
        assert np.isclose(edge_units / v025.grid_spacing(x, y), expected_pixels, atol=0.1)


def test_v025_only_the_horizon_edge_changes_from_v024() -> None:
    x, y = v025.coordinate_grids(width=600, height=600)
    r1, r2 = v025.radial_fields(x, y)
    nearest = np.minimum(r1, r2)

    before = v024.v024_field(x, y)
    after = v025.v025_field(x, y)

    assert np.allclose(after[nearest > 0.20], before[nearest > 0.20], atol=1.0e-12)
    assert np.abs(after - before)[(nearest > 0.12) & (nearest < 0.17)].max() > 1.0e-3

    far = nearest > 0.20
    rgb_difference = np.abs(v025.v025_rgb(600, 600).astype(int) - v024.v024_rgb(600, 600).astype(int))
    assert rgb_difference[far].max() == 0


def test_v025_suppression_is_applied_last() -> None:
    x, y = v025.coordinate_grids(width=300, height=300)
    r1, r2 = v025.radial_fields(x, y)

    for k_h in (80.0, 600.0):
        suppression = v025.horizon_suppression(r1, r2, k_h=k_h)
        unmasked = v025.v025_field(x, y, k_h=1.0e-9) / v025.horizon_suppression(r1, r2, k_h=1.0e-9)
        assert np.allclose(v025.v025_field(x, y, k_h=k_h), suppression * unmasked, atol=1.0e-9)


def test_v025_keeps_the_horizons_black() -> None:
    x, y = v025.coordinate_grids(width=400, height=400)
    r1, r2 = v025.radial_fields(x, y)

    margin = 6.0 * v025.grid_spacing(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - margin
    assert inside.any()

    assert v025.v025_field(x, y)[inside].max() < 1.0e-2
    assert v025.v025_rgb(400, 400)[inside].max() <= 10


def test_v025_rejects_invalid_suppression_parameters() -> None:
    import pytest

    r = np.linspace(0.1, 1.0, 8)
    for kwargs in ({"k_h": 0.0}, {"k_h": -5.0}, {"horizon_radius": 0.0}):
        with pytest.raises(ValueError):
            v025.horizon_suppression(r, r, **kwargs)


V026_DELETED = {"epsilon_w": 0.0, "anisotropy": 0.0, "epsilon_b": 0.0, "tone": "linear"}


def _v026_reference(x: np.ndarray, y: np.ndarray, **parameters) -> np.ndarray:
    return 1.0 - np.exp(-0.25 * v025.v025_field(x, y, **V026_DELETED, **parameters))


def test_v026_render_is_well_formed() -> None:
    x, y = v026.coordinate_grids(width=81, height=65)
    level = v026.v026_field(x, y)
    rgb = v026.v026_rgb(width=81, height=65)

    assert level.shape == (65, 81)
    assert np.isfinite(level).all()
    assert level.min() >= 0.0 and level.max() < 1.0
    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v026_is_v025_with_the_deleted_terms_switched_off() -> None:
    x, y = v026.coordinate_grids(width=240, height=240)

    for parameters in ({}, {"phase": 1.1}, {"pitch": 0.6, "distortion": 0.0, "strength": 0.4}):
        reference = _v026_reference(x, y, **parameters)
        assert np.array_equal(v026.v026_field(x, y, **parameters), reference)

    reference_pixels = v025.to_pixels(v025.colour_equations(_v026_reference(x, y), 0.0))
    assert np.array_equal(v026.v026_rgb(240, 240), reference_pixels)


def test_v026_deleted_terms_are_gone_from_the_code() -> None:
    for name in (
        "mathematical_background",
        "quadrupole_wave",
        "outgoing_wave",
        "global_polar",
        "angular_weight",
        "compress_intensity",
        "tone_rgb",
        "velocity_rgb",
        "velocity_field",
        "silhouette_field",
        "ring_field",
    ):
        assert not hasattr(v026, name), name

    import inspect

    assert set(inspect.signature(v026.doppler_factor_inspired).parameters) == {"velocity", "beta_d", "p_d"}
    assert set(inspect.signature(v026.colour_equations).parameters) == {"level", "rate_r", "rate_g", "rate_b"}
    for removed in ("epsilon_w", "anisotropy", "epsilon_b", "core_w", "shift_g", "tone", "structure"):
        assert removed not in inspect.signature(v026.v026_field).parameters


def test_v026_deletions_are_not_visible() -> None:
    full = v025.v025_rgb(600, 600).astype(int)
    pruned = v026.v026_rgb(600, 600).astype(int)

    difference = np.abs(full - pruned).max(axis=2)
    assert difference.mean() < 3.5
    assert np.percentile(difference, 99) <= 20


def test_v026_every_surviving_term_still_matters() -> None:
    base = v026.v026_rgb(400, 400).astype(int)

    for switch in (
        {"glow": 0.0},
        {"beta": 0.0},
        {"harmonic": 0.0},
        {"pitch": 0.5 * np.pi},
        {"decay": 0.0},
        {"distortion": 0.0},
        {"strength": 0.0},
        {"tails": 0.0},
        {"lambda_p": 0.0},
        {"beta_d": 0.0},
        {"epsilon_n": 0.0},
    ):
        difference = np.abs(v026.v026_rgb(400, 400, **switch).astype(int) - base).max(axis=2)
        assert np.percentile(difference, 99) >= 10, switch


def test_v026_cli_defaults_match_the_equation() -> None:
    import inspect
    import sys

    defaults = {
        name: parameter.default
        for function in (v026.v026_field, v026.v026_rgb)
        for name, parameter in inspect.signature(function).parameters.items()
        if parameter.default is not inspect.Parameter.empty
    }

    saved = sys.argv
    sys.argv = ["v026"]
    try:
        options = vars(v026.parse_args())
    finally:
        sys.argv = saved

    for name, default in defaults.items():
        if name in options:
            assert options[name] == default, name
    extras = set(options) - set(defaults) - {"width", "height", "output", "series", "pitch_degrees", "phase_degrees"}
    assert not extras


def test_v026_keeps_the_horizons_black() -> None:
    x, y = v026.coordinate_grids(width=400, height=400)
    r1, r2 = v026.radial_fields(x, y)
    spacing = 2.0 / 399.0

    inside = np.minimum(r1, r2) <= 0.14 - 6.0 * spacing
    assert inside.any()
    assert v026.v026_field(x, y)[inside].max() < 1.0e-2
    assert v026.v026_rgb(400, 400)[inside].max() <= 10


def test_v026_phase_series_tiles_four_renders() -> None:
    series = v026.phase_series(40, 30, gap=4)

    assert series.shape == (64, 84, 3)
    assert np.array_equal(series[:30, :40], v026.v026_rgb(40, 30, phase=0.0))


def test_v026_rejects_invalid_parameters() -> None:
    import pytest

    x, y = v026.coordinate_grids(width=16, height=16)
    with pytest.raises(ValueError):
        v026.v026_field(x, y, gamma_l=0.0)
    with pytest.raises(ValueError):
        v026.colour_equations(np.zeros((2, 2)), rate_b=0.0)
    with pytest.raises(ValueError):
        v026.fine_structure(np.full(2, 0.3), np.zeros(2), m_n=23.5)


def test_v027_render_is_well_formed() -> None:
    x, y = v027.coordinate_grids(width=81, height=65)
    level = v027.v027_field(x, y)
    rgb = v027.v027_rgb(width=81, height=65)

    assert level.shape == (65, 81)
    assert np.isfinite(level).all()
    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v027_reduces_to_v026_without_lensing() -> None:
    x, y = v027.coordinate_grids(width=240, height=240)

    for parameters in ({}, {"phase": 1.1}, {"pitch": 0.6, "strength": 0.4}):
        assert np.array_equal(
            v027.v027_field(x, y, einstein_radius=0.0, **parameters), v026.v026_field(x, y, **parameters)
        )
    assert np.array_equal(v027.v027_rgb(240, 240, einstein_radius=0.0), v026.v026_rgb(240, 240))


def test_v027_lens_is_the_softened_binary_point_lens() -> None:
    x, y = v027.coordinate_grids(width=121, height=121)
    r_e, soft = 0.12, 0.02

    expected_x, expected_y = x.copy(), y.copy()
    for cx, cy in v027.black_hole_centers():
        dx, dy = x - cx, y - cy
        denominator = dx**2 + dy**2 + soft**2
        expected_x = expected_x - r_e**2 * dx / denominator
        expected_y = expected_y - r_e**2 * dy / denominator

    lensed_x, lensed_y, _ = v027.binary_lens(x, y, einstein_radius=r_e, soft=soft)
    assert np.allclose(lensed_x, expected_x)
    assert np.allclose(lensed_y, expected_y)


def test_v027_analytic_jacobian_matches_finite_differences() -> None:
    n = 1200
    x, y = v027.coordinate_grids(width=n, height=n)
    h = 2.0 / (n - 1)
    r1, r2 = v027.radial_fields(x, y)
    visible = np.minimum(r1, r2) > 0.14 + 3.0 * h

    lensed_x, lensed_y, determinant = v027.binary_lens(x, y)
    dxy, dxx = np.gradient(lensed_x, -h, h)
    dyy, dyx = np.gradient(lensed_y, -h, h)
    numeric = dxx * dyy - dxy * dyx

    assert np.abs(determinant - numeric)[visible].max() < 1.0e-3


def test_v027_magnification_is_inverse_determinant_to_a_power() -> None:
    determinant = np.array([1.0, 0.5, 0.25, 0.05, -3.0])

    boost = v027.lens_magnification(determinant, magnification=1.5, det_floor=0.2)
    expected = (1.0 / np.maximum(np.abs(determinant), 0.2)) ** 1.5
    assert np.allclose(boost, expected)
    assert boost[0] == 1.0
    assert boost[3] == boost[3]  # clamped rather than infinite
    assert np.all(np.isfinite(boost))
    assert np.allclose(v027.lens_magnification(determinant, magnification=0.0), 1.0)


def test_v027_default_lens_never_folds_outside_the_horizons() -> None:
    n = 600
    x, y = v027.coordinate_grids(width=n, height=n)
    r1, r2 = v027.radial_fields(x, y)
    visible = np.minimum(r1, r2) > 0.14 + 3.0 * (2.0 / (n - 1))

    _, _, safe = v027.binary_lens(x, y, einstein_radius=0.12)
    _, _, folded = v027.binary_lens(x, y, einstein_radius=0.16)

    assert safe[visible].min() > 0.4
    assert folded[visible].min() < 0.0


def test_v027_magnification_intensifies_the_rim_and_the_warp_alone_does_not() -> None:
    x, y = v027.coordinate_grids(width=600, height=600)
    r1, r2 = v027.radial_fields(x, y)
    nearest = np.minimum(r1, r2)
    rim = (nearest > 0.14) & (nearest < 0.19)

    before = v026.v026_field(x, y)[rim].mean()
    warped_only = v027.v027_field(x, y, magnification=0.0)[rim].mean()
    lensed = v027.v027_field(x, y)[rim].mean()

    assert warped_only < before
    assert lensed > 1.2 * before


def test_v027_renders_in_strips_identically() -> None:
    n, rows = 301, 37
    xs = np.linspace(-1.0, 1.0, n)
    ys = np.linspace(1.0, -1.0, n)
    tiled = np.empty((n, n, 3), dtype=np.uint8)
    for start in range(0, n, rows):
        x, y = np.meshgrid(xs, ys[start : start + rows])
        tiled[start : start + rows] = v027.to_pixels(v027.colour_equations(v027.v027_field(x, y)))

    assert np.array_equal(tiled, v027.v027_rgb(n, n))


def test_v027_crowding_does_not_alias_at_small_sizes() -> None:
    n = 512
    x, y = v027.coordinate_grids(width=n, height=n)
    h = 2.0 / (n - 1)
    true1, true2 = v027.radial_fields(x, y)

    lx, ly, _ = v027.binary_lens(x, y)
    r1, r2 = v027.radial_fields(lx, ly)
    t1, t2 = v027.angular_fields(lx, ly)
    d1, d2 = v027.distorted_radii(r1, r2, t1, t2, -0.30)
    phase1, _ = v027.phased_angles(t1, t2, 0.0)
    s1, _ = v027.ring_components(d1, d2, phase1, phase1)

    psi = 90.0 * d1 + 24 * phase1 + 6.0 * np.log(d1 + 0.02)
    gy_c, gx_c = np.gradient(np.cos(psi), h)
    gy_s, gx_s = np.gradient(np.sin(psi), h)
    gradient = np.hypot(np.cos(psi) * gx_s - np.sin(psi) * gx_c, np.cos(psi) * gy_s - np.sin(psi) * gy_c)
    lit = (np.minimum(true1, true2) > 0.14 + 3.0 * h) & (s1 > 0.02)

    assert np.percentile((2.0 * np.pi / (np.maximum(gradient, 1.0e-9) * h))[lit], 0.5) > 4.0


def test_v027_keeps_the_horizons_black() -> None:
    n = 400
    x, y = v027.coordinate_grids(width=n, height=n)
    r1, r2 = v027.radial_fields(x, y)
    inside = np.minimum(r1, r2) <= 0.14 - 6.0 * (2.0 / (n - 1))
    assert inside.any()

    assert v027.v027_field(x, y)[inside].max() < 1.0e-2
    assert v027.v027_rgb(n, n)[inside].max() <= 10


def test_v027_rejects_invalid_lens_parameters() -> None:
    import pytest

    x, y = v027.coordinate_grids(width=8, height=8)
    with pytest.raises(ValueError):
        v027.binary_lens(x, y, einstein_radius=-0.1)
    with pytest.raises(ValueError):
        v027.binary_lens(x, y, soft=0.0)
    for kwargs in ({"magnification": -1.0}, {"det_floor": 0.0}):
        with pytest.raises(ValueError):
            v027.lens_magnification(np.ones(3), **kwargs)


V028_OFF = {"kappa_n": 0.0, "lambda_n": 0.0, "zeta_n": 0.0}


def test_v028_render_is_well_formed() -> None:
    x, y = v028.coordinate_grids(width=81, height=65)
    level = v028.v028_field(x, y)
    rgb = v028.v028_rgb(width=81, height=65)
    assert level.shape == (65, 81)
    assert np.all(np.isfinite(level))
    assert np.all((level >= 0.0) & (level <= 1.0))
    assert rgb.shape == (65, 81, 3)
    assert rgb.dtype == np.uint8


def test_v028_reduces_to_v027_with_ripples_frozen() -> None:
    x, y = v028.coordinate_grids(width=240, height=240)
    for parameters in ({}, {"phase": 1.1}):
        assert np.array_equal(
            v028.v028_field(x, y, **V028_OFF, **parameters), v027.v027_field(x, y, **parameters)
        )
    assert np.array_equal(v028.v028_rgb(240, 240, **V028_OFF), v027.v027_rgb(240, 240))


def test_v028_chirp_keeps_ring_spacing_and_tightens_inside() -> None:
    r = np.linspace(0.02, 0.9, 2001)
    h = r[1] - r[0]
    slope = np.gradient(v028.chirped_radius(r, kappa_n=10.0, reference=0.25), h)
    expected = (1.0 + 10.0 * 0.25) / (1.0 + 10.0 * r)
    assert np.allclose(slope[1:-1], expected[1:-1], rtol=1e-4)
    ring = np.argmin(np.abs(r - 0.25))
    assert abs(slope[ring] - 1.0) < 1e-3
    assert np.all(np.diff(slope[1:-1]) < 0.0)
    assert np.array_equal(v028.chirped_radius(r, kappa_n=0.0), r)


def test_v028_amplitude_is_unchanged_at_ring_capped_inside_and_fades_outside() -> None:
    r = np.linspace(0.0, 1.0, 1001)
    amplitude = v028.ripple_amplitude(r, epsilon_n=0.35, lambda_n=8.0, reference=0.25)
    assert np.isclose(v028.ripple_amplitude(np.array(0.25), 0.35, 8.0, 0.25), 0.35)
    assert amplitude.max() == 1.0
    assert np.all(np.diff(amplitude) <= 0.0)
    assert amplitude[r >= 0.45].max() < 0.35 * np.exp(-8.0 * 0.2) + 1e-12
    assert v028.ripple_amplitude(r, 0.35, 0.0) == 0.35


def test_v028_tidal_warp_faces_the_companion_and_grows_with_r_squared() -> None:
    theta = np.linspace(-np.pi, np.pi, 721)
    r = np.full_like(theta, 0.25)
    warp = v028.tidal_warp(r, theta, zeta_n=3.0, reference=0.25)
    assert np.isclose(warp[np.argmin(np.abs(theta))], 3.0)
    assert np.isclose(warp[np.argmin(np.abs(theta - 0.5 * np.pi))], -3.0)
    assert np.allclose(warp, v028.tidal_warp(r, v028.wrap_angle(theta + np.pi), 3.0, 0.25))
    assert np.allclose(v028.tidal_warp(2.0 * r, theta, 3.0, 0.25), 4.0 * warp)
    assert v028.tidal_warp(r, theta, zeta_n=0.0) == 0.0


def test_v028_tidal_warp_does_not_rotate_with_the_orbit(monkeypatch: pytest.MonkeyPatch) -> None:
    seen = []
    original = v028.tidal_warp

    def spy(r, anchored_theta, zeta_n=0.0, reference=0.25):
        seen.append(anchored_theta.copy())
        return original(r, anchored_theta, zeta_n, reference)

    monkeypatch.setattr(v028, "tidal_warp", spy)
    x, y = v028.coordinate_grids(width=41, height=41)
    v028.v028_field(x, y, phase=0.0)
    still = seen[:]
    seen.clear()
    v028.v028_field(x, y, phase=1.3)
    for before, after in zip(still, seen):
        assert np.array_equal(before, after)


def test_v028_strip_rendering_is_bit_identical() -> None:
    width, height = 90, 70
    x, y = v028.coordinate_grids(width=width, height=height)
    whole = v028.v028_field(x, y)
    strips = np.vstack(
        [v028.v028_field(x[start : start + 25], y[start : start + 25]) for start in range(0, height, 25)]
    )
    assert np.array_equal(whole, strips)


def test_v028_fine_structure_stays_non_negative() -> None:
    r = np.linspace(0.0, 1.2, 601)[:, None] * np.ones((1, 360))
    theta = np.linspace(-np.pi, np.pi, 360)[None, :] * np.ones((601, 1))
    n = v028.fine_structure(r, theta, kappa_n=10.0, lambda_n=8.0, zeta_n=3.0)
    assert n.min() >= 0.0
    assert n.max() <= 2.0


def test_v028_rejects_invalid_ripple_parameters() -> None:
    r = np.linspace(0.1, 0.5, 5)
    with pytest.raises(ValueError):
        v028.chirped_radius(r, kappa_n=-1.0)
    with pytest.raises(ValueError):
        v028.ripple_amplitude(r, lambda_n=-1.0)


def test_v028_cli_defaults_match_the_field() -> None:
    import inspect
    import sys as _sys

    signature = inspect.signature(v028.v028_field).parameters
    argv, _sys.argv = _sys.argv, ["v028"]
    try:
        options = vars(v028.parse_args())
    finally:
        _sys.argv = argv
    for name in ("kappa_n", "lambda_n", "zeta_n", "epsilon_n", "k_r", "einstein_radius"):
        assert options[name] == signature[name].default
