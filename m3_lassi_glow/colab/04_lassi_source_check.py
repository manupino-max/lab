# M3-LG-01: fetch the public LASSI source into the Colab runtime only.
# The source is not copied into this repository.

import subprocess
from pathlib import Path

repo = Path('/content/lassi')
if not repo.exists():
    subprocess.run(['git', 'clone', 'https://github.com/eth-sri/lassi.git', str(repo)], check=True)

print('LASSI source:', repo)
print('Top-level files:')
for p in sorted(repo.iterdir()):
    print(' -', p.name)

print('M3-LG-01 SOURCE CHECK COMPLETE')
