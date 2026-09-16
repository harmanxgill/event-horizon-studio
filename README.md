# Event Horizon Studio

A place to build mathematical images about black holes, spacetime, and astrophysics.

## Philosophy

Each image should come from equations. Python is just there to evaluate the functions on a grid and save the pixels.

## Gallery

Finished images can go in `gallery/`.

## Pieces

| Piece | Status | Notes |
| --- | --- | --- |
| [001 - The Last Orbit](https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit "https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit") | v030 (final) | Equal-mass binary black holes in the final orbit before merger. Final image: `gallery/001_THE_LAST_ORBIT_FINAL.png`. |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Rendering

Render the latest version:

```bash
python pieces/001_last_orbit/experiments/v030_final_tone.py
```

Render the final gallery image (6000x6000, in strips):

```bash
python pieces/001_last_orbit/experiments/v030_final_tone.py --width 6000 --height 6000 --strip-rows 250 --output gallery/001_THE_LAST_ORBIT_FINAL.png
```

Render the timelapse of every version, v001 to v030, ending on one full orbit of the final image (`gallery/001_THE_LAST_ORBIT_TIMELAPSE.mp4`, 1080x1080, about 48 seconds):

```bash
pip install -e ".[video]"
python pieces/001_last_orbit/timelapse.py
```

Add `--orbit-seconds 0` to skip the orbit, or `--no-labels` to hide the version names.

Render it smaller:

```bash
python pieces/001_last_orbit/experiments/v030_final_tone.py --width 512 --height 512
```

Earlier versions still render on their own:

```bash
python pieces/001_last_orbit/experiments/v001_two_radial_fields.py
python pieces/001_last_orbit/experiments/v002_horizon_masks.py
python pieces/001_last_orbit/experiments/v003_sharp_horizons.py
python pieces/001_last_orbit/experiments/v004_outer_glow.py
python pieces/001_last_orbit/experiments/v005_angular_fields.py
python pieces/001_last_orbit/experiments/v006_beamed_rings.py
python pieces/001_last_orbit/experiments/v007_structured_light.py
python pieces/001_last_orbit/experiments/v008_coupled_radius.py
python pieces/001_last_orbit/experiments/v009_log_spiral.py
python pieces/001_last_orbit/experiments/v010_spiral_decay.py
python pieces/001_last_orbit/experiments/v011_orbital_phase.py
python pieces/001_last_orbit/experiments/v012_companion_distortion.py
python pieces/001_last_orbit/experiments/v013_interaction_field.py
python pieces/001_last_orbit/experiments/v014_tidal_bridge.py
python pieces/001_last_orbit/experiments/v015_tidal_tails.py
python pieces/001_last_orbit/experiments/v016_global_potential.py
python pieces/001_last_orbit/experiments/v017_outgoing_wave.py
python pieces/001_last_orbit/experiments/v018_quadrupolar_field.py
python pieces/001_last_orbit/experiments/v019_velocity_field.py
python pieces/001_last_orbit/experiments/v020_doppler_luminosity.py
python pieces/001_last_orbit/experiments/v021_nonlinear_intensity.py
python pieces/001_last_orbit/experiments/v022_rgb_equations.py
python pieces/001_last_orbit/experiments/v023_mathematical_background.py
python pieces/001_last_orbit/experiments/v024_fine_structure.py
python pieces/001_last_orbit/experiments/v025_horizon_suppression.py
python pieces/001_last_orbit/experiments/v026_final_equation.py
python pieces/001_last_orbit/experiments/v027_horizon_lensing.py
python pieces/001_last_orbit/experiments/v028_evolving_ripples.py
python pieces/001_last_orbit/experiments/v029_approaching_side.py
```

The current renders use a square `1200x1200` default so the images line up cleanly.

## Tests

```bash
pytest
```

## Extending The Studio

Add new pieces under `pieces/002_name/`, `pieces/003_name/`, and so on. Keep shared array/image code in `src/event_horizon/`. Keep each piece's equations with that piece.
