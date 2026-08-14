# Synthetic, programming-only sanity test for the M3 representation-fairness interface.
# This is NOT a scientific result and uses no MILK10k data.

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(42)
n, d = 1200, 16
z = rng.integers(0, 2, n)
y = ((rng.normal(size=n) + 0.8 * z) > 0).astype(int)
X = rng.normal(size=(n, d))
X[:, 0] += 1.5 * z
X[:, 1] += 1.2 * y

clf_z = LogisticRegression(max_iter=2000).fit(X, z)
clf_y = LogisticRegression(max_iter=2000).fit(X, y)

auc_z = roc_auc_score(z, clf_z.predict_proba(X)[:, 1])
auc_y = roc_auc_score(y, clf_y.predict_proba(X)[:, 1])

print({'proxy_auc_z': round(float(auc_z), 4), 'task_auc_y': round(float(auc_y), 4)})
print('M3-LG-01 PASS: representation/probe plumbing works on synthetic data')
