


from scipy.stats import chi2
from scipy.stats import norm, gamma, multivariate_normal
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


def _gamma(X, mean):
	Y = gamma.pdf(X, mean)
	Y = min_max_normalization(Y, y_range=[0.0, 1.0])
	return Y


def _log(X):
	Y = np.log(X)
	Y = min_max_normalization(Y, y_range=[0.0, 1.0])
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


def sin_exp_experiment(X):
	Y = (0.2 * np.sin(X) + 0.05 * np.sin(X) + 0.4 * np.log(X) / np.log(P.FRAMES_TOT)) - 0.1
	return Y


if __name__ == '__main__':

	fig, ax = plt.subplots(figsize=(10, 6))

	# SMOKA ============
	# X = np.arange(0, 1000, 1)  # large: 960
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1., y_shift=0) for x in X]))  # smoka alpha
	# X = X + 1
	# Y = _log(X)

	# # FIr:
	# X = np.arange(0, 50, 1)  # large: 960
	# Y = sin_exp_experiment(X)
	'''
	Need do create candidate list and check mass and see whether there are too many 
	fires per moving average unit. 
	'''

	# WAVE alpha ============
	# X = np.arange(0, 23)
	# Y = _normal(X, mean=len(X) // 2, var=len(X) // 4, y_range=[0, 0.15])
	# Y = ([_sigmoid(x, grad_magn_inv=16//6, x_shift=16//3.6, y_magn=1, y_shift=0.0) for x in X])  # waves

	# ## WAVE expl (X is distance and Y is alpha) ==============
	# X = np.arange(0, 1000, 1)  # large: 960
	# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-2, y_magn=10.2, y_shift=0) for x in X]))

	# # SPL extent =============
	# X = np.arange(0, 50)
	# # Y = _normal(X, mean=len(X) // 3, var=len(X) // 4, y_range=[0, 0.999])
	# a = 1.99
	# x = np.linspace(gamma.ppf(0.01, a),
	#                 gamma.ppf(0.99, a), 50)
	# X = np.linspace(0, 16)
	# Y = gamma.pdf(X, 2)
	# Y = min_max_normalization(Y, y_range=[0.0, 1.0])

	#EXPL on ship
	# fig = plt.figure(figsize=(10, 6))
	# ax = fig.add_subplot(1, 1, 1, projection='3d')
	# X0, X1 = np.meshgrid(np.arange(0, 50, 1), np.arange(0, 50, 1))
	# X = np.dstack((X0, X1))
	# Y = multivariate_normal.pdf(X, mean=(20, 20), cov=[[15, 0], [0, 15]])  # only for rand?
	# Y = min_max_normalization(Y, y_range=[0, 1])
	# breakpoint()

	# Y = np.random.multivariate_normal((20, 20), [[1, 0], [0, 1]], size=(40, 40))
	# Y = chi2.pdf(X / 2, 4)

	# ax.plot(X, Y, '-')
	# plt.xlim([-5, NUM])
	# plt.ylim([-2.5, 2.5])

	plt.show()
