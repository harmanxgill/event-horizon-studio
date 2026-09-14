# 001 - The Last Orbit

[GitHub link](https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit "https://github.com/harmanxgill/event-horizon-studio/tree/main/pieces/001_last_orbit")

## Concept

Two equal-mass black holes in the last orbit before merger. This is art from equations, not a physics simulation.

## Mathematical Construction

The coordinate plane is normalized around the binary center of mass. With orbital phase `phi` and separation `d`, the centers are

```text
c1 = -(d / 2) (cos(phi), sin(phi))
c2 =  (d / 2) (cos(phi), sin(phi))
```

For each image coordinate `(x, y)`, the base fields are

```text
r1 = sqrt((x - c1x)^2 + (y - c1y)^2)
r2 = sqrt((x - c2x)^2 + (y - c2y)^2)

theta1 = atan2(y - c1y, x - c1x)
theta2 = atan2(y - c2y, x - c2x)
```

## Parameters

| Parameter | Meaning |
| --- | --- |
| `width`, `height` | Number of sampled pixels in the rendered grid. |
| `extent` | Half-width of the mathematical coordinate plane. |
| `separation` | Distance between the two equal-mass centers. |
| `orbit_phase` | Rotation angle of the binary axis in radians. |
| `horizon_radius` | Radius used for each horizon field. |
| `horizon_edge` | Softness of the logistic horizon boundary. |
| `softening` | Small radial term used to keep future inverse fields finite. |

## Rendering

From the repository root:

```bash
python pieces/001_last_orbit/render.py --width 1200 --height 1200
```

The default output path is `pieces/001_last_orbit/output/last_orbit_preview.png`.

## Experiments

### v001 - two radial fields

The first experiment:

```text
F(x, y) = exp(-80(r1 - 0.25)^2) + exp(-80(r2 - 0.25)^2)
```

The RGB image comes directly from `F`.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v001_two_radial_fields.py
```

### v002 - horizon masks

The same two rings, with an event horizon carved out of each center. With the
logistic horizon field

```text
H(r) = 1 / (1 + exp((r - r_h) / w))
S(x, y) = max(H(r1), H(r2))
```

the image becomes

```text
G(x, y) = F(x, y) (1 - S(x, y))
```

`S` is close to `1` inside either horizon and close to `0` outside it, so `G`
matches `F` away from the centers and falls to zero within `r_h`. The horizon
radius `r_h = 0.14` and edge width `w = 0.015` are the same values
`equations.py` uses, so the experiment and the piece agree.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v002_horizon_masks.py
```

### v003 - sharp horizons

v002's horizon edge is a fixed width `w = 0.015` in coordinate units, so the
shadow fades over roughly nine pixels at `1200x1200` and over twice that at
double the resolution. v003 sharpens it by tying `w` to the sampling itself.
With grid spacing `h`,

```text
w = k h
```

where `k` is the edge width measured in pixels (`edge_pixels`, default `1`).
The construction is otherwise v002's:

```text
S(x, y) = max(H(r1), H(r2))
G(x, y) = F(x, y) (1 - S(x, y))
```

A true step function `w -> 0` would alias the circle into a staircase. One
pixel of falloff is the sharpest edge the grid can represent without that, so
the silhouettes read as solid objects cut out of the glow, and they stay
equally crisp at every resolution: the partially lit rim is about one pixel
wide whether the render is `400x400` or `2400x2400`.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v003_sharp_horizons.py
```

Soften the rim again with a wider edge:

```bash
python pieces/001_last_orbit/experiments/v003_sharp_horizons.py --edge-pixels 4
```

### v004 - outer glow

A secondary radial falloff around each hole. The ring is a Gaussian of width
`1 / sqrt(s)` about `r_ring`, so the light it contributes has effectively died
out one ring width further out. That distance is where the halo begins:

```text
r_glow = r_ring + 1 / sqrt(s)
```

The halo is a slow exponential decay from `r_glow`, switched on by the same
logistic used for the horizons, now placed at `r_glow` instead of `r_h`:

```text
A(r) = g (1 - H(r; r_glow, u)) exp(-b (r - r_glow))
```

`1 - H` is close to `0` inside `r_glow` and close to `1` outside it, so the
glow belongs to the region beyond the ring and leaves the ring's own profile
alone. Summing over both holes and reapplying v003's silhouettes,

```text
G(x, y) = (F(x, y) + A(r1) + A(r2)) (1 - S(x, y))
```

The product of a rising gate and a falling exponential is not monotone: the
halo peaks a little outside `r_glow`, near `r = 0.45`, then decays to under a
twentieth of that by the edge of the frame. The two halos overlap between the
holes, which is what brightens the bridge across the middle.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v004_outer_glow.py
```

Turn the halo down, or stretch it further out:

```bash
python pieces/001_last_orbit/experiments/v004_outer_glow.py --glow 0.15
python pieces/001_last_orbit/experiments/v004_outer_glow.py --falloff 2.0
```

### v005 - angular fields

Everything so far depends only on `r1` and `r2`, so every version through v004
is exactly rotationally symmetric about each hole. v005 introduces the missing
half of the polar coordinates.

The angle is measured from the direction each hole faces its companion, not
from the `x` axis. `theta1` already has that origin; `theta2` is turned by half
a rotation and folded back into one turn:

```text
theta1 = atan2(y - c1y, x - c1x)
theta2 = wrap(atan2(y - c2y, x - c2x) - pi)
wrap(t) = atan2(sin t, cos t)
```

So `theta = 0` points at the companion for both holes and `theta = +-pi` points
away. The two frames are mirror images, which is what keeps the image
left-right symmetric even though it is no longer rotationally symmetric.

The first use of the new coordinate is a single cosine on each ring:

```text
W(theta) = 1 + e cos(theta)
F(x, y) = exp(-s(r1 - r_ring)^2) W(theta1) + exp(-s(r2 - r_ring)^2) W(theta2)
```

`W` averages to `1` around a full turn, so the anisotropy `e` redistributes
ring brightness rather than adding any. At the default `e = 0.35` each ring is
`1.35` times as bright on the side facing its companion and `0.65` times as
bright on the far side, which lights up the bridge between the holes. Setting
`e = 0` reproduces v004 exactly.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v005_angular_fields.py
```

Flip the anisotropy to dim the facing sides instead, which separates the two
holes rather than fusing them:

```bash
python pieces/001_last_orbit/experiments/v005_angular_fields.py --anisotropy -0.35
```

Possible next versions:

- v006: disk distortion toward the companion
- v007: orbital phase, rotating the binary axis
