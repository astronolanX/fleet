"""Demonstration of Compass.

Run with:
    python -m codex.compass.demo
"""

from __future__ import annotations

import numpy as np

from .codec import Compass


def main() -> None:
    rng = np.random.default_rng(42)
    dim = 32

    for bits in (1, 2, 3, 4):
        codec = Compass(dim=dim, bits_per_coord=bits)
        cosines = []
        for _ in range(100):
            x = rng.standard_normal(dim)
            code = codec.encode(x)
            x_hat = codec.decode(code)
            num = float(np.dot(x, x_hat))
            den = float(np.linalg.norm(x) * np.linalg.norm(x_hat))
            cosines.append(num / max(den, 1e-12))

        mean_cos = float(np.mean(cosines))
        code_len = len(codec.encode(rng.standard_normal(dim)))
        print(
            f"bits_per_coord={bits}  "
            f"bytes={code_len}  "
            f"mean_cos={mean_cos:.4f}"
        )


if __name__ == "__main__":
    main()
