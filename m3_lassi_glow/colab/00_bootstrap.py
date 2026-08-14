# M3 LAB — Colab bootstrap
# Programming-only setup. No private thesis data or evidence is committed.

import os
import subprocess
import sys
from pathlib import Path

LAB = Path('/content/m3-lab')
if not LAB.exists():
    subprocess.run(['git', 'clone', 'https://github.com/manupino-max/lab.git', str(LAB)], check=True)

REQ = LAB / 'm3_lassi_glow' / 'requirements.txt'
subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', str(REQ)], check=True)

print('LAB:', LAB)
print('M3 LASSI/GLOW bootstrap complete')
print('Next: run 01_environment_smoke.py')
