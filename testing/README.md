# Testing harness

A small testing harness for codecs in the Fleet gallery.

The goal is modest: every codec here should be testable the same way, with the same primitives, so reading one test file teaches you how to read the next.

## What's inside

| Module | Contents |
|---|---|
| `protocol.py` | The `Codec` Protocol — structural typing, `runtime_checkable` |
| `generators.py` | Reproducible `gaussian_vectors`, `unit_vectors` |
| `assertions.py` | `assert_cosine_above`, `assert_roundtrip_shape` — structured failure messages |
| `harness.py` | `run_roundtrip_eval(codec)` → `RoundtripResult` with percentile summary |
| `fixtures.py` | Opt-in pytest fixtures: `rng`, `small_gaussian_batch`, `small_unit_batch` |

## Quick start

```python
import numpy as np
from codex.turboquant import TurboQuant
from testing import run_roundtrip_eval, assert_cosine_above

codec = TurboQuant(dim=64, bits_per_coord=2)
result = run_roundtrip_eval(codec, n=100)
print(result.summary())
assert_cosine_above(
    original=np.zeros((1, 64)),  # or real batch
    decoded=np.zeros((1, 64)),   # or real batch
    threshold=0.85,
)
```

## Using the fixtures

In a test file's `conftest.py`:

```python
from testing.fixtures import *  # noqa: F401,F403
```

Then in tests:

```python
def test_my_codec(rng, small_gaussian_batch):
    ...
```

## Design notes

- The harness **reports**, it does not judge. It returns numbers. If you want pass/fail gates, apply an assertion to the returned numbers.
- Failure messages follow a fixed shape so they are easy to scan and grep:
  `ASSERT FAILED | <function> | <measured>=<value> < <threshold>=<value>`
- Nothing here depends on private datasets, benchmark fixtures, or production tuning from upstream research. This harness is intentionally lean.

## What's not here

- No benchmarking runner against real datasets (out of scope for a public gallery)
- No BER sweeps, adversarial tests, or domain-adaptation harnesses
- No cross-codec matched-bitrate comparison harness

If Fleet grows and needs any of that, it gets added as its own module — not by widening this one.

## Related

- [`../codecs/`](../codecs/) — the codec gallery this harness tests
- [`../studies/`](../studies/) — studies that use these primitives
- [`../tests/`](../tests/) — pytest suite exercising each codec against the harness
