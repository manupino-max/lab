"""Clean-room canonical LEACE replication harness for M4.

Exploratory only until executed and audited. Uses the canonical
`concept_erasure` implementation rather than a hand-written projection.
Outputs are deliberately separate from historical experiment files.

The harness records baseline-vs-LEACE protected leakage because an absolute
post-LEACE AUC* is not enough to quantify mitigation effect.
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


def make_data(seed, n=800, d=12):
    rng = np.random.default_rng(seed)
    g = rng.integers(0, 2, n)
    x = rng.normal(size=(n, d))
    x[:, 0] += 1.0 * g
    x[:, 1] += 0.8 * (g - 0.5) ** 2
    x[:, 2] += 0.6 * (g - 0.5) * np.abs(x[:, 3])
    y = (x[:, 4] + 0.8 * g + rng.normal(size=n) > 0).astype(int)
    return x, g, y


def oriented_auc(y, score):
    a = roc_auc_score(y, score)
    return max(a, 1.0 - a)


def probe_metrics(x_train, g_train, x_test, g_test, y_train, y_test):
    lin = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(x_train, g_train)
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True)).fit(x_train, g_train)
    task = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(x_train, y_train)
    p_lin = lin.predict_proba(x_test)[:, 1]
    p_rbf = rbf.predict_proba(x_test)[:, 1]
    p_task = task.predict_proba(x_test)[:, 1]
    pred_lin = (p_lin >= 0.5).astype(int)
    pred_task = (p_task >= 0.5).astype(int)
    return {
        "linear_auc_oriented": oriented_auc(g_test, p_lin),
        "linear_balanced_accuracy": balanced_accuracy_score(g_test, pred_lin),
        "nonlinear_auc_oriented": oriented_auc(g_test, p_rbf),
        "utility_auc": roc_auc_score(y_test, p_task),
        "utility_accuracy": accuracy_score(y_test, pred_task),
    }


def run(seed=42):
    from concept_erasure import LeaceEraser
    x, g, y = make_data(seed)
    tr, te = train_test_split(np.arange(len(g)), test_size=0.35,
                              random_state=seed, stratify=g)
    raw = probe_metrics(x[tr], g[tr], x[te], g[te], y[tr], y[te])
    xt = torch.from_numpy(x[tr]).float()
    gt = torch.from_numpy(g[tr]).long()
    eraser = LeaceEraser.fit(xt, gt)
    ztr = eraser(xt).detach().numpy()
    zte = eraser(torch.from_numpy(x[te]).float()).detach().numpy()
    post = probe_metrics(ztr, g[tr], zte, g[te], y[tr], y[te])
    return {
        "seed": seed, "n": len(g), "d": x.shape[1],
        "raw_linear_auc_oriented": raw["linear_auc_oriented"],
        "post_linear_auc_oriented": post["linear_auc_oriented"],
        "delta_linear_auc_oriented": post["linear_auc_oriented"] - raw["linear_auc_oriented"],
        "raw_linear_balanced_accuracy": raw["linear_balanced_accuracy"],
        "post_linear_balanced_accuracy": post["linear_balanced_accuracy"],
        "raw_nonlinear_auc_oriented": raw["nonlinear_auc_oriented"],
        "post_nonlinear_auc_oriented": post["nonlinear_auc_oriented"],
        "delta_nonlinear_auc_oriented": post["nonlinear_auc_oriented"] - raw["nonlinear_auc_oriented"],
        "raw_utility_auc": raw["utility_auc"],
        "post_utility_auc": post["utility_auc"],
        "delta_utility_auc": post["utility_auc"] - raw["utility_auc"],
        "raw_utility_accuracy": raw["utility_accuracy"],
        "post_utility_accuracy": post["utility_accuracy"],
    }


if __name__ == "__main__":
    seeds = [11, 22, 33, 42, 55]
    rows = [run(s) for s in seeds]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "seed_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    summary = {
        "status": "exploratory_pending_audit",
        "seeds": seeds,
        "n_runs": len(rows),
        "mean_raw_linear_auc_oriented": float(np.mean([r["raw_linear_auc_oriented"] for r in rows])),
        "mean_post_linear_auc_oriented": float(np.mean([r["post_linear_auc_oriented"] for r in rows])),
        "mean_delta_linear_auc_oriented": float(np.mean([r["delta_linear_auc_oriented"] for r in rows])),
        "mean_raw_nonlinear_auc_oriented": float(np.mean([r["raw_nonlinear_auc_oriented"] for r in rows])),
        "mean_post_nonlinear_auc_oriented": float(np.mean([r["post_nonlinear_auc_oriented"] for r in rows])),
        "mean_delta_nonlinear_auc_oriented": float(np.mean([r["delta_nonlinear_auc_oriented"] for r in rows])),
        "mean_raw_utility_auc": float(np.mean([r["raw_utility_auc"] for r in rows])),
        "mean_post_utility_auc": float(np.mean([r["post_utility_auc"] for r in rows])),
        "mean_delta_utility_auc": float(np.mean([r["delta_utility_auc"] for r in rows])),
        "python": platform.python_version(),
        "torch": torch.__version__,
        "numpy": np.__version__,
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
