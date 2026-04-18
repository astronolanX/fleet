"""Tests for Drift via the Fleet testing harness."""

from __future__ import annotations

import numpy as np
import pytest

from fleet_codecs.drift import Drift
from fleet_testing import Codec, assert_roundtrip_shape, run_roundtrip_eval


def test_implements_codec_protocol() -> None:
    assert isinstance(Drift(dim=32), Codec)


def test_num_bases_scales_with_dim() -> None:
    codec = Drift(dim=32)
    assert codec.num_bases == 64


def test_roundtrip_preserves_shape(rng: np.random.Generator) -> None:
    codec = Drift(dim=32, bits_per_coord=3)
    x = rng.standard_normal(32)
    decoded = codec.decode(codec.encode(x))
    assert_roundtrip_shape(x, decoded)


@pytest.mark.parametrize("bits", [1, 2, 3, 4])
def test_cosine_improves_with_bits(bits: int) -> None:
    codec = Drift(dim=32, bits_per_coord=bits)
    result = run_roundtrip_eval(codec, n=200)
    thresholds = {1: 0.80, 2: 0.82, 3: 0.85, 4: 0.88}
    assert result.mean_cos >= thresholds[bits], result.summary()


def test_dim_at_least_2() -> None:
    with pytest.raises(ValueError):
        Drift(dim=1)


def test_invalid_base_index_raises(rng: np.random.Generator) -> None:
    codec = Drift(dim=16, bits_per_coord=2)
    bad_code = np.concatenate([[255, 128], np.zeros(16, dtype=np.uint8)]).astype(
        np.uint8
    )
    with pytest.raises(ValueError):
        codec.decode(bad_code)
