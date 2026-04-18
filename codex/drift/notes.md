# Drift — Notes

## The geometric intuition

A unit vector `x` on the sphere `S^(n-1)` can be described, in local coordinates near a base point `b`, as `x = b + t` where `t` is a vector in the tangent plane at `b` (i.e., `t . b = 0`) and `|x| = 1` gives a constraint on `|t|`. For `x` close to `b`, `t` is small and the mapping from `t` to `x` is approximately linear.

This means if you can **pick the right `b`** (cheap: one codebook lookup) and then describe **`t` efficiently** (cheap: a small scalar quantizer), you can describe `x` to high precision. You're spending most of your bits refining within a small patch rather than covering the whole sphere with a single codebook.

## Choice of base set

The reference implementation uses axis-aligned unit vectors `±e_i`. That gives `2n` bases in `n` dimensions, which:

- covers the sphere in a balanced way (each base "owns" a hemisphere's worth of the sphere by cosine proximity)
- needs zero training data
- is trivial to implement and reason about

Richer choices exist:

- **Lattice-aligned bases.** Using the minimal vectors of a good lattice (e.g., the 240 roots of E8 in dimension 8) as the base set gives denser, more symmetric coverage. See the Root codec in this same gallery for a pure angular codec on those 240 points.
- **Learned bases.** A data-fit codebook (e.g., via k-means on unit-normalized training vectors) can place bases where the data actually concentrates, improving fidelity on that distribution at the cost of needing training.

## Why this is pedagogically useful

The core idea — **spend coarse bits on a base, then spend fine bits on a local displacement** — is one of the clearest expressions of the general principle that good codecs exploit locality. The two-stage structure makes the tradeoff explicit in the code layout: a fixed cost (base + scale) up front, then a variable payload whose bit budget you can tune.

## Prior art

- **Tangent-space methods in manifold statistics**. Pennec, X., Fillard, P., and Ayache, N., *A Riemannian framework for tensor computing*, International Journal of Computer Vision 66 (2006), 41–66.
- **Tree-Structured Vector Quantization and Multistage VQ**. Gersho & Gray, *Vector Quantization and Signal Compression*, Kluwer, 1992, Ch. 12.
- **Sphere-manifold geometry for VQ**. Numerous classical references; Conway & Sloane (*Sphere Packings, Lattices and Groups*) is the standard source for the lattice side.

## Scope and honesty

Drift is a reference that illustrates the tangent-space idea cleanly. It is not tuned to beat a well-designed rotation-first codec on symmetric inputs, and the axis-aligned base set is deliberately simple. If you want to experiment, swap in a richer base set (e.g., E8 roots) and watch how the fidelity changes at fixed bit budget.
