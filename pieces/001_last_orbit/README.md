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

### v009 - logarithmic spiral

v008 bends the lobes, but not into a spiral. Its shift is linear in radius, and
a constant-phase curve of `theta + q(r - r_ring)` has

```text
tan(pitch) = 1 / (q r)
```

so the arms are shallow far out and steep close in. Measured at the v008
defaults the pitch runs from `43.6` degrees at `r = 0.15` to `14.6` degrees at
`r = 0.55`: a curve that is bent, but not a spiral.

A logarithmic spiral is the curve that crosses every radius at the same angle.
Writing it as `r = r_ring exp(theta tan(psi))` and solving for the phase,

```text
phi(r, theta) = theta - ln(r / r_ring) / tan(psi)
```

Now `tan(pitch) = tan(psi)` at every radius, with no dependence on `r` at all.
That self-similarity is what makes the arms read as arms: each one keeps its
character as it winds outward instead of flattening.

`r` appears inside a logarithm, so the phase diverges at the centre. The radius
is softened the same way `equations.py` softens its inverse fields:

```text
r_soft = sqrt(r^2 + e^2)
```

with `e = 0.02`, far inside the horizon, so the guard never touches anything
visible.

The pitch has the same natural scale as v008's twist. Across one ring width the
logarithmic span is `1 / (sqrt(s) r_ring)`, and asking the arms to wind half a
lobe over that span fixes

```text
tan(psi) = m / (pi sqrt(s) r_ring)
```

which is `29.7` degrees at the defaults. Shallower angles wind tighter; at
`psi = 90` degrees the winding vanishes and v007 comes back.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v009_log_spiral.py
```

Wind it tighter, open it out, or unwind it entirely:

```bash
python pieces/001_last_orbit/experiments/v009_log_spiral.py --pitch-degrees 15
python pieces/001_last_orbit/experiments/v009_log_spiral.py --pitch-degrees 50
python pieces/001_last_orbit/experiments/v009_log_spiral.py --pitch-degrees 90
```

### v010 - spiral radial decay

Each hole's spiral field gains an exponential falloff in its own radius:

```text
S_i -> S_i exp(-L r_i)
```

`L` is the new parameter, `2.0` by default, and `L = 0` reproduces v009
exactly. The halo is untouched: the decay multiplies the ring and arm term
only.

### What the decay actually does

The arms were never unbounded. `S_i` carries the ring envelope
`exp(-s(r - r_ring)^2)`, which at the defaults is already `0.0067` of its peak
at `r = 0.5` and `1e-4` at `r = 0.6`. A Gaussian falls faster than any
exponential, so `exp(-L r)` cannot be what confines the arms; they were
confined before it was added.

What `L` does instead is reshape the envelope. Multiplying a Gaussian by a
falling exponential gives another Gaussian of the same width, shifted inward:

```text
exp(-s(r - r_ring)^2) exp(-L r) = exp(-s(r - r_ring + L/(2s))^2) k
```

so the arms peak at `r_ring - L/(2s)`, which is `0.237` at `L = 2` and `0.219`
at `L = 5`, and the constant `k` dims the whole field. The visible effects are
therefore an inward pull, a tilt that favours the inner side of each arm over
the outer, and an overall darkening: peak field falls from `2.32` at `L = 0` to
`1.45` at `L = 2` and `0.76` at `L = 5`, and clipping from `7.4%` to `2.4%` to
nothing.

The term that genuinely reaches the edge of the frame is the halo, which falls
off as `exp(-b(r - r_glow))` with `b = 3.5` and is still at `0.016` of its peak
in the corners. Applying the decay there as well would be the change that makes
structure vanish with distance in the sense the ring envelope already handles.

Render it with:

```bash
python pieces/001_last_orbit/experiments/v010_spiral_decay.py
```

Decay harder, or switch it off to recover v009:

```bash
python pieces/001_last_orbit/experiments/v010_spiral_decay.py --decay 5
python pieces/001_last_orbit/experiments/v010_spiral_decay.py --decay 0
```

### v011 - shared orbital phase

One parameter now drives both holes. With `p` in `[0, 2 pi)`,

```text
theta1~ = theta1 - p
theta2~ = theta2 - p
```

and every angular term downstream reads `theta~` instead of `theta`: the
anisotropy, the harmonic, the beaming offset and the spiral winding all turn
together. `p = 0` reproduces v010 exactly.

Written against the plain angles the second line carries an extra half turn,

```text
theta2~ = atan2(y, x - a) - p - pi
```

because `theta2` already includes that `-pi`. It is the offset introduced in
v005 to make `theta = 0` point at the companion for both holes, and it is
exactly what lets a single `p` serve the pair.

### Consequences

The field is `2 pi` periodic in `p`, and the half-turn symmetry holds at every
phase: subtracting the same `p` from both frames preserves
`theta1(P) = theta2(-P)`, so the pair rotates as one object rather than two.

Total brightness is unchanged by the phase to about `5e-7` relative, inherited
from v007 normalising the angular profile over a full turn: rotating a profile
cannot change its mean. The residual is the `4096` sample circular mean, not
the phase.

`atan2` is undefined at each hole's own centre, where numpy returns `0`. An
odd-sized grid samples those two points exactly and the raw angle arrays
disagree there, but both lie at `r = 0`, far inside `r_h = 0.14`, so the
silhouette masks them and the rendered field is unaffected.

The holes themselves do not move: `p` turns the disks in place while the
centres stay at `(-a, 0)` and `(a, 0)`. Rotating the binary axis as well is the
complementary change, and `equations.py` already carries that form as
`orbit_phase`.

Render one phase, or the four-panel series:

```bash
python pieces/001_last_orbit/experiments/v011_orbital_phase.py --phase-degrees 90
python pieces/001_last_orbit/experiments/v011_orbital_phase.py --series
```

### v012 - companion-directed distortion

Each hole's disk stops being round. With `e` the distortion strength,

```text
d(theta) = 1 + e cos(theta)
r1' = r1 d(theta1),   r2' = r2 d(theta2)
```

and the disk and spiral terms read `r'` in place of `r`: the ring envelope, the
logarithmic winding and the radial decay all see the distorted radius. Written
against the plain angles this is the pair

