# M3-LG-05/06: frozen-representation probes.
# Input is a locally generated feature matrix + metadata. No raw images are committed.

import os
from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, balanced_accuracy_score, f1_score

FEATURES = Path(os.environ.get('M3_FEATURES', '/content/m3_features.npy'))
META = Path(os.environ.get('M3_PROBE_METADATA', '/content/m3_probe_metadata.csv'))
if not FEATURES.exists() or not META.exists():
    raise FileNotFoundError('Provide M3_FEATURES (.npy) and M3_PROBE_METADATA (.csv) in the Colab runtime.')

X = np.load(FEATURES)
df = pd.read_csv(META)
if len(X) != len(df):
    raise ValueError('Feature rows and metadata rows differ.')

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
clf = LogisticRegression(max_iter=3000)

# Adapt these column names to the exact official metadata after inspection.
Y_COL = os.environ.get('M3_Y_COL', 'diagnosis')
Z_COL = os.environ.get('M3_Z_COL', 'skin_tone')

for target_name, col in [('Y', Y_COL), ('Z', Z_COL)]:
    y = df[col].to_numpy()
    pred = cross_val_predict(clf, X, y, cv=cv, method='predict_proba')
    if len(np.unique(y)) == 2:
        score = roc_auc_score(y, pred[:, 1])
        metric = {'target': target_name, 'column': col, 'roc_auc': float(score)}
    else:
        labels = np.unique(y)
        hard = labels[np.argmax(pred, axis=1)] if pred.shape[1] == len(labels) else clf.fit(X, y).predict(X)
        metric = {
            'target': target_name,
            'column': col,
            'balanced_accuracy': float(balanced_accuracy_score(y, hard)),
            'macro_f1': float(f1_score(y, hard, average='macro')),
        }
    print(metric)
