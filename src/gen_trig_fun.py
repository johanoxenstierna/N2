
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from src.trig_functions import _normal, _sigmoid, _gamma, _log, _log_and_linear

def gen_alpha(gi, fun_plot, y_range=None, plot=False):
	X = np.arange(0, gi['frame_ss'][-1] - gi['frame_ss'][0])
	alpha = None
	if fun_plot == 'normal':
		alpha = _normal(X, mean=len(X)//2, var=len(X)//4, y_range=y_range)  # THIS IS WAVE ALPHA
	elif fun_plot == 'smoka':
		alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1., y_shift=0) for x in X]))
	elif fun_plot == 'smokh':
		'''Has to end at 0 alpha because these include fire smokhs'''
		# alpha = np.full(X.shape, fill_value=0.99)
		# alpha = np.linspace(0.5, 1.0, num=len(X))
		alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1., y_shift=0) for x in X]))
	elif fun_plot == 'spl':
		# alpha = _gamma(X, mean=max(len(X)//4, 2), y_range=[0.0, 1.0])
		alpha = _gamma(X, mean=3, var=15, y_range=[0.0, 6.0])  # same as extent

	return alpha


def gen_scale_lds(NUM_FRAMES, fun_plot, plot=False, ld_ss=None, max_scale=1.0):
	scale = None
	X = np.arange(1, NUM_FRAMES + 1)
	if fun_plot == 'spl':
		max_scale = np.random.uniform(0.6, 1.0)
		scale = _gamma(X, mean=3, var=15, y_range=[0.0, max_scale])
	elif fun_plot == 'spl_hard':  # when its on top of ship
		max_scale = np.random.uniform(0.2, 0.5)
		scale = _gamma(X, mean=2, var=15, y_range=[0.0, max_scale])  # same as before just smaller
	elif fun_plot in ['a', 'r']:  # smokes
		if fun_plot == 'a':  # smoka
			# X = np.arange(1, NUM_FRAMES + 1)
			scale = _log_and_linear(X, y_range=[0.0, max_scale])
		elif fun_plot == 'r':  # smokr
			# X_scale = np.arange(1, NUM_FRAMES + 1)
			scale = _log(X, y_range=[0.0, max_scale])

	lds_vec = np.zeros((scale.shape[0], 2))  # cols are left and down
	mov_x_tot = ld_ss[1][0] - ld_ss[0][0]
	mov_y_tot = ld_ss[1][1] - ld_ss[0][1]
	for i in range(0, len(scale)):
		lds_vec[i, 0] = ld_ss[0][0] + mov_x_tot * scale[i]  # left
		lds_vec[i, 1] = ld_ss[0][1] + mov_y_tot * scale[i]  # left

	return scale, lds_vec

	# return scale


