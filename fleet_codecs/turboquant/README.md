# TurboQuant

A reference implementation of randomized-rotation scalar quantization — the core idea from the TurboQuant line of work: rotate the input by a random orthogonal matrix, then apply uniform scalar quantization on each coordinate.

## When to use

- You want to compress vectors for nearest-neighbor or inner-product search
- The input distribution is roughly zero-mean with some structure across coordinates
- You need a codec that is **training-free** — no data is required to set it up
- Bandwidth matters and you can afford a small rotation at encode/decode

Less good fit:
- Your data has strong sparsity patterns that rotation will destroy
- You have abundant bandwidth and don't need compression

## How to run

```bash
python -m fleet_codecs.turboquant.demo
```

The demo runs TurboQuant at 1, 2, 3, and 4 bits per coordinate on a random 64-dimensional vector and prints the cosine similarity between the original and the decoded vector. You should see cosine climbing as bits_per_coord increases.

## How it works

Three steps on encode:

1. **Rotate** the input by a random orthogonal matrix (the same seed is used at decode).
2. **Normalize** the rotated vector by its per-vector scale, and store the scale in one byte.
3. **Quantize** each coordinate to one of `2^bits_per_coord` uniform levels.

Decode inverts the steps: unpack the scale, look up the level for each coordinate, scale back up, and rotate back.

The rotation is what makes uniform scalar quantization work. After a random orthogonal rotation, the coordinates of a natural-signal vector look approximately Gaussian and have roughly equal magnitudes, so uniform scalar quantization covers the distribution evenly.

## Caveats

- The rotation matrix is generated from `numpy` random state and stored implicitly via `seed`. Encoder and decoder must share the seed and dimension.
- This reference uses dense matrix multiplication for the rotation. Production implementations often use structured rotations (Hadamard, SRHT) for speed on large dimensions.
- The scale encoding uses log-gain quantization over the range `2^-8` to `2^8`. Inputs outside that range will clip.

## Prior art

The technique is presented in recent work from Google and others on training-free compression for inner-product-preserving vector quantization. This implementation is deliberately simplified for clarity — see `notes.md` for references and a discussion of the variants found in the literature.
