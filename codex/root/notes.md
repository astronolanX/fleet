# Root — Notes

## The E8 root system

The E8 root system is a set of 240 vectors in R^8, each of norm √2, that form the simplest roots of the exceptional Lie algebra E8. Two standard constructions combine to give all 240:

**Integer roots (112 vectors):**
All vectors with two nonzero coordinates equal to ±1 and the rest zero. Count: (8 choose 2) × 4 = 112.

```
(±1, ±1,  0,  0,  0,  0,  0,  0)  and all coordinate permutations
```

**Half-integer roots (128 vectors):**
All vectors of the form (±½, ±½, ±½, ±½, ±½, ±½, ±½, ±½) with an **even** number of minus signs. Count: 2^8 / 2 = 128.

```
(±½, ±½, ±½, ±½, ±½, ±½, ±½, ±½)    with even count of −
```

Total: 112 + 128 = 240.

All 240 have the same norm, √2, so normalizing gives 240 unit vectors on the 7-sphere.

## Why 240 and not 256

240 is exact, not approximate. It comes from the structure of the E8 Lie algebra. There is no extra symmetry at 256 — the number 256 (one byte) is a coincidence from binary computing, not from geometry. The gap (16 unused indices) is a small price for using the geometrically optimal arrangement.

## Kissing number in 8 dimensions

The **kissing number** k(n) is the maximum number of unit spheres that can touch a central unit sphere in R^n without overlapping. For n = 8, k(8) = 240, achieved by placing spheres centered at the 240 roots of E8. This was proved independently by:

- V. I. Levenshtein, *Boundaries for packings in n-dimensional Euclidean space*, Doklady Akademii Nauk SSSR 245 (1979), 1299–1303.
- A. M. Odlyzko and N. J. A. Sloane, *New bounds on the number of unit spheres that can touch a unit sphere in n dimensions*, J. Combin. Theory Ser. A 26 (1979), 210–214.

## References

- J. H. Conway and N. J. A. Sloane, *Sphere Packings, Lattices and Groups*, 3rd ed., Springer 1998. Chapter 4 covers E8 in detail.
- N. Bourbaki, *Groupes et algèbres de Lie, Chap. 4–6*. The original Lie-theoretic source.
- Garrett Lisi's blog and visualization work has some beautiful depictions of E8 that made the lattice accessible outside pure math.

## Scope and honesty

Root is a reference codec. It is not state of the art for any specific data distribution — a trained codebook tuned to the input statistics will beat it at the same bit budget. What Root offers is an honest baseline: a maximally symmetric codebook with zero training cost, useful as a reference point and as a teaching example of how lattice geometry meets vector quantization.
