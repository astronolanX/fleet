"""Structured assertions for codec testing.

Every failure message follows:
    ASSERT FAILED | <function> | <measured>=<value> < <threshold>=<value>
so failures are easy to scan and grep.
"""

from __future__ import annotations

import numpy as np


def assert_cosine_above(
    original: np.ndarray,
    decoded: np.ndarray,
    threshold: float,
) -> float:
    """Assert that cosine(original, decoded) >= threshold.

    Works for either a single vector pair (1D arrays) or a batch of pairs
    (2D arrays with matching shapes). Returns the measured mean cosine.
    """
    if original.shape != decoded.shape:
        raise AssertionError(
            f"ASSERT FAILED | assert_cosine_above | "
            f"shape mismatch: original={original.shape} decoded={decoded.shape}"
        )

    if original.ndim == 1:
        original = original[None, :]
        decoded = decoded[None, :]

    num = np.sum(original * decoded, axis=1)
    den = np.linalg.norm(original, axis=1) * np.linalg.norm(decoded, axis=1)
    den = np.clip(den, 1e-12, None)
    cosines = num / den
    mean_cos = float(np.mean(cosines))

    if mean_cos < threshold:
        raise AssertionError(
            f"ASSERT FAILED | assert_cosine_above | "
            f"mean_cos={mean_cos:.4f} < threshold={threshold:.4f}"
        )
    return mean_cos


def assert_roundtrip_shape(original: np.ndarray, decoded: np.ndarray) -> None:
    """Assert that the decoded vector has the same shape as the original."""
    if original.shape != decoded.shape:
        raise AssertionError(
            f"ASSERT FAILED | assert_roundtrip_shape | "
            f"original={original.shape} decoded={decoded.shape}"
        )
