"""Runnable demonstration of <CodecName>.

Run with:
    python -m fleet_codecs.<name>.demo
"""

from __future__ import annotations

import numpy as np

from .codec import Codec


def main() -> None:
    rng = np.random.default_rng(42)
    dim = 64

    codec = Codec(dim=dim)
    x = rng.standard_normal(dim)

    code = codec.encode(x)
    x_hat = codec.decode(code)

    cos = float(np.dot(x, x_hat) / (np.linalg.norm(x) * np.linalg.norm(x_hat)))
    print(f"dim={dim}  cosine(original, decoded)={cos:.4f}")


if __name__ == "__main__":
    main()
