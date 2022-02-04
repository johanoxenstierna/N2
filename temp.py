
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))

# x = np.linspace(0, 1.0, 100)
x = np.linspace(0, 1.0, 100)
ax.plot(x, norm.pdf(x, loc=0.5, scale=0.15) / 2.7, 'r-', lw=5, alpha=0.6, label='norm pdf')

plt.show()
ff = 5

# HOW TO