# Tests

Pytest suite for Fleet. Each codec has its own test file that exercises it against the shared testing harness in `fleet_testing/`.

## Layout

```
tests/
├── conftest.py            # registers the fleet_testing pytest fixtures
├── test_turboquant.py     # tests for the TurboQuant codec
├── test_root.py           # tests for the Root codec
├── test_compass.py        # tests for the Compass codec
└── test_drift.py          # tests for the Drift codec
```

## Running

```bash
pytest
```

...or to run a single codec's tests:

```bash
pytest tests/test_root.py -v
```

## What a codec test checks

Every codec in Fleet gets at least the following coverage:

- **Protocol conformance** — `isinstance(codec, fleet_testing.Codec)`
- **Roundtrip shape** — encoded then decoded vector has the same shape as input
- **Roundtrip cosine** — reconstruction reaches a known threshold on the harness's Gaussian batch
- **Input validation** — bad arguments raise the expected errors

The threshold in the roundtrip-cosine check is **calibrated to what the codec actually delivers**, not to aspirational numbers. If a threshold fails, the fix is to either fix the codec or — if the codec is correct — lower the threshold to reflect reality.

## Adding tests for a new codec

When you add a codec under `fleet_codecs/<name>/`, add `tests/test_<name>.py` following the pattern of the existing test files:

```python
from fleet_codecs.<name> import YourCodec
from fleet_testing import Codec, run_roundtrip_eval


def test_implements_codec_protocol():
    assert isinstance(YourCodec(dim=32), Codec)


def test_roundtrip_cosine():
    result = run_roundtrip_eval(YourCodec(dim=64), n=200)
    assert result.mean_cos >= 0.8, result.summary()
```

Run the tests locally and confirm they pass before opening a PR.

## Studies are tested too

Studies in `fleet_studies/` don't need exhaustive test files, but each study's `run.py` must be **deterministic** — same seed, same output, every time. If a study's numbers drift between runs, seed whatever is random and document it in the study's README.

## Related

- [`../fleet_codecs/`](../fleet_codecs/) — the codec gallery under test
- [`../fleet_testing/`](../fleet_testing/) — the harness these tests are written against
- [`../fleet_studies/`](../fleet_studies/) — short investigations
