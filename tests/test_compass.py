"""Tests for Compass via the Fleet testing harness."""

from __future__ import annotations

import numpy as np
import pytest

from fleet_codecs.compass import Compass
from fleet_testing import Codec, assert_roundtrip_shape, run_roundtrip_eval


def test_implements_codec_protocol() -> None:
    assert isinstance(Compass(dim=32), Codec)


def test_roundtrip_preserves_shape(rng: np.random.Generator) -> None:
    codec = Compass(dim=32, bits_per_coord=3)
    x = rng.standard_normal(32)
    decoded = codec.decode(codec.encode(x))
    assert_roundtrip_shape(x, decoded)


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_cosine_improves_with_bits(bits: int) -> None:
    codec = Compass(dim=32, bits_per_coord=bits)
    result = run_roundtrip_eval(codec, n=200)
    thresholds = {1: 0.90, 2: 0.96, 3: 0.98, 4: 0.99}
    assert result.mean_cos >= thresholds[bits], result.summary()


def test_signs_round_trip_exactly(rng: np.random.Generator) -> None:
    """The heading preserves the full sign pattern."""
    codec = Compass(dim=16, bits_per_coord=3)
    x = rng.standard_normal(16)
    decoded = codec.decode(codec.encode(x))
    assert np.all(np.sign(x) == np.sign(decoded))


def test_bits_per_coord_validation() -> None:
    with pytest.raises(ValueError):
        Compass(dim=16, bits_per_coord=0)
    with pytest.raises(ValueError):
        Compass(dim=16, bits_per_coord=9)
