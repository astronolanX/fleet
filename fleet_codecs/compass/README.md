# Compass

Separates a vector into its **heading** (full sign pattern, one bit per coordinate) and its **magnitudes** (non-negative scalar-quantized values), stored side by side. At decode, the heading directs each magnitude to its correct sign.

## When to use

- You want a codec that makes direction and magnitude legible as separate fields in the code
- Your downstream consumer can read the heading byte(s) directly — e.g., as a fast prefilter before full decoding
- You want a codec that is simple to explain and simple to parse

Less good fit:
- Your vectors are always near unit norm — then the per-vector scale byte is overhead with no return
- You have a strong rotation-based codec already; Compass will not outperform it at the same bit budget

## Origin

<!-- ORIGIN — fill in your own words. What made you try using sign patterns as a dispatch feature? Was it a specific dataset where the sign bits looked more informative than you expected? An insight about how Lie-theory monodromy uses sign to select a branch? 3-6 sentences in your voice. -->

**[TODO: Nolan to write 3-6 sentences on what sparked Compass.]**

## How to run

```bash
python -m fleet_codecs.compass.demo
```

The demo runs Compass at 1, 2, 3, and 4 bits per coordinate on Gaussian 32-dimensional vectors and prints the resulting mean cosine. More bits give finer magnitudes and higher fidelity; the heading contribution stays the same.

## How it works

Three fields on encode:

1. **Scale** — one byte of log-gain encoding the per-vector RMS magnitude.
2. **Heading** — the full sign pattern of the input, packed one bit per coordinate into `ceil(dim/8)` bytes.
3. **Magnitudes** — for each coordinate, an index into a uniform non-negative scalar quantizer applied to the coordinate's absolute value (after division by the scale).

Decode reads the three fields, expands the sign bits into an array of +1/-1, looks up each magnitude index in the non-negative codebook, multiplies by scale and sign, and returns the vector.

The key structural idea is that **direction (heading) and magnitude (payload) are separated at the code level**. A downstream reader can inspect the heading byte without touching the payload, which makes Compass friendly for applications that want a cheap directional prefilter.

## Caveats

- **This is a deliberately simple reference.** Richer versions of the idea use the heading (or parts of it) to pick among **structurally different sub-codebooks**, not just to preserve signs. That variant is described in `notes.md`.
- **Byte overhead is fixed.** The scale and heading each take a small constant number of bytes regardless of vector length, so Compass is more efficient on longer vectors.
- **Uniform quantizer on magnitudes.** A Lloyd-Max or data-adapted magnitude codebook would improve fidelity but is out of scope for this public reference.

## Prior art

- **Structured vector quantization** that separates direction from magnitude has a long history in speech coding (Linde-Buzo-Gray and descendants).
- **Monodromy** in Lie theory and algebraic geometry — paths around a branch point selecting a sheet of a multi-valued function — is a conceptual source for the "sign as routing" framing rather than a technical ancestor.
- No specific paper is being ported; Compass is a compact illustration of "sign-pattern as an explicit code field."
