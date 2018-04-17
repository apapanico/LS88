import sys
from pathlib import Path

print('Adding datascience helper tools to path...')

ROOT = Path(__file__).parents[1]
sys.path.insert(2, str(ROOT / 'utils'))

print("Setting up Matplotlib...")

import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython import get_ipython

plt.style.use('fivethirtyeight')
get_ipython().run_line_magic('matplotlib', 'inline')
mpl.rcParams['figure.facecolor'] = (0.941, 0.941, 0.941, 1.0)

print("Matplotlib imported as mpl")
print("Matplotlib.pyplot imported as plt")