```text
d1 = 1 + e cos(atan2(y, x + a)),   d2 = 1 - e cos(atan2(y, x - a))
```

the sign flip again being the `-pi` that `theta2` already carries.

The distortion uses the unphased angles. The companion sits in a fixed
direction because the centres do not move, so the stretch should not turn with
the orbital phase of v011.

### Which way it stretches

The ring is wherever `r' = r_ring`, so it sits at

```text
r = r_ring / (1 + e cos(theta))
```

With `e > 0` that is *smaller* toward the companion and larger away from it:
the disk is pressed in on the facing side and bulges outward, and the gap
between the holes empties. Stretching toward the companion, which is what this
version is for, is `e < 0`. The default is `e = -0.30`, which puts the ring at
`0.357` toward the companion against `0.192` away, and draws both disks into
the bridge across the middle.

The horizons are untouched. They read the true `r1` and `r2`, so the two black
disks stay exactly circular at any `e`: measured around a full turn their edge
varies by under three pixels and does not move when `e` changes. The halo reads
the true radii too, so the diffuse outer glow stays round while the disks
deform inside it.

Render it, flip the stretch, or drop back to v011:

```bash
python pieces/001_last_orbit/experiments/v012_companion_distortion.py
python pieces/001_last_orbit/experiments/v012_companion_distortion.py --distortion 0.30
python pieces/001_last_orbit/experiments/v012_companion_distortion.py --distortion 0
```

### v013 - binary interaction field

A term that belongs to the pair rather than to either hole:

```text
I(x, y) = exp(-A (r1 - r2)^2) exp(-B (r1 + r2))
```

added to the luminous terms before the horizons are cut out, so the composition
becomes `(F + A_halo + I)(1 - S)`. `I` is a function of `r1` and `r2` only, and
symmetric under exchanging them, so it is the first term in the piece that is
identical for both objects instead of being summed over them.

The two exponentials do different jobs. `r1 - r2` vanishes on the perpendicular
bisector, so the first picks out the points where the two holes are equidistant.
`r1 + r2` is at least `2a` everywhere, with equality only on the segment joining
the centres, so the second falls away from the pair.

### Normalisation and the wedge

Because `r1 + r2 >= 2a`, subtracting that floor makes the second factor at most
`1` and puts the maximum of `I` at the midpoint with value exactly `s`:

```text
I = s exp(-A (r1 - r2)^2) exp(-B (r1 + r2 - 2a))
```

so the strength parameter is the peak brightness rather than an arbitrary
scale. Measured, `I` peaks at the origin at `s` and never exceeds it.

The confinement term matters more than the bisector picture suggests. The level
sets of `r1 - r2` are hyperbolae with foci at the two centres, and they
asymptote to straight lines through the origin, so the first factor alone does
not select a strip of fixed width: it selects a wedge that keeps widening.
Along the bisector the balance term stays at `1.0` forever, and at `(0.3, 1.0)`
it is still `0.38`. With the confinement term the same profile is at `34%` of
peak by `y = 0.4` and `2.6%` by `y = 0.9`.

Along the binary axis the balance term falls to under `5%` of peak by
`|x| = 0.2`, which is what keeps the bright patch between the holes narrow.

Render it, widen or tighten the wedge, or switch it off:

```bash
python pieces/001_last_orbit/experiments/v013_interaction_field.py
python pieces/001_last_orbit/experiments/v013_interaction_field.py --alpha-i 8 --beta-i 1.5
python pieces/001_last_orbit/experiments/v013_interaction_field.py --strength 0
```

### v014 - tidal bridge

The interaction term of v013 is shaped into a bar joining the two holes:

```text
T  = exp(-A_t y^2) exp(-B_t x^4) I(x, y)
T' = T [1 + n_t cos(k_t x + p_t)]
```

and `T'` replaces `I` in the composition, so the field is
`(F + A_halo + T')(1 - S)`. The `y^2` factor flattens the interaction onto the
binary axis; the `x^4` factor is what lets it stay bright all the way across
and then stop.

A quartic is flat-topped where a Gaussian is already curving. Compared at the
same half-width, `exp(-B x^4)` sits above `exp(-g x^2)` everywhere inside and
below it everywhere outside: a plateau with a shoulder rather than a peak. That
is the difference between a bar and a blob. Note this only holds at matched
half-width; at the same coefficient the quartic is the shallower of the two
until `x = 1`.

### Two parameters had to move

`I` as tuned in v013 cannot become a bridge. With `A_i = 25` the balance term
is `exp(-4 A_i x^2)` along the axis, which is `2e-6` of its peak by the time it
reaches a hole at `x = a`, so the `x^4` factor has nothing left to shape.
v014 therefore widens it to `A_i = 1.5`, which puts the half-width at `0.29`
against `a = 0.36`, and raises `A_t` to `120` to thin the bar vertically. The
result measures `0.29` wide against `0.084` tall, an aspect of about `3.5`.

The internal structure needs a matching wavenumber. At `k_t = 17.5` less than
one period fits across the bar and the envelope's decay erases the ripple
entirely, leaving no local minima at all. At `k_t = 32` with `n_t = 0.5` the
bar breaks into five knots, with dips at `x = +-0.099` and `+-0.302`.

The strength is raised to `1.0`. At v013's `0.35` the bridge adds `0.53` at the
midpoint where the rest of the field is already at `1.98`, and disappears into
it. At `1.0` nothing saturates to white and the clipped area only moves from
`5.8%` to `6.6%`, because the bar sits in a region the warm ramp has headroom
for.

`T'` alone is symmetric in both axes. The half-turn symmetry of the whole field
is unchanged.

Render it, slide the knots, or drop the bridge:

```bash
python pieces/001_last_orbit/experiments/v014_tidal_bridge.py
python pieces/001_last_orbit/experiments/v014_tidal_bridge.py --bridge-phase 3.14159
python pieces/001_last_orbit/experiments/v014_tidal_bridge.py --eta-t 0 --strength 0.35
```

### v015 - tidal tails

Material thrown outward from each hole, added to the composition alongside the
bridge:

