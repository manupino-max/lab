"""M3 MILK10k acquisition/schema preflight.

This script does not train models, create splits, tune thresholds, or alter data.
It only validates an officially acquired local MILK10k copy before E3.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

EXPECTED = {
    "images": 10480,
    "lesions": 5240,
    "skin_tone_levels": set(range(6)),
}


def sha256(path: Path, chunk: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def pick_csvs(root: Path):
    csvs = sorted(root.rglob("*.csv"))
    metadata = [p for p in csvs if "metadata" in p.name.lower()]
    diagnosis = [p for p in csvs if "diagnos" in p.name.lower() or "ground" in p.name.lower()]
    return csvs, metadata, diagnosis


def find_col(df: pd.DataFrame, candidates: list[str]):
    lower = {c.lower(): c for c in df.columns}
    for c in candidates:
        if c.lower() in lower:
            return lower[c.lower()]
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    args = ap.parse_args()
    root = args.root.resolve()
    if not root.exists():
        raise SystemExit(f"DATA_ROOT_NOT_FOUND: {root}")

    images = [p for p in root.rglob("*") if p.is_file() and p.suffix.lower() in {".jpg", ".jpeg"}]
    csvs, metadata_csvs, diagnosis_csvs = pick_csvs(root)
    report = {
        "status": "PASS",
        "root": str(root),
        "image_count": len(images),
        "csv_count": len(csvs),
        "metadata_candidates": [str(p.relative_to(root)) for p in metadata_csvs],
        "diagnosis_candidates": [str(p.relative_to(root)) for p in diagnosis_csvs],
        "checks": [],
        "file_sha256": {},
    }

    def check(name, ok, detail):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["status"] = "FAIL"

    check("image_count", len(images) == EXPECTED["images"], f"{len(images)} / {EXPECTED['images']}")
    check("csv_available", bool(csvs), "at least one CSV required")

    if metadata_csvs:
        meta = pd.read_csv(metadata_csvs[0])
        lesion_col = find_col(meta, ["lesion", "lesion_id", "lesionid"])
        tone_col = find_col(meta, ["skin_tone", "skin tone", "skintone"])
        check("metadata_lesion_column", lesion_col is not None, str(lesion_col))
        check("metadata_skin_tone_column", tone_col is not None, str(tone_col))
        if lesion_col:
            n_lesions = meta[lesion_col].nunique(dropna=True)
            check("lesion_count", n_lesions == EXPECTED["lesions"], f"{n_lesions} / {EXPECTED['lesions']}")
        if tone_col:
            vals = set(pd.to_numeric(meta[tone_col], errors="coerce").dropna().astype(int).unique())
            check("skin_tone_levels", vals == EXPECTED["skin_tone_levels"], sorted(vals))

    # Hash only small metadata/config files; never hash/copy the image corpus here.
    for p in metadata_csvs + diagnosis_csvs:
        report["file_sha256"][str(p.relative_to(root))] = sha256(p)

    print(json.dumps(report, indent=2, sort_keys=True))
    if report["status"] != "PASS":
        raise SystemExit(2)


if __name__ == "__main__":
    main()
