"""M2 P0 canonical LEACE clean-room matrix.

Uses the pinned canonical concept_erasure.LeaceEraser implementation.
This branch is an execution bridge only; it does not replace M2 evidence
until provenance/audit gates are closed.
"""
from pathlib import Path
import csv, json, platform
import numpy as np
import torch
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, balanced_accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

OUT = Path(__file__).resolve().parent / "results" / "leace_canonical_replication"
SEEDS = list(range(20))
DIMS = [8, 16, 32, 64, 128]
INTENSITIES = [0.25, 0.5, 1.0, 2.0, 4.0]


def make_data(seed, d, intensity, n0=500, n1=500):
    rng = np.random.default_rng(seed)
    z = np.r_[np.zeros(n0, dtype=int), np.ones(n1, dtype=int)]
    y_signal = rng.normal(size=n0 + n1)
    y = (y_signal > 0).astype(int)
    x = rng.normal(size=(n0 + n1, d))
    x[:, 0] += intensity * z
    x[:, 1] += y_signal
    return x, z, y


def auc_star(y, score):
    a = roc_auc_score(y, score)
    return max(a, 1.0 - a), a


def probe_metrics(x_train, g_train, x_test, g_test, y_train, y_test, seed):
    lin = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed)).fit(x_train, g_train)
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True, random_state=seed)).fit(x_train, g_train)
    task = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000, random_state=seed)).fit(x_train, y_train)

    p_lin = lin.predict_proba(x_test)[:, 1]
    p_rbf = rbf.predict_proba(x_test)[:, 1]
    p_task = task.predict_proba(x_test)[:, 1]
    a_lin, raw_lin = auc_star(g_test, p_lin)
    a_rbf, raw_rbf = auc_star(g_test, p_rbf)
    pred_lin = (p_lin >= 0.5).astype(int)
    pred_task = (p_task >= 0.5).astype(int)
    return {
        "linear_auc_star": a_lin,
        "linear_auc_raw": raw_lin,
        "linear_balanced_accuracy": balanced_accuracy_score(g_test, pred_lin),
        "nonlinear_auc_star": a_rbf,
        "nonlinear_auc_raw": raw_rbf,
        "utility_auc": roc_auc_score(y_test, p_task),
        "utility_accuracy": accuracy_score(y_test, pred_task),
    }


def run(seed, d, intensity):
    from concept_erasure import LeaceEraser

    x, g, y = make_data(seed, d, intensity)
    idx = np.arange(len(g))
    space_train, rem = train_test_split(idx, test_size=0.4, random_state=seed, stratify=g)
    probe_train, test = train_test_split(rem, test_size=0.5, random_state=seed + 1000, stratify=g[rem])

    raw = probe_metrics(x[probe_train], g[probe_train], x[test], g[test], y[probe_train], y[test], seed)

    xt = torch.from_numpy(x[space_train]).float()
    gt = torch.from_numpy(g[space_train]).long()
    eraser = LeaceEraser.fit(xt, gt)
    z = eraser(torch.from_numpy(x).float()).detach().numpy()
    post = probe_metrics(z[probe_train], g[probe_train], z[test], g[test], y[probe_train], y[test], seed + 500000)

    return {
        "seed": seed, "D": d, "intensity": intensity,
        "raw_linear_auc_star": raw["linear_auc_star"],
        "post_linear_auc_star": post["linear_auc_star"],
        "delta_linear_auc_star": post["linear_auc_star"] - raw["linear_auc_star"],
        "post_linear_balanced_accuracy": post["linear_balanced_accuracy"],
        "raw_nonlinear_auc_star": raw["nonlinear_auc_star"],
        "post_nonlinear_auc_star": post["nonlinear_auc_star"],
        "delta_nonlinear_auc_star": post["nonlinear_auc_star"] - raw["nonlinear_auc_star"],
        "raw_utility_auc": raw["utility_auc"],
        "post_utility_auc": post["utility_auc"],
        "delta_utility_auc": post["utility_auc"] - raw["utility_auc"],
        "raw_utility_accuracy": raw["utility_accuracy"],
        "post_utility_accuracy": post["utility_accuracy"],
    }


if __name__ == "__main__":
    rows = [run(seed, d, intensity) for d in DIMS for intensity in INTENSITIES for seed in SEEDS]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "matrix_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    summary = {
        "status": "exploratory_pending_audit",
        "n_runs": len(rows),
        "seeds": SEEDS,
        "dims": DIMS,
        "intensities": INTENSITIES,
        "mean_raw_linear_auc_star": float(np.mean([r["raw_linear_auc_star"] for r in rows])),
        "mean_post_linear_auc_star": float(np.mean([r["post_linear_auc_star"] for r in rows])),
        "mean_delta_linear_auc_star": float(np.mean([r["delta_linear_auc_star"] for r in rows])),
        "mean_post_linear_balanced_accuracy": float(np.mean([r["post_linear_balanced_accuracy"] for r in rows])),
        "mean_raw_nonlinear_auc_star": float(np.mean([r["raw_nonlinear_auc_star"] for r in rows])),
        "mean_post_nonlinear_auc_star": float(np.mean([r["post_nonlinear_auc_star"] for r in rows])),
        "mean_delta_nonlinear_auc_star": float(np.mean([r["delta_nonlinear_auc_star"] for r in rows])),
        "mean_raw_utility_auc": float(np.mean([r["raw_utility_auc"] for r in rows])),
        "mean_post_utility_auc": float(np.mean([r["post_utility_auc"] for r in rows])),
        "mean_delta_utility_auc": float(np.mean([r["delta_utility_auc"] for r in rows])),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "numpy": np.__version__,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
