# M3-LG-02: dataset integrity manifest.
# Public LAB only. Dataset must be acquired independently under official ISIC terms.

from pathlib import Path
import hashlib, json, os
import pandas as pd

ROOT = Path(os.environ.get('MILK10K_ROOT', '/content/MILK10k'))
META = Path(os.environ.get('MILK10K_METADATA', str(ROOT / 'metadata.csv')))
OUT = Path('/content/m3_milk10k_integrity_manifest.json')

if not META.exists():
    raise FileNotFoundError(f'Metadata not found: {META}')

meta = pd.read_csv(META)
image_files = [p for p in ROOT.rglob('*') if p.suffix.lower() in {'.jpg', '.jpeg', '.png'}]

manifest = {
    'dataset': 'MILK10k',
    'source': 'official ISIC Archive',
    'expected_training_images': 10480,
    'expected_training_lesions': 5240,
    'observed_metadata_rows': int(len(meta)),
    'observed_image_files': int(len(image_files)),
    'metadata_columns': list(meta.columns),
}

if len(meta) != 10480:
    raise RuntimeError(f'Metadata row count mismatch: {len(meta)} != 10480')
if len(image_files) != 10480:
    raise RuntimeError(f'Image count mismatch: {len(image_files)} != 10480')

# Hash only the manifest, not dataset contents, to keep this repository data-free.
text = json.dumps(manifest, sort_keys=True, indent=2)
manifest['manifest_sha256'] = hashlib.sha256(text.encode()).hexdigest()
OUT.write_text(json.dumps(manifest, indent=2), encoding='utf-8')
print(json.dumps(manifest, indent=2))
print('M3-LG-02 PASS')
