
from scipy.stats import norm
import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(12, 8))

A = np.random.random((3, 6))
ex = 1.3
A = A * ex
A[A > 1.0] = 1.0


plt.show()


# HOW TO