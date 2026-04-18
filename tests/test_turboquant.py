"""Tests for TurboQuant via the Fleet testing harness."""

from __future__ import annotations

import numpy as np
import pytest

from codex.turboquant import TurboQuant
from testing import (
    Codec,
    assert_cosine_above,
    assert_roundtrip_shape,
    run_roundtrip_eval,
)


def test_implements_codec_protocol() -> None:
    codec = TurboQuant(dim=32, bits_per_coord=2)
    assert isinstance(codec, Codec)


def test_roundtrip_preserves_shape(rng: np.random.Generator) -> None:
    codec = TurboQuant(dim=64, bits_per_coord=2)
    x = rng.standard_normal(64)
    decoded = codec.decode(codec.encode(x))
    assert_roundtrip_shape(x, decoded)


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_roundtrip_cosine_improves_with_bits(bits: int) -> None:
    codec = TurboQuant(dim=64, bits_per_coord=bits)
    result = run_roundtrip_eval(codec, n=200)
    thresholds = {1: 0.60, 2: 0.85, 3: 0.87, 4: 0.88}
    assert result.mean_cos >= thresholds[bits], result.summary()


def test_harness_returns_percentiles() -> None:
    codec = TurboQuant(dim=64, bits_per_coord=2)
    result = run_roundtrip_eval(codec, n=100)
    assert result.p05_cos <= result.p50_cos <= result.p95_cos
    assert 0.0 <= result.mean_cos <= 1.0


def test_harness_accepts_custom_vectors(rng: np.random.Generator) -> None:
    codec = TurboQuant(dim=32, bits_per_coord=2)
    vectors = rng.standard_normal((50, 32))
    result = run_roundtrip_eval(codec, vectors=vectors)
    assert result.n == 50


def test_harness_rejects_dim_mismatch(rng: np.random.Generator) -> None:
    codec = TurboQuant(dim=32, bits_per_coord=2)
    wrong_shape = rng.standard_normal((10, 64))
    with pytest.raises(ValueError):
        run_roundtrip_eval(codec, vectors=wrong_shape)


def test_assert_cosine_above_passes_on_high_cosine(
    small_gaussian_batch: np.ndarray,
) -> None:
    measured = assert_cosine_above(
        small_gaussian_batch,
        small_gaussian_batch,
        threshold=0.99,
    )
    assert measured > 0.99


def test_assert_cosine_above_fails_on_low_cosine(
    rng: np.random.Generator,
) -> None:
    a = rng.standard_normal((8, 16))
    b = rng.standard_normal((8, 16))
    with pytest.raises(AssertionError, match="ASSERT FAILED"):
        assert_cosine_above(a, b, threshold=0.95)