```text
Q1 = exp(-A_q (r1 - R_q - c_q t1)^2) exp(-B_q r1)
Q2 = exp(-A_q (r2 - R_q + c_q t2)^2) exp(-B_q r2)
Q  = Q1 + Q2
```

The ridge of each Gaussian is `r = R_q +- c_q t`, an Archimedean spiral: radius
growing linearly with angle, unlike v009's logarithmic winding inside the
disks. `B_q` fades the arm with distance so it thins out rather than running to
the frame edge.

These use the plain angles, `t2 = atan2(y, x - a)`, not the companion-anchored
`theta2` the rest of the piece uses, so the written formula is exactly the one
above.

### This is the first version with no symmetry

Every version from v006 to v014 satisfies `G(-x, -y) = G(x, y)`. `Q` does not,
and the opposite signs are why. Under a half turn `r1 -> r2` and
`t2(-P) = t1(P) + pi`, so

```text
Q2(-P) = exp(-A_q (r1 - (R_q - c_q pi) + c_q t1)^2) exp(-B_q r1)
```

which differs from `Q1(P)` in the sign of `c_q t1` *and* by a shift of `c_q pi`
in the base radius. Measured, the half-turn residual on `Q` is `87%` of its own
peak. Matching the signs does not fix it either: that leaves the `c_q pi` shift
and the residual rises to `100%`.

The form that does restore it exactly is the same sign together with the
companion-anchored angles, since those satisfy `theta1(P) = theta2(-P)` with no
offset:

```text
Q = q(r1, theta1) + q(r2, theta2),   q(r, t) = exp(-A_q (r - R_q - c_q t)^2) exp(-B_q r)
```

which measures a residual of `6e-14`. v015 keeps the asymmetric form as
specified; the symmetric one is a one-line change if the pinwheel is wanted
back.

### The branch cut

`r = R_q + c_q t` needs a continuous angle, but `atan2` jumps at `+-pi`, and on
the far side of the jump the ridge radius `R_q - c_q pi` is negative, so no arm
exists there. The arm is therefore sliced along a straight ray rather than
ending: an `8%` of peak step across a single pixel, clearly visible as a
horizontal seam to the left of the frame.

A taper closes it:

```text
w(t) = 1 - exp(-((pi - |t|) / u)^2)
```

zero on the cut and above `0.99` once `|t|` is more than `1.5` radians from it,
so it fades the far tip of each arm and leaves the rest alone. The seam goes to
zero and the peak moves from `0.5970` to `0.5966`. `--taper 0` restores the
literal formula and the seam with it.

Render it, lengthen the arms, or drop them:

```bash
python pieces/001_last_orbit/experiments/v015_tidal_tails.py
python pieces/001_last_orbit/experiments/v015_tidal_tails.py --c-q 0.4 --beta-q 1.0
python pieces/001_last_orbit/experiments/v015_tidal_tails.py --tails 0
```

### v016 - global potential

A field belonging to the binary as a whole, standing in for its gravitational
potential:

```text
Phi = -M1 / (r1 + e) - M2 / (r2 + e),   M1 = M2 = 1
P   = 1 - exp(-k |Phi|)
```

`e = 0.05` keeps `Phi` finite at the centres, where it would otherwise diverge.
`Phi` is negative everywhere, so `|Phi|` is largest at the holes and smallest
far out, and `P` maps that onto `(0, 1)`: deepest where the binary is, shallow
at the edges of the frame.

The composition becomes

```text
G = (S1 + S2 + A_halo + L_t T' + L_q Q + L_p P)(1 - S)
```

with `L_p = 0.25`. `A_halo` is v004's outer glow, which is not in the written
sum but has been part of `S1 + S2`'s neighbourhood since then.

### Added, not multiplied

The specification says `P` should modulate the total luminosity, which reads as
a product, but the intensity formula lists `+ L_p P`. v016 follows the formula.
The two behave very differently here, because `P` does not reach zero anywhere
inside the frame:

```text
P at the midpoint   0.519
P on a ring         0.496
P at the corner     0.153
```

so as a multiplier it would dim the corners to `0.20` of their value and act as
a vignette, while as an addend it raises them. Measured, the corner background
goes from `0.027` to `0.076`, which is `8` to `21` in the red channel: a faint
warm pedestal rather than pure black. Lowering `k` sharpens the contrast, from
`1.95x` midpoint-to-corner at `k = 0.6` up to `3.38x` at `k = 0.15`, which is
why `0.15` is the default.

The pedestal is added inside the horizon mask, so the two black disks stay
exactly black. Every pixel the silhouette zeroes is still zero.

Render it, deepen the pedestal, or drop it:

```bash
python pieces/001_last_orbit/experiments/v016_global_potential.py
python pieces/001_last_orbit/experiments/v016_global_potential.py --kappa-phi 0.4 --lambda-p 0.4
python pieces/001_last_orbit/experiments/v016_global_potential.py --lambda-p 0
```

### v017 - outgoing wave phase

The first structure measured from the centre of the whole binary rather than
from either hole:

```text
rho   = sqrt(x^2 + y^2)
Theta = atan2(y, x)
```

and a phase that travels outward as the orbit advances:

```text
Psi = k_g rho - w_g p
W0  = cos(Psi)
```

`p` is v011's orbital phase, so the wave and the disks are driven by the same
parameter. `w_g = 2` because a binary radiates at twice its orbital frequency.

A surface of constant phase satisfies `rho = (Psi + w_g p) / k_g`, so it moves
outward at `w_g / k_g` per radian of orbit. Measured at the defaults that is
`0.0714`, and stepping the phase by `0.2`, `0.4` and `0.6` moves the crests by
exactly that rate. The wavelength is `2 pi / k_g = 0.224`, giving about six
rings across the frame, and the pattern repeats every `2 pi / w_g` in `p`.

`Theta` is computed but does not appear in `Psi`, so `W0` is a set of perfect
concentric rings with no angular structure at all. That is the point: the
angular dependence is what v018 adds, and this version exists to establish the
coordinates and the travelling phase underneath it.

### Rendered weakly on purpose

`W0` is a cosine, so it is signed, and it enters as `+ L_w W0` with `L_w = 0.05`.
The rings therefore brighten and darken the field by at most `0.05` either way,
under `15%` of the local brightness across the lit area. Nothing is driven
negative: the potential pedestal from v016 sits above the wave's trough
everywhere outside the horizons, and inside them the silhouette zeroes it.

