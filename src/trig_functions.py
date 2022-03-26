


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

# def sigmoid(X):
# 	return 1/(1 + np.exp(-X))

def _sigmoid(x, grad_magn_inv=None, x_shift=None, y_magn=None, y_shift=None):
	"""
	the leftmost dictates gradient: 75=steep, 250=not steep
	the rightmost one dictates y: 0.1=10, 0.05=20, 0.01=100, 0.005=200
	"""
	return (1 / (math.exp(-x / grad_magn_inv + x_shift) + y_magn)) + y_shift  # finfin


if __name__ == '__main__':

	fig, ax = plt.subplots(figsize=(10, 6))

	# X = np.linspace(0, 1, num=50)
	# Y = _normal(X)
	# Y = ([sigmoid(x, grad_magn_inv=16//6, x_shift=16//3.6, y_magn=1, y_shift=0.0) for x in X])  # waves

	# SMOKA ============
	X = np.arange(0, 50, 1)  # large: 960
	Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1.2, y_shift=0) for x in X]))  # smoka

	ax.plot(X, Y, '-')
	# plt.xlim([-5, NUM])
	# plt.ylim([-2.5, 2.5])
	plt.show()
