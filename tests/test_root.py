"""Tests for Root via the Fleet testing harness."""

from __future__ import annotations

import numpy as np
import pytest

from codex.root import Root
from testing import Codec, assert_roundtrip_shape, run_roundtrip_eval


def test_implements_codec_protocol() -> None:
    assert isinstance(Root(), Codec)


def test_codebook_size() -> None:
    assert Root().codebook.shape == (240, 8)


def test_codebook_is_unit_norm() -> None:
    codebook = Root().codebook
    norms = np.linalg.norm(codebook, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-10)


def test_dim_must_be_8() -> None:
    with pytest.raises(ValueError):
        Root(dim=16)


def test_roundtrip_preserves_shape(rng: np.random.Generator) -> None:
    codec = Root()
    x = rng.standard_normal(8)
    decoded = codec.decode(codec.encode(x))
    assert_roundtrip_shape(x, decoded)


def test_roundtrip_mean_cosine_reasonable() -> None:
    codec = Root()
    vectors = np.random.default_rng(42).standard_normal((200, 8))
    # Normalize inputs; Root is a unit-vector codec.
    vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
    result = run_roundtrip_eval(codec, vectors=vectors)
    # 240 codewords on a 7-sphere — expected mean cosine is around 0.84.
    assert result.mean_cos >= 0.80, result.summary()


def test_encode_returns_single_byte(rng: np.random.Generator) -> None:
    codec = Root()
    code = codec.encode(rng.standard_normal(8))
    assert code.shape == (1,)
    assert code.dtype == np.uint8


def test_invalid_index_raises(rng: np.random.Generator) -> None:
    codec = Root()
    with pytest.raises(ValueError):
        codec.decode(np.array([240], dtype=np.uint8))
