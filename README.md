# Fleet

A curated showcase of codecs and protocol patterns from [Peripheral Technologies LLC](https://github.com/astronolanX).

Fleet is the public-facing companion to private research on edge-sensor compression — specifically the family of lattice-quantized and rotation-based codecs that compress sensor data into geometric vectors small enough to stream from a microcontroller to a language model.

## What lives here

Fleet publishes:

- **Reference codec implementations** that are either public prior art (e.g., TurboQuant) or simplified demonstrations of a technique.
- **Protocol sketches** — wire formats, MCP bridges, and closed-loop patterns for LLM-to-sensor communication.
- **Benchmarks and harnesses** where the harness itself is the contribution, not the numbers.
- **Notes and writeups** — short reads on ideas worth sharing.

## What does not live here

Fleet is deliberately a curated shelf, not a mirror of upstream work. The following stay private:

- Production codecs and their tuning
- Full performance benchmarks
- Embedded C ports and firmware
- Evidence trails from ongoing research
- Domain-adaptive feature extractors

The goal is to publish enough to be useful and honest, without handing competitors the work that took years to build.

## Why it exists

Small, careful public artifacts help the field more than polished marketing. If you're a researcher, engineer, or someone curious about how language models might one day talk to physical sensors at the codec layer — this repo is meant for you.

## Layout

```
fleet/
├── fleet_codecs/         # the codec gallery, one folder per codec
│   ├── turboquant/
│   └── _template/        # copy this when adding a new codec
├── fleet_testing/        # reusable testing harness (protocol, generators,
│                         # assertions, roundtrip eval, pytest fixtures)
├── tests/                # tests for each codec, written against the harness
├── CLAUDE.md             # guidance for Claude Code sessions in this repo
├── CONTRIBUTING.md       # how to add a codec or propose a change
└── pyproject.toml
```

## Get started

```bash
pip install -e .
python -m fleet_codecs.turboquant.demo
pytest
```

## Codecs in the gallery

| Codec | One-liner |
|---|---|
| [TurboQuant](fleet_codecs/turboquant/) | Randomized-rotation scalar quantization that preserves inner products |

## Adding a codec

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0. Code here is free to use, study, and build on. The patent-grant clause is intentional.

## Contact

Nolan Figueroa — [astronolan on X](https://x.com/astronolan) · [LinkedIn](https://www.linkedin.com/in/astronolan/)
