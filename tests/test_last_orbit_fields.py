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
