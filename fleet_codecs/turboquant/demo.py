"""Demonstration of TurboQuant on a random vector.

Run with:
    python -m fleet_codecs.turboquant.demo
"""

from __future__ import annotations

import numpy as np

from .codec import TurboQuant


def main() -> None:
    rng = np.random.default_rng(42)
    dim = 64

    for bits in (1, 2, 3, 4):
        codec = TurboQuant(dim=dim, bits_per_coord=bits, seed=0)
        x = rng.standard_normal(dim)
        code = codec.encode(x)
        x_hat = codec.decode(code)
        cos = float(np.dot(x, x_hat) / (np.linalg.norm(x) * np.linalg.norm(x_hat)))
        print(
            f"bits_per_coord={bits}  "
            f"bytes={len(code)}  "
            f"cosine(original, decoded)={cos:.4f}"
        )


if __name__ == "__main__":
    main()
