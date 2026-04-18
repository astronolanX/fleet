"""Fleet testing SDK.

A small, public testing harness for codecs in the Fleet gallery. Provides
a common Protocol, reproducible generators, structured assertions, a
roundtrip evaluation runner, and pytest fixtures — so every codec gets
tested the same way.

Public surface:

    from fleet_testing import (
        Codec,                       # Protocol every Fleet codec implements
        gaussian_vectors,            # reproducible Gaussian generator
        unit_vectors,                # reproducible unit-norm generator
        assert_cosine_above,
        assert_roundtrip_shape,
        run_roundtrip_eval,
        RoundtripResult,
    )

See fleet_testing/README.md for details.
"""

from .assertions import assert_cosine_above, assert_roundtrip_shape
from .generators import gaussian_vectors, unit_vectors
from .harness import RoundtripResult, run_roundtrip_eval
from .protocol import Codec

__all__ = [
    "Codec",
    "RoundtripResult",
    "assert_cosine_above",
    "assert_roundtrip_shape",
    "gaussian_vectors",
    "run_roundtrip_eval",
    "unit_vectors",
]