Render it, or raise the amplitude to see the rings clearly:

```bash
python pieces/001_last_orbit/experiments/v017_outgoing_wave.py
python pieces/001_last_orbit/experiments/v017_outgoing_wave.py --lambda-w 0.25
python pieces/001_last_orbit/experiments/v017_outgoing_wave.py --phase-degrees 45
```

### v018 - quadrupolar field

v017's rings gain the angular structure a binary actually radiates with:

```text
W = cos(2 Theta - k_g rho + w_g p) / (1 + g_w rho)
```

The `2 Theta` is the whole point. At any fixed radius the wave has exactly two
crests instead of being constant around the circle, and a ridge satisfies
`2 Theta - k_g rho = const`, so the angle advances at `k_g / 2` with radius: a
two-armed spiral rather than concentric rings. The amplitude `1 / (1 + g_w rho)`
falls from `1.0` at the centre to `0.26` at the corners with `g_w = 2`.

The test that v017's phase had no angular dependence now has a counterpart
asserting this one has exactly two lobes at every radius.

### Multiplied, and replacing v017

The specification is explicit here where v016's was not:

```text
F18 = F16 [1 + e_w W]
```

so `W` scales the intensity rather than adding to it, and it is `F16` being
scaled, not `F17`. v017's additive `L_w W0` term is therefore gone rather than
stacked underneath: that version existed to establish the coordinates and the
travelling phase, and this one supersedes it. Setting `e_w = 0` gives back v016
exactly, not v017.

The difference between the two forms is visible. v017 added a signed cosine, so
its rings appeared everywhere including the dark corners. v018 multiplies, so
the wave can only shape light that is already there: where the field is below
`1e-4` it stays below `1e-4`, and the two-armed pattern reads as a slow banding
across the halo rather than rings on black.

`e_w = 0.10` keeps it small, as asked. The modulation is bounded by `+-e_w`
exactly, since `|W| <= 1`, and across the lit area it changes brightness by
`9.8%` at most and `2.7%` typically. The horizons are untouched: the mask is
applied after the modulation, so both black disks stay exactly black.

`W` is itself half-turn symmetric, because `cos(2 Theta)` has period `pi`. It
does not restore the symmetry the tails broke in v015, but it does not add to
the breakage either.

Render it, or push the wave until it is obvious:

```bash
python pieces/001_last_orbit/experiments/v018_quadrupolar_field.py
python pieces/001_last_orbit/experiments/v018_quadrupolar_field.py --epsilon-w 0.4
python pieces/001_last_orbit/experiments/v018_quadrupolar_field.py --gamma-w 0.3 --k-g 14
```

### v019 - orbital velocity field

A signed field marking which side of each disk is approaching and which is
receding:

```text
V1 = cos(t1 - p),   V2 = -cos(t2 - p)
V  = S1 V1 + S2 V2
```

Written against the plain angles the second term carries a minus sign; against
the companion-anchored `theta2` it does not, because `theta2` already includes
the `-pi`. Both reduce to `V = S1 cos(theta1~) + S2 cos(theta2~)`, where
`theta~` is v011's phased angle. A test checks the implementation against the
plain-angle form at three phases.

`V` needs each hole's disk separately, so `ring_field` is split into
`ring_components`, returning `(S1, S2)`; `ring_field` remains as their sum and
is checked to agree with v018's.

### Shape of the field

`|V| <= S1 + S2` everywhere, so `V` lives only where the disks do. At `p = 0`
it is positive between the holes, where each disk faces its companion, and
negative on the outer flanks. Advancing `p` rotates the approaching side, with
period `2 pi`.

The sign change is a smooth crossing: the largest step between neighbouring
pixels is `3%` of the peak. It can look like a hard edge in a linear rendering,
because `V` spans about two orders of magnitude, from `1.68` at the midpoint to
under `0.01` near the crossings. The signed diagnostic therefore scales on the
90th percentile of `|V|` rather than the maximum.

### How it enters the image

The specification defines `V` without saying how to use it. v019 adds it as a
small signed term, `+ L_v V` with `L_v = 0.08`, inside the quadrupole
modulation and the horizon mask. That brightens the approaching side and dims
the receding side by at most about `6%`, and nothing goes negative. `L_v = 0`
reproduces v018 exactly.

A signed approaching/receding field is the natural input for colour, blue on
one side and red on the other, rather than for brightness. That is not done
here, since the piece is still rendered through a single warm ramp, but
`--velocity` renders the field itself that way:

```bash
python pieces/001_last_orbit/experiments/v019_velocity_field.py
python pieces/001_last_orbit/experiments/v019_velocity_field.py --velocity
python pieces/001_last_orbit/experiments/v019_velocity_field.py --lambda-v 0.3
```

### v020 - Doppler-inspired luminosity

v019's signed velocity becomes a brightness factor on each disk:

```text
D1 = (1 + B_d V1)^p_d,   D2 = (1 + B_d V2)^p_d
S1' = D1 S1,             S2' = D2 S2
```

This is Doppler-*inspired*. The power-law form echoes how relativistic beaming
brightens approaching material, but nothing here traces rays, transforms
frequencies, or uses a physical velocity; `V` is a cosine of the phased angle
and `B_d` is a free contrast parameter.

The parameters are `beta_d` and `p_d` because `beta` and `exponent` already
belong to v006's beaming inside the ring profile. The two effects are
different: v006's is fixed along each hole's orbital direction and normalised
to add no light, while this one follows the phased angle and is not normalised.

The composition becomes

```text
G = (S1' + S2' + A_halo + L_t T' + L_q Q + L_p P) [1 + e_w W] (1 - S)
```

which is the written `F20` with v004's halo, v018's quadrupole modulation and
v003's horizon mask kept from earlier versions. v019's additive `L_v V` term is
gone, since `D` now carries the velocity: `B_d = 0` or `p_d = 0` gives back v018
exactly, not v019.

### Numbers

`|V_i| <= 1` and `B_d < 1`, so `1 + B_d V` is always positive and the factor
never flips sign. At the defaults `B_d = 0.3`, `p_d = 3`:

