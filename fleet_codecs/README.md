# Codecs

Each codec in Fleet lives in its own folder and follows the same layout:

```
fleet_codecs/<name>/
├── README.md     # what it is, when to use it, how to run the demo, caveats
├── codec.py      # a clean reference implementation
├── demo.py       # a short runnable demonstration
└── notes.md      # optional deeper write-up (math, prior art, intuition)
```

The shape is the same everywhere so that reading one codec teaches you how to read the next.

## What's here

| Codec | Folder | One-liner |
|---|---|---|
| TurboQuant | [turboquant/](turboquant/) | Randomized-rotation scalar quantization that preserves inner products |
| Root | [root/](root/) | Angular quantization against the 240 minimal vectors of E8 |
| Compass | [compass/](compass/) | Sign-pattern heading + magnitude payload, direction and magnitude as separate code fields |
| Drift | [drift/](drift/) | Base + tangent-space quantization — pick the nearest prototype, refine locally |

## Adding a codec

See [CONTRIBUTING.md](../CONTRIBUTING.md) in the repo root. The short version:

1. Copy `fleet_codecs/_template/` to `fleet_codecs/<your-codec-name>/`
2. Fill in the four files
3. Make sure `python -m fleet_codecs.<name>.demo` runs and produces sensible output
4. Open a PR with a short description of why this codec is worth sharing
