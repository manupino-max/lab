"""M4 LEACE-CL: rank-1 linear combination along maximum Fisher separation.

The fitted map is unconditional at application time: it does not require the
protected label for each test sample. Train statistics alone define the map.
"""
from __future__ import annotations
import numpy as np


def fit_leace_cl(X: np.ndarray, g: np.ndarray, eps: float = 1e-6):
    x0, x1 = X[g == 0], X[g == 1]
    mu0, mu1 = x0.mean(0), x1.mean(0)
    d = mu1 - mu0
    s0 = np.cov(x0, rowvar=False)
    s1 = np.cov(x1, rowvar=False)
    sw = (s0 * (len(x0)-1) + s1 * (len(x1)-1)) / max(len(X)-2, 1)
    sw = sw + eps * np.eye(X.shape[1])
    w = np.linalg.solve(sw, d)                 # maximum Fisher separation
    denom = float(w @ d)
    P = np.outer(d, w) / max(denom, eps)       # P d = d
    midpoint = 0.5 * (mu0 + mu1)
    return {"mu0": mu0, "mu1": mu1, "d": d, "w": w, "P": P, "midpoint": midpoint}


def transform(X: np.ndarray, fit: dict, alpha: float):
    """Unconditional partial LEACE-CL.

    T_alpha(z) = z - alpha P(z-mu_f). Since P(mu1-mu0)=mu1-mu0,
    alpha=1 maps both empirical means to the same mu_f.
    """
    P, target = fit["P"], fit["midpoint"]
    return X - alpha * ((X - target) @ P.T)


def sanity_check(seed=42):
    rng = np.random.default_rng(seed)
    x0 = rng.normal(size=(400, 8))
    x1 = x0 + np.array([2, 1, .5, 0, 0, 0, 0, 0])
    X = np.vstack([x0, x1]); g = np.r_[np.zeros(len(x0), int), np.ones(len(x1), int)]
    f = fit_leace_cl(X, g)
    z = transform(X, f, 1.0)
    assert np.linalg.norm(z[g == 0].mean(0) - z[g == 1].mean(0)) < 1e-8
    return True

if __name__ == "__main__":
    print("sanity_check:", sanity_check())
