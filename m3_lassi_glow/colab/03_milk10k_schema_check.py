# M3-LG-02: schema-only check. Requires a locally obtained MILK10k metadata CSV.
# Set MILK10K_METADATA to the local path in Colab. No dataset is committed here.

import os
from pathlib import Path
import pandas as pd

path = Path(os.environ.get('MILK10K_METADATA', '/content/MILK10k_Training_Metadata.csv'))
if not path.exists():
    raise FileNotFoundError(f'Metadata not found: {path}. Download from the official ISIC source.')

meta = pd.read_csv(path)
print('rows:', len(meta))
print('columns:', list(meta.columns))

expected_rows = 10480
if len(meta) != expected_rows:
    raise ValueError(f'Expected {expected_rows} metadata entries, got {len(meta)}')

print('M3-LG-02 PASS: metadata row count matches official training image count')
