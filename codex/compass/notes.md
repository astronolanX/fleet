# Compass — Notes

## Why signs are more informative than they look

In many real signal distributions — sensor readings, embeddings, audio features — coordinate signs are not independent. A positive value in one coordinate often correlates with a positive value in another, especially after any kind of feature extraction or rotation. This means that conditioning a codebook on the sign pattern of a few leading coordinates can separate the input distribution into sub-populations that are each easier to quantize than the whole.

## The simplified reference

This implementation uses the **heading** (sign pattern of the first few coordinates) only to preserve those signs exactly; the payload is quantized as unsigned magnitudes. The effect is:

- The leading `heading_bits` coordinates are perfectly reconstructed in sign.
- The remaining coordinates lose their sign, which pulls the achievable cosine toward the sign-free limit on symmetric inputs.

That is intentional for a public reference — it makes the *contribution of the heading* legible without muddying the picture with additional machinery.

## Richer variants

Full-strength versions of the idea can do any of the following:

- **Store the full sign pattern** (one bit per coordinate) alongside a smaller-footprint magnitude code, recovering all signs at decode
- **Use the heading to select among structurally different sub-codebooks** — each branch specializes in a different region of the sphere (e.g., each branch uses a rotation adapted to that region)
- **Use the heading as a context for an entropy coder**, so the magnitude distribution within each branch is compressed more tightly
- **Combine with a rotation first** so the heading selects a branch after coordinates have been decorrelated

These extensions move beyond the scope of this reference. The goal here is to make the core idea — *sign as routing* — readable.

## Prior art

- **Monodromy** as a mathematical concept comes from algebraic geometry and the study of multi-valued functions (see e.g., Deligne, *Équations Différentielles à Points Singuliers Réguliers*, Springer 1970). It is the inspiration behind the branch-selection metaphor used here, not a specific technical source.
- **Structured vector quantization** with conditional codebooks has a long history in speech and audio coding; the Linde-Buzo-Gray algorithm and its descendants all use input-dependent routing in one form or another.

## Scope and honesty

Compass is a minimal illustration. The numbers it produces should be read as "look, sign-routing does something measurable," not as "this is a competitive codec." A tuned rotation-based codec will usually beat it at the same bit budget on symmetric inputs.
