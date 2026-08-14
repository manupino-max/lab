"""M2 mode-based selective LEACE H20 experiment.

Uses the official concept-erasure LEACE implementation as the linear-erasure
reference. The proposed variant keeps the fitted LEACE protected direction but
applies its full linear erasure only to H=20 samples whose protected-direction
scores fall outside the empirical common-support interval of the two groups.

Mode is estimated in 1-D on the protected-direction scores with a fixed KDE grid.
The modal score is used to anchor the group-specific location; the intervention
selection itself is support-exclusion based, not tuned on test fairness.

Train-only fit/selection; held-out test metrics.
"""
from __future__ import annotations

import json, hashlib, platform, subprocess, sys
from pathlib import Path

import numpy as np
import torch
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import roc_auc_score, balanced_accuracy_score
from scipy.stats import gaussian_kde

from concept_erasure import LeaceEraser

SEEDS = list(range(20))
H = 20
D = 32
N = 1200
TEST_SIZE = 0.30
GRID_Q = (0.01, 0.99)
EPS = 0.02

OUT = Path("results/M2_LEACE_MODE_H20_20260814")
OUT.mkdir(parents=True, exist_ok=True)


def oriented_auc(y_true, score):
    auc = roc_auc_score(y_true, score)
    return max(float(auc), 1.0 - float(auc))


def fit_mode_1d(values: np.ndarray) -> float:
    values = np.asarray(values, dtype=float)
    if np.std(values) < 1e-12:
        return float(np.mean(values))
    kde = gaussian_kde(values)
    lo, hi = np.quantile(values, GRID_Q)
    grid = np.linspace(lo, hi, 2048)
    dens = kde(grid)
    return float(grid[int(np.argmax(dens))])


