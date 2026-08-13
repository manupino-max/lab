"""Public synthetic experiment runner.

This is a clean-room execution harness for the public lab. It generates all
inputs at runtime and writes reproducible CSV/JSON artifacts. It intentionally
does not depend on private-repository files or historical results.
"""
from pathlib import Path
import csv, json
import numpy as np

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results"


def surface(kind, n, rng):
    u = rng.uniform(-1, 1, n)
    v = rng.uniform(-1, 1, n)
    if kind == "plane":
        return np.c_[u, v, np.zeros(n)]
    if kind == "saddle":
        return np.c_[u, v, 0.5 * (u*u - v*v)]
    if kind == "paraboloid":
        return np.c_[u, v, 0.5 * (u*u + v*v)]
    if kind == "sphere":
        z = rng.uniform(-0.8, 0.8, n)
        t = rng.uniform(0, 2*np.pi, n)
        r = np.sqrt(1-z*z)
        return np.c_[r*np.cos(t), r*np.sin(t), z]
    if kind == "cylinder":
        t = rng.uniform(0, 2*np.pi, n)
        y = rng.uniform(-1, 1, n)
        return np.c_[np.cos(t), y, np.sin(t)]
    raise ValueError(kind)


def local_fit(points, k):
    center = points.mean(axis=0)
    idx = np.argsort(np.sum((points-center)**2, axis=1))[:k]
    y = points[idx] - points[idx].mean(axis=0)
    _, s, vt = np.linalg.svd(y, full_matrices=False)
    q = y @ vt[:2].T
    z = y @ vt[2]
    A = np.c_[q[:,0]**2, q[:,0]*q[:,1], q[:,1]**2, q[:,0], q[:,1], np.ones(k)]
    coef = np.linalg.lstsq(A, z, rcond=None)[0]
    pred = A @ coef
    return float(np.sqrt(np.mean((pred-z)**2))), float(s[-1]**2 / max(s[-2]**2, 1e-15))


def run(seed=42):
    rng = np.random.default_rng(seed)
    rows = []
    for kind in ["plane", "sphere", "cylinder", "saddle", "paraboloid"]:
        for sigma in [0.0, 0.001, 0.01]:
            x = surface(kind, 1000, rng)
            x = x + rng.normal(0, sigma, x.shape)
            for k in [20, 50, 100]:
                rmse, spectrum_ratio = local_fit(x, k)
                rows.append({"surface": kind, "noise": sigma, "k": k,
                             "fit_rmse": rmse, "spectrum_ratio": spectrum_ratio})
    OUT.mkdir(parents=True, exist_ok=True)
    csv_path = OUT / "public_synthetic_experiments.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    summary = {"seed": seed, "rows": len(rows), "status": "completed",
               "inputs": "generated synthetically at runtime"}
    (OUT / "run_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run()
