# Event Horizon Studio

A place to build mathematical images about black holes, spacetime, and astrophysics.

## Philosophy

Each image should come from equations. Python is just there to evaluate the functions on a grid and save the pixels.

## Gallery

Finished images can go in `gallery/`.

## Pieces

| Piece | Status | Notes |
| --- | --- | --- |
| [001 - The Last Orbit](https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit "https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit") | v007 | Equal-mass binary black holes in the final orbit before merger. |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Rendering

Render the latest version:

```bash
python pieces/001_last_orbit/experiments/v007_structured_light.py
```

Render it smaller:

```bash
python pieces/001_last_orbit/experiments/v007_structured_light.py --width 512 --height 512
```

Earlier versions still render on their own:

```bash
python pieces/001_last_orbit/experiments/v001_two_radial_fields.py
python pieces/001_last_orbit/experiments/v002_horizon_masks.py
python pieces/001_last_orbit/experiments/v003_sharp_horizons.py
python pieces/001_last_orbit/experiments/v004_outer_glow.py
python pieces/001_last_orbit/experiments/v005_angular_fields.py
python pieces/001_last_orbit/experiments/v006_beamed_rings.py
```

The current renders use a square `1200x1200` default so the images line up cleanly.

## Tests

```bash
pytest
```

## Extending The Studio

Add new pieces under `pieces/002_name/`, `pieces/003_name/`, and so on. Keep shared array/image code in `src/event_horizon/`. Keep each piece's equations with that piece.