def make_data(seed: int):
    rng = np.random.default_rng(seed)
    g = np.r_[np.zeros(N//2, dtype=int), np.ones(N//2, dtype=int)]
    z = rng.normal(size=D)
    z /= np.linalg.norm(z)
    task = rng.normal(size=D)
    task -= task @ z * z
    task /= np.linalg.norm(task)
    X = rng.normal(size=(N, D))
    X += g[:, None] * 2.0 * z
    yscore = X @ task + rng.normal(0, 0.8, N)
    y = (yscore > np.median(yscore)).astype(int)
    return X, g, y


def eval_metrics(Xtr, Xte, gtr, gte, ytr, yte):
    lin = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xtr, gtr)
    rbf = make_pipeline(StandardScaler(), SVC(kernel="rbf", C=1, probability=True)).fit(Xtr, gtr)
    task = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(Xtr, ytr)
    sg = lin.predict_proba(Xte)[:, 1]
    rg = rbf.predict_proba(Xte)[:, 1]
    sy = task.predict_proba(Xte)[:, 1]
    return {
        "auc_g_linear": oriented_auc(gte, sg),
        "ba_g_linear": balanced_accuracy_score(gte, sg >= 0.5),
        "auc_g_rbf": oriented_auc(gte, rg),
        "auc_y": roc_auc_score(yte, sy),
    }


def selective_mode_eraser(Xtr, gtr, H=20):
    Xtr_t = torch.from_numpy(Xtr.astype(np.float32))
    gtr_t = torch.from_numpy(gtr.astype(np.int64))
    eraser = LeaceEraser.fit(Xtr_t, gtr_t)
    P = eraser.P.detach().cpu().numpy()
    mu = eraser.bias.detach().cpu().numpy() if eraser.bias is not None else Xtr.mean(0)
    full = (Xtr - mu) @ P.T + mu
    delta = Xtr[gtr == 1].mean(0) - Xtr[gtr == 0].mean(0)
    delta /= max(np.linalg.norm(delta), 1e-12)
    scores = Xtr @ delta
    modes = {0: fit_mode_1d(scores[gtr == 0]), 1: fit_mode_1d(scores[gtr == 1])}
    qs = {g: np.quantile(scores[gtr == g], [0.01, 0.99]) for g in [0,1]}
    lo = max(qs[0][0], qs[1][0])
    hi = min(qs[0][1], qs[1][1])
    outside = np.flatnonzero((scores < lo) | (scores > hi))
    # Prefer points farthest from the common-support interval, then deterministically
    # break ties by distance to the nearest group mode.
    dist_support = np.maximum(lo - scores[outside], scores[outside] - hi)
    dist_mode = np.minimum(np.abs(scores[outside] - modes[0]), np.abs(scores[outside] - modes[1]))
    order = np.lexsort((-dist_mode, -dist_support))
    chosen = outside[order[:min(H, len(outside))]]
    return eraser, P, mu, delta, modes, (lo, hi), chosen, full


def apply_selective(X, mu, P, chosen):
    Xout = X.copy()
    Xfull = (X - mu) @ P.T + mu
    Xout[chosen] = Xfull[chosen]
    return Xout


def run(seed: int):
    X, g, y = make_data(seed)
    idx = np.arange(N)
    train, test = train_test_split(idx, test_size=TEST_SIZE, random_state=seed, stratify=g)
    space, probe_test = train_test_split(train, test_size=0.35, random_state=seed+1000, stratify=g[train])
    # Baseline and proposed transformation are fitted/selected using TRAIN only.
    eraser, P, mu, delta, modes, support, chosen, full_train = selective_mode_eraser(X[space], g[space], H=H)
    # Build a held-out transformed representation with the same H20-selection rule
    # transferred via train-derived protected direction/support; select test points
    # by their train-derived support criterion, without using test metrics.
    scores_test = X[test] @ delta
    lo, hi = support
    outside_test = np.flatnonzero((scores_test < lo) | (scores_test > hi))
    dist_support = np.maximum(lo - scores_test[outside_test], scores_test[outside_test] - hi)
    dist_mode = np.minimum(np.abs(scores_test[outside_test] - modes[0]), np.abs(scores_test[outside_test] - modes[1]))
    order = np.lexsort((-dist_mode, -dist_support))
    chosen_test = outside_test[order[:min(H, len(outside_test))]]
    X_mode = apply_selective(X[test], mu, P, chosen_test)
    X_space_full = (X[space] - mu) @ P.T + mu
    X_test_full = (X[test] - mu) @ P.T + mu
    raw = eval_metrics(X[probe_test], X[test], g[probe_test], g[test], y[probe_test], y[test])
    mode = eval_metrics(X[probe_test], X_mode, g[probe_test], g[test], y[probe_test], y[test])
    full = eval_metrics(X[space], X_test_full, g[space], g[test], y[space], y[test])
    return {
        "seed": seed,
        "H": H,
        "n_train": len(space),
        "n_test": len(test),
        "n_selected_test": int(len(chosen_test)),
        "support_lo": float(lo), "support_hi": float(hi),
        "mode_g0": float(modes[0]), "mode_g1": float(modes[1]),
        **{f"raw_{k}": float(v) for k,v in raw.items()},
        **{f"mode_{k}": float(v) for k,v in mode.items()},
        **{f"full_leace_{k}": float(v) for k,v in full.items()},
        "mode_delta_auc_g_linear": float(mode["auc_g_linear"] - raw["auc_g_linear"]),
        "mode_delta_auc_y": float(mode["auc_y"] - raw["auc_y"]),
        "full_delta_auc_g_linear": float(full["auc_g_linear"] - raw["auc_g_linear"]),
        "full_delta_auc_y": float(full["auc_y"] - raw["auc_y"]),
    }


rows = [run(s) for s in SEEDS]
with (OUT / "results.json").open("w", encoding="utf-8") as f:
    json.dump(rows, f, indent=2)

summary = {
    "experiment": "M2-LEACE-MODE-H20-20260814",
    "library": "EleutherAI/concept-erasure",
    "library_entrypoint": "concept_erasure.LeaceEraser.fit",
    "seeds": SEEDS,
    "H": H,
    "D": D,
    "n": N,
    "criterion": "20 selected points outside train-derived common support on protected LEACE direction; mode from 1-D KDE",
    "results": rows,
}
with (OUT / "summary.json").open("w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2)
for p in sorted(OUT.iterdir()):
    if p.is_file():
        print(p.name, hashlib.sha256(p.read_bytes()).hexdigest())
print(json.dumps({k: summary[k] for k in ["experiment","library","H","D","n"]}, indent=2))
