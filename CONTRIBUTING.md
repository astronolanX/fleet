# Contributing to Fleet

Fleet is a curated shelf. Contributions are welcome when they help readers learn something — a clean reference implementation, a useful harness, a short writeup that illuminates a technique.

## What makes a good Fleet contribution

A codec or pattern belongs in Fleet if:

- It is **public prior art** (a published technique) or a **deliberately simplified demonstration**
- It has a clean, readable reference implementation — clarity over speed
- It comes with a short README explaining what it is, when to use it, and its caveats
- It is **safe to publish** — no production tuning, no proprietary datasets, no benchmark numbers against private work
- It is **tested** against the Fleet testing harness where reasonable

## Adding a codec

1. Copy `fleet_codecs/_template/` to `fleet_codecs/<your-codec-name>/`
2. Fill in the four files: `README.md`, `codec.py`, `demo.py`, `notes.md`
3. Add a test file under `tests/test_<your-codec-name>.py` using `fleet_testing`:

   ```python
   from fleet_codecs.<your_codec> import YourCodec
   from fleet_testing import Codec, run_roundtrip_eval

   def test_implements_codec_protocol():
       assert isinstance(YourCodec(dim=32), Codec)

   def test_roundtrip_cosine():
       result = run_roundtrip_eval(YourCodec(dim=64), n=200)
       assert result.mean_cos >= 0.8, result.summary()
   ```

4. Run `pytest` locally and confirm all tests pass
5. Add your codec to the table in `README.md` and `fleet_codecs/README.md`
6. Open a PR with a short description of why this codec is worth sharing and any prior art it builds on

## Style

- **Plain language** in READMEs — write for the reader, not for the author
- **Attribution matters** — cite the paper, repo, or standard behind a technique
- **Be honest about limitations** — every codec has regimes where it struggles; say so
- **No hype** — no "revolutionary," "first-of-its-kind," or similar superlatives

## What not to contribute

- Codecs that require private datasets or proprietary tuning
- Benchmark comparisons against codecs whose performance numbers are private
- Firmware or embedded ports tied to proprietary targets
- Forks of existing codecs that add tuning or optimizations without explanation

When in doubt, open an issue first and propose the contribution — a short discussion is cheaper than a rejected PR.

## License

All contributions are accepted under Apache-2.0, including its patent-grant clause.
