"""Root — angular quantization against the 240 minimal vectors of E8.

The E8 lattice has exactly 240 minimal-norm vectors, known as its root
system. These 240 points sit on a sphere with remarkable symmetry —
it is one of the densest sphere packings known in 8 dimensions and
also the optimal kissing configuration there.

Root treats those 240 vectors as a fixed angular codebook: given a
unit vector, find the root closest to it by cosine similarity, encode
the index. To decode, look up the root by index and return it as the
reconstructed unit vector. No training. No parameters. One byte per
8-dimensional vector.

See notes.md for the construction of the 240 roots and attribution.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def _build_e8_roots() -> np.ndarray:
    """Build the 240 minimal vectors of the E8 root system.

    The E8 root system consists of:
      - 112 "integer" roots: all permutations of (+-1, +-1, 0, 0, 0, 0, 0, 0)
      - 128 "half-integer" roots: all vectors (+-1/2, ..., +-1/2) with an
        even number of minus signs

    Total: 240 vectors, each with norm sqrt(2).
    """
    from itertools import combinations, product

    roots = []

    for i, j in combinations(range(8), 2):
        for si, sj in product((1, -1), repeat=2):
            v = np.zeros(8)
            v[i] = si
            v[j] = sj
            roots.append(v)

    for signs in product((0.5, -0.5), repeat=8):
        if sum(1 for s in signs if s < 0) % 2 == 0:
            roots.append(np.array(signs))

    roots_arr = np.array(roots)
    assert roots_arr.shape == (240, 8), f"expected (240, 8), got {roots_arr.shape}"
    return roots_arr


@dataclass
class Root:
    """Root codec — angular quantization against the E8 root system.

    Parameters
    ----------
    dim:
        Must be 8. Root is defined only for 8-dimensional vectors
        because the E8 root system lives in R^8.
    """

    dim: int = 8
    _roots: np.ndarray = field(init=False, repr=False)
    _roots_normalized: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.dim != 8:
            raise ValueError(f"Root is only defined for dim=8, got dim={self.dim}")
        self._roots = _build_e8_roots()
        norms = np.linalg.norm(self._roots, axis=1, keepdims=True)
        self._roots_normalized = self._roots / norms

    @property
    def codebook(self) -> np.ndarray:
        """The 240 unit-norm codewords, shape (240, 8)."""
        return self._roots_normalized.copy()

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (8,) to a single uint8 index."""
        if x.shape != (8,):
            raise ValueError(f"expected shape (8,), got {x.shape}")
        norm = np.linalg.norm(x)
        if norm < 1e-12:
            return np.array([0], dtype=np.uint8)
        unit = x / norm
        cosines = self._roots_normalized @ unit
        best = int(np.argmax(cosines))
        return np.array([best], dtype=np.uint8)

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode an index back to a unit vector of shape (8,)."""
        if code.shape != (1,):
            raise ValueError(f"expected shape (1,), got {code.shape}")
        idx = int(code[0])
        if idx >= 240:
            raise ValueError(f"invalid root index {idx} (must be < 240)")
        return self._roots_normalized[idx].copy()
