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

- The rotation-first-then-quantize idea has a long history in signal processing. Recent attention comes from work on training-free compression for vector search and for LLM weight compression.
- The specific "TurboQuant" framing appears in recent work from Google; see the TurboQuant paper at ICLR 2026 for the published version.
- This implementation is original — it is not a line-by-line port of any specific paper's code.
