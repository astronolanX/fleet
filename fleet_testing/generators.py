"""Reproducible vector generators for codec testing."""

from __future__ import annotations

import numpy as np


def gaussian_vectors(
    n: int,
    dim: int,
    *,
    rng: np.random.Generator | None = None,
    seed: int = 0,
) -> np.ndarray:
    """Generate an (n, dim) array of zero-mean unit-variance Gaussian vectors.

    Pass either an existing `rng` or a `seed` — if both are omitted, the
    default rng from `seed=0` is used (fully reproducible).
    """
    if rng is None:
        rng = np.random.default_rng(seed)
    return rng.standard_normal((n, dim))


def unit_vectors(
    n: int,
    dim: int,
    *,
    rng: np.random.Generator | None = None,
    seed: int = 0,
) -> np.ndarray:
    """Generate an (n, dim) array of unit-norm vectors uniformly on S^(dim-1)."""
    x = gaussian_vectors(n, dim, rng=rng, seed=seed)
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    return x / np.clip(norms, 1e-12, None)
