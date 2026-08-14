# M3-LG external-source inventory check.
# Clones only into ephemeral /content; nothing is copied into the repository.

import subprocess
from pathlib import Path

sources = {
    'lassi': 'https://github.com/eth-sri/lassi.git',
    'lassi-repro': 'https://github.com/Mametchiii/lassi-reproducibility.git',
    'milk10k-fairness': 'https://github.com/daaviidmadrid/milk10k-fairness-skin-lesion-classification.git',
    'multimodal-lesion': 'https://github.com/sshemanth/multimodal-lesion-diagnosis.git',
    'panderm-milk10k': 'https://github.com/enjoeyland/PanDerm_milk10k.git',
    'mm-skin-fs': 'https://github.com/SaptarshiPani/MM-Skin-FS.git',
}

root = Path('/content/m3_external_sources')
root.mkdir(exist_ok=True)
for name, url in sources.items():
    dest = root / name
    if not dest.exists():
        print('CLONE', name)
        subprocess.run(['git', 'clone', '--depth', '1', url, str(dest)], check=True)
    else:
        print('EXISTS', name)

print('\nM3-LG external inventory complete')
for p in sorted(root.iterdir()):
    print(p.name, '->', p)
