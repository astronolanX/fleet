# TurboQuant — Notes

## The idea in one paragraph

A random orthogonal rotation is a good "universal whitener" for natural signals. After rotation, coordinates are decorrelated and approximately Gaussian in magnitude, so uniform scalar quantization — the simplest quantizer there is — covers the distribution well. The original input is recovered by inverting the rotation. No training, no codebook, no learned structure.

## Why rotation helps

Uniform scalar quantization wastes bits when the input distribution has heavy tails or strong magnitude imbalance across coordinates. Natural signals (sensor data, embeddings, audio features) often have both. A random orthogonal rotation spreads the energy across coordinates and softens the tails, so each coordinate gets similar quantization error — which is exactly what you want when the downstream use is cosine similarity or inner products.

## Variants in the literature

Production implementations differ from this reference in a few ways:

- **Structured rotations** — Hadamard transforms, SRHT, or product-of-random-rotations instead of a dense matrix. Same statistical properties, much cheaper at large dimensions.
- **Non-uniform quantization** — Lloyd-Max optimized levels per coordinate, sometimes shared across coordinates.
- **Lattice quantization** — replacing scalar quantization with lattice quantization (e.g., D_n, E_8) after rotation, trading a small amount of complexity for a better packing of the post-rotation distribution.
- **Entropy coding** — applying Huffman or range coding to the post-quantization indices.

This reference sticks to the core: dense rotation, scalar quantization, log-gain scale. It's the clearest version to read.

## Attribution

**TurboQuant** is introduced by:

> Amir Zandieh, Majid Daliri, Majid Hadian, Vahab Mirrokni.
> *TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate.*
> ICLR 2026. arXiv: [2504.19874](https://arxiv.org/abs/2504.19874).

Zandieh, Hadian, and Mirrokni are at Google Research / Google DeepMind; Daliri is at NYU. The paper establishes near-optimal distortion rates for mean-squared-error and inner-product preservation using randomized rotations and optimal per-coordinate scalar quantizers, with a careful analysis based on the beta distribution that emerges after rotation.

Google Research's blog post ([research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression](https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/)) gives a more accessible summary.

The broader rotation-first-then-quantize family has a long history in signal processing — see the classical references in Gersho & Gray, *Vector Quantization and Signal Compression* (Kluwer, 1992). TurboQuant's contribution is the near-optimality analysis and the specific bit-allocation scheme, not the basic idea of rotating before quantizing.

**About this reference implementation.** This code is a clean-room, deliberately simplified version written to illustrate the core structure (dense random rotation + uniform scalar quantization + log-gain scale). It does not implement the paper's optimal per-coordinate quantizers, structured rotations, or other refinements. For the full method, read the paper.
