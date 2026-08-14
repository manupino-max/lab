# M3 COMPLETE LAB RUN — Google Colab
# Public/exploratory only. Obtain MILK10k directly from ISIC under its terms.

from pathlib import Path
import subprocess, sys, os

ROOT = Path('/content/m3-lab')
if not ROOT.exists():
    subprocess.run(['git', 'clone', 'https://github.com/manupino-max/lab.git', str(ROOT)], check=True)

subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', '-r', str(ROOT/'m3_lassi_glow/requirements.txt')], check=True)

# 1) Environment
subprocess.run([sys.executable, str(ROOT/'m3_lassi_glow/colab/01_environment_smoke.py')], check=True)

# 2) Public LASSI source (runtime only)
subprocess.run([sys.executable, str(ROOT/'m3_lassi_glow/colab/04_lassi_source_check.py')], check=True)

# 3) Synthetic pipeline sanity
subprocess.run([sys.executable, str(ROOT/'m3_lassi_glow/colab/02_synthetic_representation_probe.py')], check=True)

# 4) If official MILK10k has already been acquired into /content/MILK10k,
#    run the schema check. Otherwise this stage is explicitly BLOCKED_BY_DATA.
data = Path('/content/MILK10k')
if data.exists():
    metadata_candidates = list(data.rglob('*Metadata*.csv')) + list(data.rglob('*metadata*.csv'))
    if metadata_candidates:
        os.environ['MILK10K_METADATA'] = str(metadata_candidates[0])
        subprocess.run([sys.executable, str(ROOT/'m3_lassi_glow/colab/03_milk10k_schema_check.py')], check=True)
    else:
        print('BLOCKED_BY_DATA: metadata CSV not found under /content/MILK10k')
else:
    print('BLOCKED_BY_DATA: acquire MILK10k from official ISIC source first')

print('\nM3 COMPLETE PUBLIC LAB BOOTSTRAP FINISHED')
print('Next scientific stages: representation extraction -> Y/Z probes -> GLOW validity -> LASSI adapter.')
