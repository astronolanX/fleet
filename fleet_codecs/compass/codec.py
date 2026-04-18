"""Compass — sign-pattern routing with full sign preservation.

The sign pattern of a vector carries real information before you look at
magnitudes. Compass packs the full sign pattern into a separate "heading"
payload, then quantizes magnitudes only. At decode time the heading
directs each magnitude to its correct sign.

Two pieces live in the code:

- The **heading** — one bit per input coordinate, packed into bytes. This
  is the full sign pattern of the input.
- The **magnitudes** — unsigned scalar quantization of the per-coordinate
  absolute values, after scaling by the per-vector RMS.

Splitting direction (heading) from magnitude (payload) makes the idea
legible: the heading is a compact representation of which way the vector
points, and the magnitudes are a compact representation of how far it
reaches in each direction.

See notes.md for variants that use the heading to dispatch among
structurally different sub-codebooks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


@dataclass
class Compass:
    """Compass codec — sign-pattern heading + magnitude payload.

    Parameters
    ----------
    dim:
        Input vector dimension.
    bits_per_coord:
        Bits used to quantize each magnitude. Typical: 2-4.
    """

    dim: int
    bits_per_coord: int = 3
    _centers: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.bits_per_coord < 1 or self.bits_per_coord > 8:
            raise ValueError(
                f"bits_per_coord must be in [1, 8], got {self.bits_per_coord}"
            )
        levels = 1 << self.bits_per_coord
        # Magnitudes are non-negative, so centers live in [0, 2] with a
        # uniform step. A magnitude of 2 covers up to two RMS units,
        # which is plenty of headroom for near-Gaussian inputs.
        self._centers = (np.arange(levels) + 0.5) * (2.0 / levels)

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (dim,) to a heading + scale + magnitudes."""
        if x.shape != (self.dim,):
            raise ValueError(f"expected shape ({self.dim},), got {x.shape}")

        heading = _pack_signs(x)
        scale = float(np.linalg.norm(x)) / np.sqrt(self.dim) + 1e-12
        normalized_magnitudes = np.abs(x) / scale
        indices = _quantize(normalized_magnitudes, self._centers)
        scale_byte = _encode_scale(scale)
        return np.concatenate(
            [[scale_byte], heading, indices]
        ).astype(np.uint8)

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode back to a vector of shape (dim,)."""
        scale = _decode_scale(int(code[0]))
        heading_bytes = (self.dim + 7) // 8
        heading = code[1 : 1 + heading_bytes]
        indices = code[1 + heading_bytes :]

        signs = _unpack_signs(heading, self.dim)
        magnitudes = self._centers[indices] * scale
        return signs * magnitudes


def _pack_signs(x: np.ndarray) -> np.ndarray:
    """Pack the sign pattern of x into (dim+7)//8 bytes."""
    dim = x.shape[0]
    n_bytes = (dim + 7) // 8
    out = np.zeros(n_bytes, dtype=np.uint8)
    for i in range(dim):
        if x[i] >= 0:
            out[i // 8] |= 1 << (i % 8)
    return out


def _unpack_signs(heading: np.ndarray, dim: int) -> np.ndarray:
    """Inverse of _pack_signs. Returns an array of +/-1 floats."""
    out = np.empty(dim)
    for i in range(dim):
        bit = (heading[i // 8] >> (i % 8)) & 1
        out[i] = 1.0 if bit else -1.0
    return out


def _quantize(x: np.ndarray, centers: np.ndarray) -> np.ndarray:
    diffs = np.abs(x[:, None] - centers[None, :])
    return np.argmin(diffs, axis=1).astype(np.uint8)


def _encode_scale(scale: float) -> int:
    log_scale = np.log2(max(scale, 1e-12))
    clipped = np.clip(log_scale, -8.0, 8.0)
    return int(round((clipped + 8.0) * 255.0 / 16.0))


def _decode_scale(code: int) -> float:
    log_scale = code * 16.0 / 255.0 - 8.0
    return float(2.0**log_scale)
