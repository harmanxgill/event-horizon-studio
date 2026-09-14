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

Possible next versions:

- v017: rotating the binary axis with the same phase
- v018: separation shrinking as the orbit decays
