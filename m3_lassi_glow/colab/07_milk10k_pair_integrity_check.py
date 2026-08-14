"""M3 E2 integrity gate: verify paired clinical/dermoscopic views per lesion.
Public LAB; dataset must be acquired independently from official ISIC terms.
This script only audits metadata and filenames/IDs; it does not train or alter data.
"""
from pathlib import Path
import os
import pandas as pd

META = Path(os.environ.get("MILK10K_METADATA", "/content/MILK10k/metadata.csv"))
if not META.exists():
    raise FileNotFoundError(f"Metadata not found: {META}")
meta = pd.read_csv(META)

required = {"lesion_id"}
missing = required - set(meta.columns)
if missing:
    raise ValueError(f"Missing required columns: {sorted(missing)}")

counts = meta.groupby("lesion_id").size()
if len(counts) != 5240:
    raise ValueError(f"Expected 5240 lesion IDs, got {len(counts)}")
if not (counts == 2).all():
    bad = counts[counts != 2].to_dict()
    raise ValueError(f"Expected exactly 2 views per lesion; violations: {bad}")

print("M3-E2 PAIR INTEGRITY PASS")
print("metadata_rows:", len(meta))
print("lesions:", len(counts))
print("views_per_lesion:", counts.value_counts().to_dict())
