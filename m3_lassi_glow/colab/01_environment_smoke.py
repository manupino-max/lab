import importlib
import platform

mods = ['numpy', 'pandas', 'sklearn', 'scipy', 'torch', 'torchvision']
print('Python:', platform.python_version())
for name in mods:
    m = importlib.import_module(name)
    print(f'{name}:', getattr(m, '__version__', 'unknown'))

import torch
print('CUDA available:', torch.cuda.is_available())
if torch.cuda.is_available():
    print('GPU:', torch.cuda.get_device_name(0))

print('M3-LG-00 PASS')