```text
approaching  (1.3)^3 = 2.20
receding     (0.7)^3 = 0.34     contrast 6.4x
```

Unlike the angular profile of v007 this is not brightness-neutral. Averaged
around a turn, the odd powers of `cos` vanish and

```text
<(1 + B cos t)^3> = 1 + 1.5 B^2
```

so the disks gain `13.5%` of their light at `B_d = 0.3`, and `37.5%` at `0.5`.

At `p = 0` the approaching side is the side facing the companion, so the
boost lands on material that already feeds the bridge. The peak field rises
from `4.03` to `6.22` and clipping from `8.4%` to `9.6%`, which is why the
centre of the frame now reads as one hot region. Advancing `--phase-degrees`
moves the approaching side off the bridge.

Render it, sharpen the contrast, or turn it off:

```bash
python pieces/001_last_orbit/experiments/v020_doppler_luminosity.py
python pieces/001_last_orbit/experiments/v020_doppler_luminosity.py --phase-degrees 90
python pieces/001_last_orbit/experiments/v020_doppler_luminosity.py --beta-d 0
```

### v021 - nonlinear intensity

By v020 the raw field has a `47x` spread between its 10th and 99.9th
percentiles, peaking at `6.26`. Rendered linearly, the red channel sits flat at
`255` over `9.9%` of the lit area, while only `0.07%` of pixels ever reach
white. v021 compresses the field into `[0, 1)` before colouring it:

```text
exponential   L = 1 - exp(-g F)
hill          L = F^p / (F^p + k)
```

Both fix `0` at `0`, so the horizons stay black, and both rise monotonically
toward `1`. The Hill form reaches exactly `1/2` at `F = k^(1/p)`, which is what
makes it the more controllable of the two.

### The colour ramp had to change

The ramp in use since v001 maps a field value `f` to
`(1.10 f, 0.58 f, 0.18 f)`, clipped. At `f = 1` that is `(255, 148, 46)`, which is
orange. The white in earlier renders only appeared because the raw field
overshot `1` far enough for every channel to clip, so a compressed field in
`[0, 1)` fed to that ramp could never whiten anything. That defeats the point of
the version.

v021 colours `L` with a ramp that reaches white at `L = 1` instead:

```text
(L, L^1.5, L^2.5)
```

Red rises first, then green, then blue, so faint light stays deep amber and
bright light passes through yellow to white. All three channels are monotone
and ordered `R >= G >= B` at every level. Mid-tones come out browner and less
saturated than under the old ramp.

### Defaults and measurements

`g = 1.4` was chosen from the field's own distribution, placing the median at
`L = 0.30` and the 99th percentile at `0.99`:

```text
                     near-white   red flat-clipped   faint-half red levels
v020, linear ramp       0.10%          9.87%                55
exponential             0.98%          0.45%                56
hill (p 1.5, k 0.56)    0.00%          0.00%                42
```

The exponential form whitens ten times as much of the frame, removes almost
all of the flat clipping, and keeps the faint half's tonal range while making
it brighter on average. The Hill form at these settings never reaches white,
since its 99th percentile only maps to `0.92`, and it darkens the faint half; a
smaller `k` pushes it brighter.

`--tone linear` skips the compression and uses the old ramp, reproducing v020
exactly.

```bash
python pieces/001_last_orbit/experiments/v021_nonlinear_intensity.py
python pieces/001_last_orbit/experiments/v021_nonlinear_intensity.py --tone hill --k-l 0.2
python pieces/001_last_orbit/experiments/v021_nonlinear_intensity.py --gamma-l 0.7
python pieces/001_last_orbit/experiments/v021_nonlinear_intensity.py --tone linear
```

### v022 - RGB equations

Colour is now a set of equations in the compressed intensity `L` of v021 and
the quadrupole wave `W` of v018:

```text
R = 1 - exp(-4 L)
G = (1 - exp(-2 L))   (1 + 0.05 W)
B = (1 - exp(-0.7 L)) (1 + 0.10 W)
C = clamp([R, G, B], 0, 1)
```

Every pixel of the image is now the value of a written formula, from the
coordinates through the fields to the three channels.

The experiments never used a premade colormap: the v001 ramp and v021's ramp
were both per-channel formulas already. What changes here is that colour stops
being a fixed ramp bolted on at the end and becomes its own set of equations
with a field of their own feeding in. The only premade colormap left in the
repository is matplotlib's `magma`, in the original `render.py`.

The channel rates are `rate_r`, `rate_g` and `rate_b`, since `k_g` is already
the wave number, and the tints are `shift_g` and `shift_b`.

### What the equations do

For faint light each channel is close to linear, `R : G : B ~ 4 : 2 : 0.7`,
which is `1 : 0.500 : 0.175`. That is almost exactly the `1 : 0.527 : 0.164` of
the ramp the piece started with in v001, so the dim structure keeps its
original amber. The channels then saturate at different rates, red first and
blue last, so hue warms toward gold as `L` rises.

The brightest colour the equations can make is gold, not white. At `L = 1`

```text
(0.982, 0.865, 0.503)  ->  (250, 220, 128)
```

because `1 - exp(-0.7)` is only `0.50`. v021's ramp whitened the bridge; this
one keeps it gold. The channels stay ordered `R >= G >= B` everywhere.

The wave leaves red untouched and tints green by at most `5%` and blue by at
most `10%`: a faint cool-warm shimmer following the two-armed spiral, too small
to read as rings.

### Two corrections the first render needed

Taken at v021's settings, the equations washed the frame out. `L` is already a
compression of the raw field, `1 - exp(-1.4 F)`, and `R = 1 - exp(-4 L)`
compresses it a second time. Faint light is multiplied by about `4` on the way
through, so the dim background v016 left in the corners came out as tan rather
than near-black:

```text
                        corner luma   p99 / p5 contrast
v021                        13.5            17.1x
v022 at g = 1.4             58.0             3.5x
v022 at g = 0.25            12.4            13.0x
```

The fix belongs to the tone curve rather than the colour: the rate `g` in `L`
was chosen in v021 for a linear ramp, and v022 sets it to `0.25`, which puts the
corners back where v021 had them and restores most of the contrast. The colour
rates stay exactly as written. With less compression the brightest pixel in
the frame is now `L = 0.76`, which colours to `(243, 199, 105)`.

