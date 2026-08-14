"""Auditable provisional Pi x Fi smoke calculation.

IMPORTANT: this is NOT the M2 scientific result. It reconstructs the previously
used public synthetic P03-style classification smoke from its documented
parameters and computes a task-performance/fairness view. It must not be
promoted to M2 Results until M2's canonical protocol and evidence gate are met.
"""
from pathlib import Path
import csv, json
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "results" / "pifi_smoke"
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = [11, 22, 33, 44, 55]
LAMBDAS = np.linspace(0, 1, 6)


def one_seed(seed):
    rng = np.random.default_rng(seed)
    n, d = 1200, 10
    s = rng.integers(0, 2, n)
    X = rng.normal(size=(n, d))
    X[:, 0] += 1.8 * s
    y = (X[:, 1] + 0.7 * s + rng.normal(size=n) > 0.5).astype(int)
    tr, te = train_test_split(np.arange(n), test_size=0.35,
                              random_state=seed, stratify=s)
    rows = []
    for lam in LAMBDAS:
        Z = X.copy()
        gm = np.vstack([Z[s == g].mean(0) for g in [0, 1]])
        Z = (1 - lam) * Z + lam * (Z - np.array([gm[g] for g in s]))
        clf = LogisticRegression(max_iter=2000).fit(Z[tr], y[tr])
        pred = (clf.predict_proba(Z[te])[:, 1] >= 0.5).astype(int)
        st, yt = s[te], y[te]
        pred_rate = [pred[st == g].mean() for g in [0, 1]]
        tpr = []
        for g in [0, 1]:
            mask = st == g
            pos = yt[mask] == 1
            tpr.append(((pred[mask] == 1) & pos).sum() / max(pos.sum(), 1))
        rows.append({
            "seed": int(seed), "lambda": float(lam),
            "Pi_accuracy": float(accuracy_score(yt, pred)),
            "DP_gap": float(abs(pred_rate[1] - pred_rate[0])),
            "EO_gap": float(abs(tpr[1] - tpr[0])),
        })
    return rows

rows = [r for seed in SEEDS for r in one_seed(seed)]
with (OUT / "raw_seed_results.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

summary = []
for lam in LAMBDAS:
    rr = [r for r in rows if np.isclose(r["lambda"], lam)]
    acc = np.array([r["Pi_accuracy"] for r in rr])
    dp = np.array([r["DP_gap"] for r in rr])
    eo = np.array([r["EO_gap"] for r in rr])
    # Exploratory scalar only: larger F is better. Primary fairness metrics
    # remain DP_gap and EO_gap and are retained in the CSV.
    F = 1.0 - (dp.mean() + eo.mean()) / 2.0
    summary.append({
        "lambda": float(lam), "Pi_accuracy_mean": float(acc.mean()),
        "Pi_accuracy_sd": float(acc.std(ddof=1)), "DP_gap_mean": float(dp.mean()),
        "EO_gap_mean": float(eo.mean()), "Fi_exploratory": float(F),
    })

with (OUT / "PiFi_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=summary[0].keys()); w.writeheader(); w.writerows(summary)

# SVG is text and therefore auditable in the repository.
svg = ["<svg xmlns='http://www.w3.org/2000/svg' width='900' height='650'>",
       "<rect width='100%' height='100%' fill='white'/>",
       "<text x='450' y='35' text-anchor='middle' font-size='22'>Provisional Pi x Fi — public synthetic smoke</text>",
       "<text x='450' y='625' text-anchor='middle' font-size='16'>Pi: task accuracy</text>",
       "<text x='20' y='325' text-anchor='middle' font-size='16' transform='rotate(-90 20 325)'>Fi: exploratory fairness score</text>"]
xs = [r["Pi_accuracy_mean"] for r in summary]; ys = [r["Fi_exploratory"] for r in summary]
xmin, xmax = min(xs)-0.01, max(xs)+0.01; ymin, ymax = min(ys)-0.01, max(ys)+0.01
for r, x, y in zip(summary, xs, ys):
    px = 90 + (x-xmin)/(xmax-xmin)*750
    py = 560 - (y-ymin)/(ymax-ymin)*470
    svg.append(f"<circle cx='{px:.2f}' cy='{py:.2f}' r='6' fill='black'/>")
    svg.append(f"<text x='{px+10:.2f}' y='{py-8:.2f}' font-size='13'>lambda={r['lambda']:.1f}</text>")
svg.append("</svg>")
(OUT / "PiFi_provisional.svg").write_text("\n".join(svg), encoding="utf-8")

manifest = {
    "status": "completed",
    "scientific_status": "exploratory_public_smoke_only",
    "seeds": SEEDS,
    "lambdas": [float(x) for x in LAMBDAS],
    "primary_task_metric": "accuracy",
    "primary_fairness_metrics": ["DP_gap", "EO_gap"],
    "scalar_fairness_score": "Fi_exploratory = 1 - mean(DP_gap, EO_gap)",
    "promotion": "NOT_ELIGIBLE_FOR_M2_RESULTS",
}
(OUT / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps(manifest, indent=2))
