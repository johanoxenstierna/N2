


from scipy.stats import chi2
from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as lines

import math
import numpy as np
import P as P
import random


def _normal(X, mean, var, y_range):
	# Y = norm.pdf(X, loc=len(X)//2, scale=10)
	Y = norm.pdf(X, loc=mean, scale=var)
	Y = min_max_normalization(Y, y_range)
	return Y


def min_max_normalization(X, y_range):
	new_min = y_range[0]
	new_max = y_range[1]
	Y = np.zeros(X.shape)

	_min = np.min(X)
	_max = np.max(X)

	for i, x in enumerate(X):
		Y[i] = ((x - _min) / (_max - _min)) * (new_max - new_min) + new_min

	return Y



if __name__ == '__main__':

	fig, ax = plt.subplots(figsize=(10, 6))

	# X = np.linspace(0, 100, num=50)
	X = np.arange(0, 100)
	Y = _normal(X)

	ax.plot(X, Y, '-')
	# plt.xlim([-5, NUM])
	# plt.ylim([-2.5, 2.5])
	plt.show()
