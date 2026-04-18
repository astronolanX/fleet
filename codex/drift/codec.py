"""Drift — tangent-space quantization around a base direction.

Every point on a unit sphere has a tangent plane where small
displacements look flat. Drift exploits that: choose a base direction
closest to the input (from a small fixed set of base points), project
the input into the tangent plane around that base, then quantize the
tangent vector with a tiny scalar codebook. Decoding reverses the
steps: take the base, add the tangent displacement, renormalize back
onto the sphere.

The result is a two-stage code: a base index that picks the neighborhood,
and a tangent payload that refines within it. Drift is a clean way to
trade global coverage (which a single codebook would need) for local
precision (where most of the input's interesting structure lives).

See notes.md for discussion of how the base set is chosen and why
tangent-space quantization can be efficient near the chosen base.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np


def _build_base_directions(dim: int) -> np.ndarray:
    """Build a small fixed set of base directions on the unit sphere.

    For the reference, we use the 2*dim axis-aligned unit vectors
    (+/- e_i). This is the simplest base set that covers the sphere
    in a balanced way and keeps the reference readable.
    """
    bases = np.concatenate([np.eye(dim), -np.eye(dim)], axis=0)
    return bases


@dataclass
class Drift:
    """Drift codec — base + tangent-space quantization.

    Parameters
    ----------
    dim:
        Input vector dimension.
    bits_per_coord:
        Bits used to quantize each tangent-space coordinate.
    """

    dim: int
    bits_per_coord: int = 3
    _bases: np.ndarray = field(init=False, repr=False)
    _centers: np.ndarray = field(init=False, repr=False)

    def __post_init__(self) -> None:
        if self.dim < 2:
            raise ValueError(f"dim must be >= 2, got {self.dim}")
        if self.bits_per_coord < 1 or self.bits_per_coord > 8:
            raise ValueError(
                f"bits_per_coord must be in [1, 8], got {self.bits_per_coord}"
            )
        self._bases = _build_base_directions(self.dim)
        levels = 1 << self.bits_per_coord
        step = 2.0 / levels
        self._centers = np.linspace(-1.0 + step / 2, 1.0 - step / 2, levels)

    @property
    def num_bases(self) -> int:
        return int(self._bases.shape[0])

    def encode(self, x: np.ndarray) -> np.ndarray:
        """Encode a vector of shape (dim,) to base + scale + tangent payload."""
        if x.shape != (self.dim,):
            raise ValueError(f"expected shape ({self.dim},), got {x.shape}")

        scale = float(np.linalg.norm(x)) + 1e-12
        unit = x / scale

        cosines = self._bases @ unit
        base_idx = int(np.argmax(cosines))
        base = self._bases[base_idx]

        # Tangent component: part of `unit` orthogonal to `base`.
        projection = float(unit @ base)
        tangent = unit - projection * base

        indices = _quantize(tangent, self._centers)
        scale_byte = _encode_scale(scale)
        return np.concatenate(
            [[base_idx, scale_byte], indices]
        ).astype(np.uint8)

    def decode(self, code: np.ndarray) -> np.ndarray:
        """Decode back to a vector of shape (dim,)."""
        base_idx = int(code[0])
        if base_idx >= self.num_bases:
            raise ValueError(
                f"invalid base index {base_idx} (must be < {self.num_bases})"
            )
        scale = _decode_scale(int(code[1]))
        indices = code[2:]

        base = self._bases[base_idx]
        tangent = self._centers[indices]
        # Remove any component along `base` — tangent lives in the
        # orthogonal complement by construction.
        tangent = tangent - (tangent @ base) * base

        unit_hat = base + tangent
        unit_hat = unit_hat / (np.linalg.norm(unit_hat) + 1e-12)
        return scale * unit_hat


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
