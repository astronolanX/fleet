# Drift

Base + tangent-space quantization. Pick the base direction nearest to your input, project into the tangent plane around that base, then quantize the tangent vector with a tiny scalar codebook. Two-stage codes that trade global coverage for local precision.

## When to use

- Your inputs cluster near a small number of "prototype" directions — so locking onto the nearest prototype and refining locally is natural
- You want a codec whose code structure reflects the geometry of the problem (base + displacement), not just a flat bitfield
- You want a small codec that is friendly to reason about

Less good fit:
- Your inputs are uniform on the sphere with no clustering — then tangent-space refinement does no better than plain scalar quantization, and the base byte is overhead
- You have a well-tuned rotation-based codec already; Drift's pedagogical clarity does not translate to a performance win over rotation on symmetric inputs

## Origin

<!-- ORIGIN — fill in your own words. What made you try quantizing in a tangent space? A visualization of vectors as arrows on a sphere? A moment noticing that most of your input distribution sat near a handful of directions? A connection to differential geometry or to E8's local structure? 3-6 sentences in your voice. -->

**[TODO: Nolan to write 3-6 sentences on what sparked Drift.]**

## How to run

```bash
python -m codex.drift.demo
```

The demo runs Drift at 1, 2, 3, and 4 bits per tangent coordinate on Gaussian 32-dimensional vectors. You should see cosine similarity climbing as bits increase — the base is already doing most of the coarse work, and the tangent refines within the local patch.

## How it works

Three fields on encode:

1. **Base index** — the axis-aligned unit vector (±e_i) closest to the normalized input, as a single byte.
2. **Scale** — one byte of log-gain encoding the per-vector magnitude.
3. **Tangent payload** — for each coordinate, a uniform scalar quantization of the tangent component (the part of the normalized input orthogonal to the base).

Decode reads the base from its index, reads the tangent magnitudes, assembles `base + tangent`, renormalizes back onto the unit sphere, and multiplies by the scale.

The reason it works: near any base point on a unit sphere, small displacements in the tangent plane are (to first order) the right way to describe where you've drifted. Quantizing in the tangent plane around the *right* base point gives you finer effective resolution than quantizing the full sphere with the same bit budget.

## Caveats

- **This reference uses axis-aligned bases (±e_i).** That gives `2*dim` base directions, which is a coarse but balanced cover of the sphere. Richer versions of the idea use a smarter base set — E8 roots, a learned codebook, or a lattice-aligned set — and see more benefit per bit.
- **Tangent is sign-preserving but magnitude-limited.** The uniform scalar quantizer on the tangent covers `[-1, 1]`. Inputs whose tangent exceeds that range will clip; in practice, after normalizing to unit norm and subtracting a well-chosen base, tangent magnitudes stay inside the range.
- **Base is chosen by cosine-max.** Near corner cases where two bases are equally close, the encoder picks the lower-indexed one; this is deterministic but can produce small discontinuities in the reconstructed vector.

## Prior art

- **Tangent-space methods** are standard in differential geometry and in manifold-aware quantization (see e.g., Pennec et al., *A Riemannian framework for tensor computing*, IJCV 2006, for the general idea of working in tangent space).
- **Two-stage codebooks** (base + refinement) are a classical pattern in vector quantization; the Tree-Structured VQ and Multistage VQ literatures are the canonical references.
- No specific paper is being ported; Drift is a compact illustration of "quantize locally in the tangent plane around the nearest base."
