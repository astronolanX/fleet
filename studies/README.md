# Studies

A study is a short, reproducible investigation into how a codec behaves — when it works, when it breaks, what it looks like at the edges. Each study is one folder, one command, one plot or table, one honest conclusion.

Studies in Fleet have the same shape every time:

```
studies/<name>/
├── README.md     # the question, the method, the result, the conclusion
├── run.py        # a single runnable script that reproduces the finding
└── notes.md      # optional deeper notes on the math, alternatives, caveats
```

A reader should be able to clone the repo, install it, and run:

```bash
python -m studies.<name>.run
```

...in under sixty seconds, and see the numbers or plot that back up the study's conclusion.

## What belongs here

- **Characterizations** — "this codec scallops at 45°"; "this codec floors at a fixed cosine in D=8"
- **Regime maps** — "codec X works well here and fails here, and here's why"
- **Methodology notes** — "this metric misses that property"; "this baseline is misleading"
- **Honest negative results** — "we expected X, got Y, here's what that tells us"

## What doesn't belong here

- Horse-race leaderboards between codecs
- Findings that require private data or private codecs to reproduce
- Results whose mechanism you can't explain before running the code

## What's here

*(No studies yet.)*

The first study will be added when a finding is picked, piloted, and confirmed to reproduce cleanly.

## Adding a study

See [CONTRIBUTING.md](../CONTRIBUTING.md) in the repo root. The short version:

1. Copy `studies/_template/` to `studies/<your-study-name>/`
2. Fill in `run.py`, `README.md`, and (optionally) `notes.md`
3. Make sure `python -m studies.<name>.run` completes in under sixty seconds with deterministic output
4. Add your study to the list above and open a PR

## Related

- [`../codecs/`](../codecs/) — the codecs these studies investigate
- [`../testing/`](../testing/) — shared harness primitives available to studies
