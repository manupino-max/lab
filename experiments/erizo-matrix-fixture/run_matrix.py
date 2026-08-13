from __future__ import annotations
import json, os
from pathlib import Path

import numpy as np


def run(seed: int, condition: str) -> dict:
    rng = np.random.default_rng(seed)
    x = rng.normal(size=(256, 8))
    if condition == "translation":
        y = x + 0.5
    elif condition == "anisotropic_scale":
        y = x * np.array([1.0, 1.1, 0.9, 1.2, 1.0, 0.8, 1.05, 0.95])
    elif condition == "shear":
        y = x.copy()
        y[:, 1] += 0.25 * x[:, 0]
    else:
        y = x.copy()
    mse = float(np.mean((x - y) ** 2))
    return {"seed": seed, "condition": condition, "n": len(x), "mse": mse}


if __name__ == "__main__":
    seed = int(os.environ["SEED"])
    condition = os.environ["CONDITION"]
    out = Path(os.environ.get("OUTPUT", "result.json"))
    out.write_text(json.dumps(run(seed, condition), indent=2) + "\n", encoding="utf-8")
    print(out.read_text())
