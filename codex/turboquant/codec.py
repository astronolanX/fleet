"""TurboQuant — randomized-rotation scalar quantization.

A clean reference implementation of the core idea: rotate the input by a
random orthogonal matrix (decorrelates coordinates), then apply uniform
scalar quantization on each coordinate. Decoding inverts both steps.

The rotation is the essential ingredient: after a random orthogonal
rotation, coordinates of a natural-signal vector look approximately
Gaussian and have small magnitudes, so uniform scalar quantization loses
less structure than it would on the raw input.

See notes.md for background and attribution.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class TurboQuant:
    """TurboQuant codec.

    Parameters
    ----------
    dim:
        Input vector dimension.
    bits_per_coord:
        Number of bits per coordinate after rotation. Typical values: 1-4.
    seed:
        Seed used to generate the random orthogonal rotation. The same
        seed must be used for encoding and decoding.
    """

    dim: int
    bits_per_coord: int = 2
    seed: int = 0

    def __post_init__(self) -> None:
        self._rotation = _random_orthogonal(self.dim, self.seed)
        self._levels = 1 << self.bits_per_coord
        self._centers = _uniform_centers(self._levels)

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (dim,) to a uint8 array of indices."""
        if x.shape != (self.dim,):
            raise ValueError(f"expected shape ({self.dim},), got {x.shape}")
        rotated = self._rotation @ x
        scale = np.linalg.norm(rotated) / np.sqrt(self.dim) + 1e-12
        normalized = rotated / scale
        indices = _quantize(normalized, self._centers)
        return np.concatenate([[_encode_scale(scale)], indices]).astype(np.uint8)

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode back to a vector of shape (dim,)."""
        scale = _decode_scale(code[0])
        indices = code[1:]
        normalized = self._centers[indices]
        rotated = normalized * scale
        return self._rotation.T @ rotated


def _random_orthogonal(dim: int, seed: int) -> np.ndarray:
    """Random orthogonal matrix via QR decomposition of a Gaussian matrix."""
    rng = np.random.default_rng(seed)
    q, r = np.linalg.qr(rng.standard_normal((dim, dim)))
    return q * np.sign(np.diag(r))


def _uniform_centers(levels: int) -> np.ndarray:
    """Symmetric uniform quantization centers around zero."""
    step = 2.0 / levels
    return np.linspace(-1.0 + step / 2, 1.0 - step / 2, levels)


def _quantize(x: np.ndarray, centers: np.ndarray) -> np.ndarray:
    """Snap each coordinate of x to the nearest center."""
    diffs = np.abs(x[:, None] - centers[None, :])
    return np.argmin(diffs, axis=1).astype(np.uint8)


def _encode_scale(scale: float) -> int:
    """Encode a positive scale to a single uint8 via log-gain quantization."""
    log_scale = np.log2(max(scale, 1e-12))
    clipped = np.clip(log_scale, -8.0, 8.0)
    return int(round((clipped + 8.0) * 255.0 / 16.0))


def _decode_scale(code: int) -> float:
    """Inverse of _encode_scale."""
    log_scale = code * 16.0 / 255.0 - 8.0
    return float(2.0**log_scale)
