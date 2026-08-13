from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"
OUT.mkdir(parents=True, exist_ok=True)

SURFACES = ["plane", "paraboloid", "cylinder", "sphere"]
SEEDS = [0, 1]
N_VALUES = [50, 100]
NOISES = [0.0, 0.01]
KS = [5, 10]


def sample_surface(name: str, n: int, rng: np.random.Generator) -> np.ndarray:
    if name == "plane":
        xy = rng.uniform(-0.5, 0.5, (n, 2))
        return np.c_[xy, np.zeros(n)]
    if name == "paraboloid":
        xy = rng.uniform(-0.5, 0.5, (n, 2))
        return np.c_[xy, (xy[:, 0] ** 2 + xy[:, 1] ** 2) / 2.0]
    if name == "cylinder":
        theta = rng.uniform(-0.5, 0.5, n)
        y = rng.uniform(-0.5, 0.5, n)
        return np.c_[np.cos(theta), y, np.sin(theta)]
    if name == "sphere":
        uv = rng.uniform(-0.4, 0.4, (n, 2))
        x = np.sqrt(np.maximum(1.0 - np.sum(uv ** 2, axis=1), 0.0))
        return np.c_[x, uv]
    raise ValueError(name)


def estimate(points: np.ndarray, k: int) -> float:
    center = points[np.argmin(np.sum(points ** 2, axis=1))]
    q = points - center
    d2 = np.sum(q[:, :2] ** 2, axis=1)
    idx = np.argsort(d2)[:k]
    uv, z = q[idx, :2], q[idx, 2]
    A = np.c_[uv[:, 0] ** 2, uv[:, 0] * uv[:, 1], uv[:, 1] ** 2,
              uv[:, 0], uv[:, 1], np.ones(len(idx))]
    coef, *_ = np.linalg.lstsq(A, z, rcond=None)
    return float(np.sqrt(np.mean((A @ coef - z) ** 2)))


def main() -> None:
    rows = []
    for surface in SURFACES:
        for n in N_VALUES:
            for sigma in NOISES:
                for seed in SEEDS:
                    rng = np.random.default_rng(seed)
                    clean = sample_surface(surface, n, rng)
                    points = clean + rng.normal(0.0, sigma, clean.shape)
                    for k in KS:
                        rows.append({
                            "surface": surface,
                            "N": n,
                            "noise_sigma": sigma,
                            "seed": seed,
                            "k": k,
                            "fit_rmse": estimate(points, k),
                        })

    path = OUT / "fixture_results.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} synthetic records")
    print(path)


if __name__ == "__main__":
    main()
