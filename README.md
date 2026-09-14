# Event Horizon Studio

A place to build mathematical images about black holes, spacetime, and astrophysics.

## Philosophy

Each image should come from equations. Python is just there to evaluate the functions on a grid and save the pixels.

## Gallery

Finished images can go in `gallery/`.

## Pieces

| Piece | Status | Notes |
| --- | --- | --- |
| 001 - The Last Orbit | v001 | Equal-mass binary black holes in the final orbit before merger. |

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Rendering

Render v001:

```bash
python pieces/001_last_orbit/experiments/v001_two_radial_fields.py
```

Render it smaller:

```bash
python pieces/001_last_orbit/experiments/v001_two_radial_fields.py --width 512 --height 512
```

## Tests

```bash
pytest
```

## Extending The Studio

Add new pieces under `pieces/002_name/`, `pieces/003_name/`, and so on. Keep shared array/image code in `src/event_horizon/`. Keep each piece's equations with that piece.
