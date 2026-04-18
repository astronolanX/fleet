# Fleet

A curated showcase of codecs and protocol patterns from [Peripheral Technologies LLC](https://github.com/astronolanX).

Fleet is the public-facing companion to private research on edge-sensor compression — compressing sensor data into small geometric representations that travel efficiently from a microcontroller to a language model.

## What lives here

Fleet publishes:

- **Reference codec implementations** that are either public prior art (e.g., TurboQuant) or simplified demonstrations of a technique.
- **Studies** — short, reproducible investigations into how a codec behaves.
- **Protocol sketches** — wire formats, MCP bridges, and closed-loop patterns for LLM-to-sensor communication.
- **Harnesses** where the harness itself is the contribution, not the numbers.
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
│   ├── root/
│   ├── compass/
│   ├── drift/
│   └── _template/        # copy this when adding a new codec
├── fleet_studies/        # short, reproducible investigations
│   └── _template/        # copy this when adding a new study
├── fleet_testing/        # reusable testing harness (protocol, generators,
│                         # assertions, roundtrip eval, pytest fixtures)
├── tests/                # tests for each codec, written against the harness
├── CLAUDE.md             # guidance for Claude Code sessions in this repo
├── CONTRIBUTING.md       # how to add a codec, study, or propose a change
└── pyproject.toml
```

Each directory has its own README that explains what lives there and how to add more.

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
| [Root](fleet_codecs/root/) | Angular quantization against the 240 minimal vectors of E8 |
| [Compass](fleet_codecs/compass/) | Sign-pattern heading + magnitude payload, direction and magnitude as separate code fields |
| [Drift](fleet_codecs/drift/) | Base + tangent-space quantization — pick the nearest prototype, refine locally |

## Studies

Short investigations into how codecs behave — when they work, when they break, what they look like at the edges. See [fleet_studies/](fleet_studies/) for the current list and the study template.

## Adding a codec or a study

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

Apache-2.0. Code here is free to use, study, and build on. The patent-grant clause is intentional.

## Contact

Nolan Figueroa — [astronolan on X](https://x.com/astronolan) · [LinkedIn](https://www.linkedin.com/in/astronolan/)
