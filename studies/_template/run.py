"""Runnable script for <StudyName>.

Run with:
    python -m studies.<name>.run

Should complete in under sixty seconds and print or plot the result
that backs up the study's conclusion. Deterministic — seed anything
that uses randomness.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(42)
    # Your study code here.
    _ = rng
    print("StudyName — replace this with the study's output.")


if __name__ == "__main__":
    main()
