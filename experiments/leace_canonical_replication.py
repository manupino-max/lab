"""Clean-room canonical LEACE replication harness for M4.

Exploratory only until executed and audited. Uses the public synthetic generator
and the canonical `concept_erasure` implementation rather than a hand-written
projection. Outputs are deliberately separate from historical experiment files.
"""
from pathlib import Path
import csv, json
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


def run(seed=42):
    from concept_erasure import LeaceEraser

    x, g, y = make_data(seed)
    tr, te = train_test_split(np.arange(len(g)), test_size=0.35,
                              random_state=seed, stratify=g)
    xt = torch.from_numpy(x[tr]).float()
    gt = torch.from_numpy(g[tr]).long()
    eraser = LeaceEraser.fit(xt, gt)
    ztr = eraser(xt).detach().numpy()
    zte = eraser(torch.from_numpy(x[te]).float()).detach().numpy()

    lin = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(ztr, g[tr])
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", probability=True)).fit(ztr, g[tr])
    task = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(ztr, y[tr])

    p_lin = lin.predict_proba(zte)[:, 1]
    p_rbf = rbf.predict_proba(zte)[:, 1]
    p_task = task.predict_proba(zte)[:, 1]
    pred_lin = (p_lin >= 0.5).astype(int)
    pred_task = (p_task >= 0.5).astype(int)

    return {
        "seed": seed,
        "n": len(g),
        "d": x.shape[1],
        "linear_auc_oriented": oriented_auc(g[te], p_lin),
        "linear_balanced_accuracy": balanced_accuracy_score(g[te], pred_lin),
        "nonlinear_auc_oriented": oriented_auc(g[te], p_rbf),
        "utility_auc": roc_auc_score(y[te], p_task),
        "utility_accuracy": accuracy_score(y[te], pred_task),
    }


if __name__ == "__main__":
    rows = [run(s) for s in [11, 22, 33, 42, 55]]
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "seed_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    summary = {
        "status": "exploratory_pending_audit",
        "seeds": [r["seed"] for r in rows],
        "mean_linear_auc_oriented": float(np.mean([r["linear_auc_oriented"] for r in rows])),
        "mean_nonlinear_auc_oriented": float(np.mean([r["nonlinear_auc_oriented"] for r in rows])),
        "mean_utility_auc": float(np.mean([r["utility_auc"] for r in rows])),
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))
