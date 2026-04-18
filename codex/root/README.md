# Root

Angular quantization against the 240 minimal vectors of the E8 lattice. One byte per 8-dimensional unit vector, no training, no parameters.

## When to use

- Your vectors are 8-dimensional (or you can block 8 coordinates at a time)
- You care about **angle** more than magnitude — cosine similarity, inner products, directional similarity
- You want a codec that is **training-free** and has a fixed, well-studied codebook
- You want something small and extremely simple to reason about

Less good fit:
- Your vectors are not near unit norm and you need to preserve magnitude
- Your dimension is not a multiple of 8

## Origin

<!-- ORIGIN — fill in your own words. What made you try using the 240 roots of E8 as a codebook? Was it an image of the lattice? A paper? A moment staring at USQ and wondering what a maximally-symmetric alternative would look like? 3-6 sentences in your voice. -->

**[TODO: Nolan to write 3-6 sentences on what sparked Root.]**

## How to run

```bash
python -m codex.root.demo
```

The demo runs Root on 100 random unit vectors in R^8 and prints the cosine similarity between each original and its decoded reconstruction. You should see a mean cosine around 0.84 — 240 points do a decent job of covering the 7-sphere, but "decent" is not "perfect," and the 15th percentile is a useful reminder that one byte of angular resolution in 8D has real limits.

## How it works

The E8 lattice has exactly 240 minimal-norm vectors, called its **root system**. These 240 points sit on a sphere of radius √2 and have extraordinary symmetry — they form one of the densest sphere packings known in 8 dimensions and achieve the optimal kissing number for that dimension.

Root treats those 240 vectors (normalized to unit length) as a fixed angular codebook. Encoding:

1. Take a vector of shape (8,) and normalize it to unit length.
2. Compute cosine similarity against all 240 normalized roots.
3. Return the index of the closest root as a single byte.

Decoding is a table lookup: index → unit root vector.

Because 240 fits in 8 bits (with 16 spare index values), the codebook is naturally byte-aligned.

## Caveats

- **Dimension is fixed at 8.** Root is defined only on R^8. For higher dimensions, block the input into groups of 8 and apply Root to each block separately.
- **Unit-vector codec.** Root quantizes direction, not magnitude. If you need to preserve length, pair it with a scale code (e.g., one byte of log-gain).
- **Not as accurate as a trained codebook** at the same bit budget for a specific data distribution. Root wins on simplicity and zero setup cost, not on data-fit.
- **16 unused indices.** Indices 240–255 are not valid codewords in this implementation. Downstream parsers should reject them (or reserve them for sentinels).

## Prior art

- **E8 lattice and root system** — classical, see Conway & Sloane, *Sphere Packings, Lattices and Groups* (3rd ed., 1998) for the definitive reference.
- **Kissing number in 8D** — Levenshtein (1979) and Odlyzko–Sloane (1979) independently proved 240 is optimal.
- **E8 in vector quantization** — a long history in signal processing; this reference is a deliberately simple restatement, not a novel contribution in itself.

See `notes.md` for the root-system construction and references.
