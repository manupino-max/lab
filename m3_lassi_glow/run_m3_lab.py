"""M3 LAB public experiment orchestrator.

Runs only public/exploratory stages. It never commits dataset images,
private evidence, credentials or unpublished thesis results.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def git_sha(path: Path) -> str | None:
    try:
        return subprocess.check_output(
            ['git', '-C', str(path), 'rev-parse', 'HEAD'], text=True
        ).strip()
    except Exception:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument('--data-root', type=Path, default=None)
    ap.add_argument('--output', type=Path, default=Path('runs'))
    args = ap.parse_args()

    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')
    out = args.output / run_id
    out.mkdir(parents=True, exist_ok=True)

    manifest = {
        'run_id': run_id,
        'status': 'STARTED',
        'scope': 'M3 public exploratory lab',
        'python': platform.python_version(),
        'platform': platform.platform(),
        'data_root': str(args.data_root) if args.data_root else None,
        'dataset_policy': 'official ISIC acquisition only; no redistribution by this lab',
        'thesis_status': 'NOT_THESIS_VALIDATED',
    }

    if args.data_root and args.data_root.exists():
        files = [p for p in args.data_root.rglob('*') if p.is_file()]
        images = [p for p in files if p.suffix.lower() in {'.jpg', '.jpeg'}]
        manifest['image_count'] = len(images)
        manifest['image_sha256_count'] = len(images)
        manifest['data_root_sha256_sample'] = [
            {'file': str(p.relative_to(args.data_root)), 'sha256': sha256_file(p)}
            for p in sorted(images)[:20]
        ]
    else:
        manifest['status'] = 'NO_DATA_RUNTIME_ONLY'

    (out / 'run_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2))
    print(f'Run manifest: {out / "run_manifest.json"}')


if __name__ == '__main__':
    main()
