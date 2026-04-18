"""Reference implementation of <CodecName>.

A clean, readable implementation — optimized for understanding, not speed.
See notes.md for background.
"""

from __future__ import annotations

import numpy as np


class Codec:
    """Stub codec — replace with your implementation."""

    def __init__(self, dim: int) -> None:
        self.dim = dim

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (dim,) to a compact representation."""
        raise NotImplementedError

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode back to a vector of shape (dim,)."""
        raise NotImplementedError