The first render also showed a small pinch at the exact centre of the frame.
`W = cos(2 Theta - k_g rho) / (1 + g_w rho)` has its largest amplitude at
`rho = 0`, which is exactly where `Theta` has no value, so the tint swung
through every angle within a couple of pixels: blue went from `116` to `141`
around a circle of radius `0.012`. The wave is now tapered at its core,

```text
W -> W (1 - exp(-(rho / 0.06)^2))
```

which is zero at the origin and leaves `W` unchanged to within `6e-10` beyond
`rho = 0.25`. The same swing shrinks to three levels. The taper applies
wherever `W` is used, including v018's intensity modulation, which had the same
singularity hidden under saturation until now.

Setting `--gamma-l 1.4 --core-w 0` reproduces v021's intensity exactly.

```bash
python pieces/001_last_orbit/experiments/v022_rgb_equations.py
python pieces/001_last_orbit/experiments/v022_rgb_equations.py --rate-b 2.5
python pieces/001_last_orbit/experiments/v022_rgb_equations.py --shift-g 0 --shift-b 0
python pieces/001_last_orbit/experiments/v022_rgb_equations.py --gamma-l 1.4 --core-w 0
```

`--rate-b 2.5` lets the brightest light approach white again; the last command
shows the washed-out, pinched version for comparison.

### v023 - mathematical background

No random stars. The empty space around the binary is a field too:

```text
B_bg = e_b exp(-g_b rho) [1 + n_b cos(k_b rho + m_b Theta)]
L'   = L + B_bg
```

`rho` and `Theta` are v017's coordinates about the centre of the binary, so the
background is an `m_b`-armed spiral fading slowly outward, with `m_b = 5`,
`k_b = 12`, `g_b = 0.5` and `n_b = 0.5`. Five arms keeps it distinct from the
two-armed quadrupole wave it sits under.

### Barely there

`e_b = 0.003`. Added to `L` and passed through the colour equations of v022,
the background changes no channel of any pixel by more than `3` levels out of
`255`. In the dark `16%` of the frame the typical change to red is `1` level,
on a base of about `21`; in the bright core it is at most `1`. Because the
colour equations are steepest near `L = 0` and flatten as they saturate, the
same small addition shows most in the darkest regions and all but vanishes in
the bright ones, which is where a background should live. It is invisible at a
glance; a difference image multiplied by forty shows the five arms clearly.

### Two choices in the construction

`m_b` must be an integer. `Theta` jumps from `pi` to `-pi` across the negative
`x` axis, and `cos(k_b rho + m_b Theta)` only agrees on both sides of that jump
when `m_b` is whole. A half-integer would draw a straight seam there, the same
failure as the tidal tails in v015, so a fractional `m_b` is rejected. At
`m_b = 5` the step across the cut is `6e-5`, no larger than the change between
neighbouring pixels.

The background sits behind the holes. It is multiplied by the same horizon mask
`(1 - S)` as everything else, so the two black disks stay black; even at a
background a hundred times stronger than the default, the horizons stay below
`0.01`.

```bash
python pieces/001_last_orbit/experiments/v023_mathematical_background.py
python pieces/001_last_orbit/experiments/v023_mathematical_background.py --epsilon-b 0.03
python pieces/001_last_orbit/experiments/v023_mathematical_background.py --epsilon-b 0
```

`--epsilon-b 0.03` makes the arms plainly visible, for checking what is there.

### v024 - fine structure

High-frequency detail, but only where there is already light. Each hole's
Doppler-scaled disk `S_i'` from v020 is multiplied by a structure factor:

```text
product   N_i = 1 + e_n sin(k_r r_i + m theta_i) sin(k_t theta_i)
log       N_i = 1 + e_n sin(k_r r_i + m theta_i + c ln(r_i + s))
S_i'' = S_i' N_i
```

The logarithmic form is the default; `--structure product` selects the other.
Defaults are `e_n = 0.35`, `k_r = 90`, `m = 24`, `k_t = 16`, `c = 6`, `s = 0.02`.

No procedural noise is involved. The product form crosses a spiral phase with
a purely angular one, which weaves the disks into a fine feathered lattice. The
log form adds `c ln(r + s)` to the phase, so the local radial frequency is
`k_r + c / (r + s)`: higher near the horizon than further out, `125` against
`100` between `r = 0.15` and `r = 0.6`, about `26%`. The result is continuous spiral fibres that
tighten toward each hole.

### Where it applies

Because `N_i` multiplies the disks and nothing else, the structure appears only
inside them. Where the disks carry no light it changes no pixel by more than
one level, and the corners of the frame not at all. The bridge, tails, halo and
background of earlier versions are untouched. Inside the lit disks the red
channel moves by about `5` levels on average and up to `29` at the brightest
fibres.

`r_i` and `theta_i` are the distorted radii of v012 and the phased angles of
v011, the same coordinates the disks are drawn in, so the fibres stretch toward
the companion and turn with the orbit along with the light they sit on.

`N_i` averages to `1` over a cycle, so the structure redistributes brightness
rather than adding it: mean intensity over the lit disks moves by well under
`1%`.

### Continuity and aliasing

`m` and `k_t` multiply an angle that jumps from `pi` to `-pi` on one side of
each hole, so both must be integers or the fibres tear along a straight line, as
the tails did in v015. Fractional values are rejected.

Frequencies this high can alias. The shortest wavelength of the structure is
`2 pi / |grad Psi|` for its phase `Psi`, and it is shortest at the inner edge of
each disk, where the angular term `m / r` is largest. Measured from the phase
gradient over the visible lit area, the shortest cycle is `17` pixels at
`1200x1200` and `8` pixels at `512x512`, so the fibres stay well clear of the
two-pixel limit even at small render sizes. Between the holes the two disks'
fibres overlap and cross; that interference is real superposition, not moiré.

```bash
python pieces/001_last_orbit/experiments/v024_fine_structure.py
python pieces/001_last_orbit/experiments/v024_fine_structure.py --structure product
python pieces/001_last_orbit/experiments/v024_fine_structure.py --c-n 20 --m-n 12
python pieces/001_last_orbit/experiments/v024_fine_structure.py --epsilon-n 0
```

