"""Demonstration of Root on random unit vectors.

Run with:
    python -m fleet_codecs.root.demo
"""

from __future__ import annotations

import numpy as np

from .codec import Root


def main() -> None:
    rng = np.random.default_rng(42)
    codec = Root()

    n = 100
    cosines = np.empty(n)
    for i in range(n):
        x = rng.standard_normal(8)
        x /= np.linalg.norm(x)
        code = codec.encode(x)
        x_hat = codec.decode(code)
        cosines[i] = float(np.dot(x, x_hat))

    print(f"codebook size: {codec.codebook.shape[0]} unit vectors")
    print(f"bytes per vector: 1")
    print(f"cosine(original, decoded):")
    print(f"  mean = {cosines.mean():.4f}")
    print(f"  p05  = {np.percentile(cosines, 5):.4f}")
    print(f"  p95  = {np.percentile(cosines, 95):.4f}")


if __name__ == "__main__":
    main()
