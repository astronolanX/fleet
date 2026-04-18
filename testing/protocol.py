"""The Codec Protocol every Fleet codec implements.

Structural typing — a class is a Codec if it has `dim`, `encode`, and
`decode`. No subclassing required.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Codec(Protocol):
    """A codec that encodes a vector to a compact code and decodes back."""

    dim: int

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (dim,) to a compact uint8 code."""
        ...

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode a code back to a vector of shape (dim,)."""
        ...
