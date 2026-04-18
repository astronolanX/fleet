"""Roundtrip evaluation runner.

Runs a codec across a batch of vectors and returns summary stats. The
harness is deliberately light — it reports, it does not judge. If you
want a pass/fail gate, use an assertion from fleet_testing.assertions
against the returned numbers.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .generators import gaussian_vectors
from .protocol import Codec


@dataclass
class RoundtripResult:
    """Summary of a roundtrip evaluation."""

    n: int
    dim: int
    bytes_per_vector: float
    mean_cos: float
    p05_cos: float
    p50_cos: float
    p95_cos: float

    def summary(self) -> str:
        """One-line summary string for logging or printing."""
        return (
            f"n={self.n} dim={self.dim} "
            f"bytes/vec={self.bytes_per_vector:.1f} "
            f"cos: p05={self.p05_cos:.3f} p50={self.p50_cos:.3f} "
            f"mean={self.mean_cos:.3f} p95={self.p95_cos:.3f}"
        )


def run_roundtrip_eval(
    codec: Codec,
    *,
    n: int = 100,
    rng: np.random.Generator | None = None,
    vectors: np.ndarray | None = None,
) -> RoundtripResult:
    """Encode then decode `n` vectors and summarize the roundtrip cosines.

    Either pass your own `vectors` of shape (n, dim) or let the harness
    generate a Gaussian batch. Returns a RoundtripResult with population
    percentiles of cosine(original, decoded).
    """
    if vectors is None:
        vectors = gaussian_vectors(n, codec.dim, rng=rng)
    else:
        if vectors.shape[1] != codec.dim:
            raise ValueError(
                f"vectors.shape[1]={vectors.shape[1]} does not match "
                f"codec.dim={codec.dim}"
            )
        n = vectors.shape[0]

    cosines = np.empty(n)
    total_bytes = 0

    for i in range(n):
        code = codec.encode(vectors[i])
        total_bytes += len(code)
        decoded = codec.decode(code)
        num = float(np.dot(vectors[i], decoded))
        den = float(np.linalg.norm(vectors[i]) * np.linalg.norm(decoded))
        cosines[i] = num / max(den, 1e-12)

    return RoundtripResult(
        n=n,
        dim=codec.dim,
        bytes_per_vector=total_bytes / n,
        mean_cos=float(np.mean(cosines)),
        p05_cos=float(np.percentile(cosines, 5)),
        p50_cos=float(np.percentile(cosines, 50)),
        p95_cos=float(np.percentile(cosines, 95)),
    )