### v025 - horizon suppression

The horizons are revisited last, and applied last:

```text
H_i = 1 / (1 + exp(-k_h (r_i - r_h)))
H   = H1 H2
L_final = H L'
```

`H_i` rises from `0` inside a horizon to `1` outside it, reaching exactly `1/2`
at `r_i = r_h`, and the product is dark wherever either hole is.

### Same shape, new place

Since v003 the horizons have been cut out with `1 - max(S1, S2)`, where `S_i`
is a logistic. That is the same function as `H1 H2` whenever the two horizons do
not overlap, and at a separation of `0.72` against a radius of `0.14` they are
far apart: the two agree everywhere to `2e-16`. What v025 changes is not the
shape of the mask but where in the pipeline it acts.

Before, the mask multiplied the raw intensity, and the result then went through
the compression `1 - exp(-g F)` of v021 and had the background of v023 added.
The visible edge was therefore a logistic bent by a nonlinear curve, with the
background masked separately. Now `L'` is built in full, background included,
and multiplied by `H` once at the very end. The edge that reaches the colour
equations is exactly the logistic above, which is what makes `k_h` a direct
control over it.

Nothing inside the horizons survives. `L'` there is not small, `0.161` at a
hole's centre, since the disks, potential and fine structure are all defined
at small radius, but `H` is below `1e-20` at the centre and the rendered disks
stay at most one level above black. The exponent is clipped like v003's, so
even `k_h = 1e6` evaluates without overflow.

### The edge is now measured in space, not pixels

The logistic's `10%` to `90%` transition spans `ln 81 / k_h` in coordinate
units. v003 instead tied its edge to the pixel spacing, so it looked the same at
every render size. `k_h` is a length scale in the plane, so the edge in pixels
now depends on resolution:

```text
k_h = 600    1200 px: 4.4 px    512 px: 1.9 px
k_h = 300    1200 px: 8.8 px    512 px: 3.7 px
k_h = 150    1200 px: 17.6 px   512 px: 7.5 px
```

The default `k_h = 600` reproduces v003's `4.4` pixel edge exactly at the
standard `1200x1200` size, so the full-size render keeps the edge it had. At
smaller sizes the edge is sharper in pixels than before. Away from the edge
nothing changes: beyond `r = 0.2` no pixel differs from v024 by a single level,
and the intensity differs only in the band `0.13 < r < 0.16`, by at most `0.02`.
Lower `k_h` gives a visibly soft, glowing rim.

```bash
python pieces/001_last_orbit/experiments/v025_horizon_suppression.py
python pieces/001_last_orbit/experiments/v025_horizon_suppression.py --k-h 80
python pieces/001_last_orbit/experiments/v025_horizon_suppression.py --k-h 60000
```

### v026 - final equation

No new effect. This version is editing: every term was switched off in turn,
and anything whose absence could not be seen was deleted.

```text
F = H [ D1 S1 N1 + D2 S2 N2 + A + T + Q + P ]
L = 1 - exp(-g F)
Pixel = 255 [ 1 - exp(-4 L),  1 - exp(-2 L),  1 - exp(-0.7 L) ]
```

`S_i` are the disks: a Gaussian ring about the distorted radius of v012, wound
into a logarithmic spiral (v009), shaped by the harmonic (v007) and beaming
(v006) profile, and faded by the radial decay of v010. `N_i` is the fine
structure of v024, `D_i` the Doppler-inspired factor of v020, `A` the outer
halo of v004, `T` the tidal bridge of v014, `Q` the tidal tails of v015, `P`
the potential glow of v016 and `H` the horizon suppression of v025.

### How the cuts were decided

Each of sixteen terms was removed from the full `1200x1200` render, one at a
time, and the change measured in eight-bit levels:

```text
term removed               mean   p99    max   pixels > 3 levels
background     (v023)      1.47     3      3        0.0%
wave tint      (v022)      0.73     5      8        3.1%
quadrupole     (v018)      1.37     5      6        6.1%
anisotropy     (v005)      0.86     8     11       10.9%
bridge         (v014)      0.71    20     81        3.2%
harmonic       (v007)      1.38    15     23       13.8%
fine structure (v024)      1.54    18     29       14.2%
  ... spiral, beaming, Doppler, decay, tails, distortion ...
potential      (v016)     13.43    25     29       94.9%
halo           (v004)     22.70    51     54       96.4%
```

Four were cut.

The background of v023 was designed to be seen only on close inspection, at
three levels. In the final equation it is added before compression rather than
after, which compresses it about four times harder: it then changes no pixel by
more than one level anywhere, and is gone.

The quadrupole wave `W` of v017 and v018 appeared twice, as `(1 + e_w W)` on the
intensity and as a tint in the colour. Removed together, the change is under
nine levels at the 99th percentile. The pattern is real, a clean two-armed
spiral in a tenfold-magnified difference image, but it is not visible in the
image itself. It does not carry the motion either: across a five degree step of
orbital phase it accounts for half a level on average and three at most, against
thirty-two levels of change from everything else. With `W` gone, the core taper
added in v022 to repair its singularity at the origin has nothing to repair and
goes too.

The anisotropy `1 + e cos theta` of v005 was the one borderline cut. Its change
sits in the brightest part of the bridge, where twenty levels are hardest to
see, and it duplicates what the Doppler factor of v020 now does: both are a
cosine peaked toward the companion. Removing the background, `W` and the
anisotropy together moves the frame by `2.0` levels on average and `14` at the
99th percentile, and side by side the two renders are not distinguishable.

A second pass removed each survivor from the pruned image. Every one still
matters, the smallest being the bridge at `22` levels in the 99th percentile
and `84` at its brightest knot, so nothing further was cut.

The bridge and the harmonic look small on average, but their change is
concentrated: the bridge is a narrow bar of up to `81` levels, and averages
across a mostly empty frame say little about that.

### Differences from the equation as written

The halo `A` was not in the proposed final equation but is the single largest
term: removing it changes `96%` of the frame by `23` levels on average. It stays.

