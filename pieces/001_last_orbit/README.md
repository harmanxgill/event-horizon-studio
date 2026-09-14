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

### v006 - beamed rings

v005 put one cosine on each ring. A second cosine of the same order would only
collapse back into the first, so v006 modulates with a factor that is not a
single harmonic.

Each hole carries its material around the orbit, and the side sweeping forward
is brighter. Writing `theta_v` for the orbital direction in a hole's own frame,

```text
D(theta) = 1 / (1 - B cos(theta - theta_v))
N(theta) = D(theta)^p / <D^p>
```

`<D^p>` is the average of `D^p` over a full turn, so `N` averages to `1`: the
beaming redistributes ring brightness without adding any, exactly as `W` does.
At the defaults `B = 0.28` and `p = 2` the bright arc is `3.16` times the dim
one, and unlike a cosine it is concentrated rather than spread.

Because the binary turns counter-clockwise, both holes have

```text
theta_v = -pi/2
```

in their own frames. One constant covers both, which is the same statement as
the symmetry below. The ring becomes

```text
F = exp(-s(r1 - r_ring)^2) W(theta1) N(theta1)
  + exp(-s(r2 - r_ring)^2) W(theta2) N(theta2)
```

`W` is even about `theta = 0` and `N` is even about `theta = -pi/2`, so the two
are orthogonal over a turn and their product still averages to exactly `1`.
Setting `B = 0` reproduces v005.

## Symmetry

v001 through v005 are all left-right symmetric, and the tests check it. v006 is
not, and should not be: a binary that turns has a handedness, and reflecting
the image reverses it. What survives is the half-turn:

```text
G(-x, -y) = G(x, y)
```

The rotation carries each hole onto the other and each velocity onto the
other's, so an equal-mass binary is symmetric under `rot180` whatever its
orbital phase. The tests assert that from v006 on, and assert that mirror
symmetry is genuinely gone.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v006_beamed_rings.py
```

Push the beaming harder, or turn it off to recover v005:

```bash
python pieces/001_last_orbit/experiments/v006_beamed_rings.py --beta 0.5 --exponent 3
python pieces/001_last_orbit/experiments/v006_beamed_rings.py --beta 0 --anisotropy 0.35
```

### v007 - structured light

v005 added the `m = 1` term and v006 a beaming factor. v007 adds a harmonic of
arbitrary order, so the light around each hole breaks into `m` lobes:

```text
C(theta) = 1 + c cos(m theta)
```

`theta = 0` still points at the companion, so one lobe always faces across the
gap. The default `m = 4` keeps each ring legible while the structure is
unmistakable; `m = 3` gives sweeping arcs instead, and `m >= 5` breaks the ring
into separate beads.

### Keeping the modulation brightness-neutral

Each factor so far averages to `1` over a turn, so none of them changes total
ring brightness. That stops being automatic once the harmonic is added. `D^p`
has a component at every order, so `cos(m theta)` is not orthogonal to it, and
the product of the three drifts away from unit mean by order `1%` depending on
`m`. Rather than choose `m` to make the drift small, v007 normalises the whole
angular profile once:

```text
P(theta) = W(theta) C(theta) D(theta)^p
R(theta) = P(theta) / <P>
```

`<P>` is the average of `P` over a full turn. `R` then averages to exactly `1`
for every order and every combination of `c`, `e`, `B` and `p`, and the earlier
per-factor normalisation of the beaming term is no longer needed: `D^p` enters
raw as `doppler_factor`. Setting `c = 0` reproduces v006.

The ring is

```text
F = exp(-s(r1 - r_ring)^2) R(theta1) + exp(-s(r2 - r_ring)^2) R(theta2)
```

Both holes take the same `R`, and `theta1(P) = theta2(-P)`, so any angular
profile whatsoever leaves the half-turn symmetry of v006 intact.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v007_structured_light.py
```

Change the order, or fall back to v006:

```bash
python pieces/001_last_orbit/experiments/v007_structured_light.py --order 3
python pieces/001_last_orbit/experiments/v007_structured_light.py --order 6 --harmonic 0.5
python pieces/001_last_orbit/experiments/v007_structured_light.py --harmonic 0
```

### v008 - coupled radius

Every angular profile so far is evaluated at `theta` alone, so the lobes of
v007 sit at the same angle at every radius and point straight out from each
hole. v008 couples the two coordinates by shifting the angle with radius:

```text
phi(r, theta) = theta + q (r - r_ring)
R(theta) -> R(phi(r, theta))
```

The shift is zero on the ring itself and grows linearly on either side, so a
lobe leans one way inside the ring and the other way outside it. The straight
spokes become arcs.

The strength `q` has a natural scale. The ring is a Gaussian of width
`1 / sqrt(s)` and the lobes repeat every `2 pi / m`, so asking the pattern to
shear by half a lobe across one ring width fixes

```text
q = pi sqrt(s) / m
```

which is `7.02` at the defaults. Smaller values bend the lobes without
detaching them; around `16` each arc wraps far enough to overlap its
neighbour. `q = 0` reproduces v007.

Because `phi` only rotates the profile at fixed `r`, `R(phi)` still averages to
exactly `1` around every circle, so the coupling bends the light without
brightening or dimming any radius. And `r1(P) = r2(-P)` alongside
`theta1(P) = theta2(-P)`, so the half-turn symmetry survives unchanged.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v008_coupled_radius.py
```

Bend it less, wind it much further, or fall back to v007:

```bash
python pieces/001_last_orbit/experiments/v008_coupled_radius.py --twist 4
python pieces/001_last_orbit/experiments/v008_coupled_radius.py --twist 16
python pieces/001_last_orbit/experiments/v008_coupled_radius.py --twist 0
```

Possible next versions:

- v009: disk distortion toward the companion
- v010: orbital phase, rotating the binary axis
