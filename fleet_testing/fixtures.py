"""Pytest fixtures for codec testing.

Drop `from fleet_testing.fixtures import *` into a `conftest.py` to pick
these up. They are not registered globally — opt-in per test module.
"""

from __future__ import annotations

import numpy as np
import pytest

from .generators import gaussian_vectors, unit_vectors


@pytest.fixture
def rng() -> np.random.Generator:
    """A deterministic numpy Generator seeded with 42."""
    return np.random.default_rng(42)


@pytest.fixture
def small_gaussian_batch(rng: np.random.Generator) -> np.ndarray:
    """A (16, 64) batch of Gaussian vectors."""
    return gaussian_vectors(16, 64, rng=rng)


@pytest.fixture
def small_unit_batch(rng: np.random.Generator) -> np.ndarray:
    """A (16, 64) batch of unit-norm vectors."""
    return unit_vectors(16, 64, rng=rng)