`H` now multiplies the intensity before compression, as written, where v025
applied it after. The two orderings differ by about one level on average and
twelve at most, all in the thin band at the horizon edge.

### Deleted code

Beyond the four terms, the file drops everything that only served them or had
been left behind: the Hill and linear tone modes, the product form of the fine
structure, the velocity diagnostic, `ring_field`, `silhouette_field`, an unused
colour ramp and import, and four stray parameters that an earlier edit had
attached to `doppler_factor_inspired` by mistake. The experiment goes from
`1073` lines to `607`, and from `67` command-line options to `48`.

The surviving functions are copied unchanged from v025, and the result is
verified to be bit-for-bit identical to v025 rendered with the four terms
switched off.

```bash
python pieces/001_last_orbit/experiments/v026_final_equation.py
python pieces/001_last_orbit/experiments/v026_final_equation.py --series
```

## Finishing

v026 is the preserved late-stage version. Judged against it, the image still
read as two black circles on a repeating ripple, rather than as a binary black
hole merger whose mathematics shows on closer inspection. The piece is finished
in four more steps, each a single idea: the horizons act on their surroundings
(v027), the ripples lose their regularity (v028), one strong asymmetry (v029),
and tone and composition only (v030). No stars, flares, noise or realistic
textures are added at any point.

### v027 - horizon lensing

In v026 the horizons were clean circles sitting on top of the pattern. Now the
holes bend the plane around them. Every luminous term is evaluated at the image
of each point under the softened binary point-lens equation,

```text
beta(p) = p - sum_i  r_E^2 (p - c_i) / (|p - c_i|^2 + s^2)
```

with `r_E = 0.12` and `s = 0.02`, and weighted by the lens magnification

```text
mu = 1 / det J(beta)          F = H(p) [ ... ](beta)  mu^q
```

with `q = 1.5`. The horizon suppression `H` still uses the true position `p`,
so both interiors stay black and exactly circular.

One equation gives all three effects asked for. Structure crowds toward each
horizon, because the map compresses radial spacing by `1 + r_E^2 / r^2`: nearly
double at the rim. Patterns bend around the holes, and very slightly around the
binary as a whole. And light intensifies at the boundary, since `mu` peaks at
about `2.1` there and returns to `1` away from the holes.

The warp and the magnification are separate for a reason. On its own the warp
does not brighten the rim; it dims it, to `0.86` of v026. It pulls the inner
part of each disk out from behind the horizon, and that part is dimmer than the
ring. The magnification is what makes the rim glow: mean brightness in the band
just outside the horizon rises to `1.33` times v026 at `1200x1200`.

`det J` is computed analytically rather than by differencing neighbouring
pixels. It agrees with finite differences to `2e-4`, and it keeps every term a
pure function of position, so rendering in strips stays bit-for-bit identical to
a single pass.

### The limit on r_E

The softened map folds, with `det J` passing through zero, on a curve of radius
close to `r_E`. While that curve lies inside the horizon it is hidden. At
`r_E = 0.12` the smallest determinant anywhere visible is `0.48`, and nothing
folds. At `r_E = 0.16` the fold emerges on `0.7%` of the visible frame as a
thin, hard, bright sliver beside the horizon: a caustic, whose magnification
and spatial frequency are unbounded and which would alias at any resolution.

The crowding does raise the frequency of the fine structure near the rim. Its
shortest cycle over the visible lit area is now `9` pixels at `1200x1200` and
`5.6` at `512x512`, down from `17` and `8`, still clear of the two-pixel limit.

Beyond the rims the bending is gentle but not zero: the pattern shifts enough to
change the far field by up to `20` levels at the 99th percentile. Setting
`--einstein-radius 0` reproduces v026 exactly.

```bash
python pieces/001_last_orbit/experiments/v027_horizon_lensing.py
python pieces/001_last_orbit/experiments/v027_horizon_lensing.py --magnification 0
python pieces/001_last_orbit/experiments/v027_horizon_lensing.py --einstein-radius 0
```

The second command shows the warp without the magnification.

### v028 - evolving ripples

The fine structure from v024 had one wavenumber and one amplitude everywhere,
so its striations read as interference fringes. v028 keeps the same term but
lets all three of its properties change with radius:

```text
N_i = 1 + eps(r_i) sin( k_r R(r_i) + m theta_i + zeta (r_i / r_ring)^2 cos(2 theta_i*) + c ln(r_i + s) )

R(r)   = (1 + kappa r_ring) ln(1 + kappa r) / kappa
eps(r) = min(1, eps_N exp(-lambda (r - r_ring)))
```

- **Spacing.** `R` has slope `(1 + kappa r_ring) / (1 + kappa r)`, which is
  exactly `1` at the ring. The ripples keep their v027 spacing there, are
  tighter toward the horizon and loosen outward. With `kappa = 10` the local
  wavenumber is about three times larger at the horizon than in the outer disk.
- **Amplitude.** `eps` is still `0.35` at the ring. It reaches its cap of `1`
  beside the horizons and falls to about `0.12` between `r = 0.4` and `0.5`, so
  the outer structure dissolves into the smooth disk.
- **Distortion.** `r^2 cos(2 theta*)` is the shape of a companion's tidal
  potential. `theta*` is the anchored angle, measured from the companion and
  not rotated by the orbital phase, so the bulge always faces the other hole.
  Its effect grows with `r^2`: inner ripples stay coherent while the outer ones
  are pulled out of line.

Defaults are `kappa_n = 10`, `lambda_n = 8` and `zeta_n = 3`. Setting all three
to `0` reproduces v027 exactly.

Tighter inner ripples raise the aliasing risk. The shortest cycle over the
visible lit disk is `5.9` pixels at `1200x1200` and `2.5` at `512x512`, against
`7.9` and `3.4` in v027 under the same measurement. Both stay above the
two-pixel limit, and the final render at `6000x6000` has five times the margin.

```bash
python pieces/001_last_orbit/experiments/v028_evolving_ripples.py
python pieces/001_last_orbit/experiments/v028_evolving_ripples.py --zeta-n 0
python pieces/001_last_orbit/experiments/v028_evolving_ripples.py --kappa-n 0 --lambda-n 0 --zeta-n 0
```

