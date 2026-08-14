"""M4 LEACE-CL: rank-1 linear combination along the maximum-separation direction.

Fits everything on TRAIN only. The test set is used only for final evaluation.
"""
from __future__ import annotations
import numpy as np


def fit_leace_cl(X: np.ndarray, g: np.ndarray, eps: float = 1e-6):
    """Fit a rank-1 linear intervention using the Fisher/LDA maximum-separation direction."""
    x0, x1 = X[g == 0], X[g == 1]
    mu0, mu1 = x0.mean(0), x1.mean(0)
    d = mu1 - mu0
    s0 = np.cov(x0, rowvar=False)
    s1 = np.cov(x1, rowvar=False)
    sw = (s0 * (len(x0)-1) + s1 * (len(x1)-1)) / max(len(X)-2, 1)
    sw = sw + eps * np.eye(X.shape[1])
    w = np.linalg.solve(sw, d)
    # Rank-1 map sends the Fisher-optimal discriminant component into the
    # mean-difference direction. At alpha=1 it removes the group mean contrast.
    denom = float(w @ d)
    P = np.outer(d, w) / max(denom, eps)
    midpoint = 0.5 * (mu0 + mu1)
    return {"mu0": mu0, "mu1": mu1, "d": d, "w": w, "P": P, "midpoint": midpoint}


def transform(X: np.ndarray, g: np.ndarray, fit: dict, alpha: float):
    """Partial group-conditional LEACE-CL, with common midpoint at alpha=1."""
    mu0, mu1, P = fit["mu0"], fit["mu1"], fit["P"]
    target = fit["midpoint"]
    out = X.copy()
    for group, mu in ((0, mu0), (1, mu1)):
        m = g == group
        # Move the mean along the maximum-separation linear direction.
        shift = alpha * P @ (target - mu)
        out[m] += shift
    return out


def sanity_check(seed=42):
    rng = np.random.default_rng(seed)
    x0 = rng.normal(size=(400, 8))
    x1 = x0 + np.array([2, 1, .5, 0, 0, 0, 0, 0])
    X = np.vstack([x0, x1]); g = np.r_[np.zeros(len(x0), int), np.ones(len(x1), int)]
    f = fit_leace_cl(X, g)
    z = transform(X, g, f, 1.0)
    assert np.linalg.norm(z[g == 0].mean(0) - z[g == 1].mean(0)) < 1e-8
    return True

if __name__ == "__main__":
    print("sanity_check:", sanity_check())
