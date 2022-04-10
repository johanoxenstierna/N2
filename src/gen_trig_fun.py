
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from src.trig_functions import _normal, _sigmoid, _gamma, _log

def gen_alpha(gi, fun_plot, plot=False):
	X = np.arange(0, gi['frame_ss'][-1] - gi['frame_ss'][0])
	alpha = None
	if fun_plot == 'normal':
		alpha = _normal(X, mean=len(X)//2, var=len(X)//4, y_range=[0, 0.15])  # THIS IS WAVE ALPHA
	elif fun_plot == 'smoka':
		alpha = np.asarray(([_sigmoid(x, grad_magn_inv=- len(X) / 10, x_shift=-6, y_magn=1., y_shift=0) for x in X]))
	elif fun_plot == 'spl':
		alpha = _gamma(X, mean=max(len(X)//4, 2))

	return alpha


def gen_scale(NUM_FRAMES, fun_plot, plot=False, ld_ss=None):
	if fun_plot == 'spl':
		X = np.arange(1, NUM_FRAMES + 1)
		scale = _gamma(X, len(X) // 3)
		lds_vec = np.zeros((scale.shape[0], 2))
		mov_x_tot = ld_ss[1][0] - ld_ss[0][0]
		mov_y_tot = ld_ss[1][1] - ld_ss[0][1]
		for i in range(0, len(scale)):
			lds_vec[i, 0] = ld_ss[0][0] + mov_x_tot * scale[i]  # left
			lds_vec[i, 1] = ld_ss[0][1] + mov_y_tot * scale[i]  # left
		return scale, lds_vec
	elif fun_plot == 'smoka':
		X = np.arange(1, NUM_FRAMES + 1)
		scale = _log(X)
	elif fun_plot == 'smokr':
		X_scale = np.arange(1, NUM_FRAMES + 1)
		scale = _log(X_scale)
		lds_vec = np.zeros((scale.shape[0], 2))  # cols are left and down
		mov_x_tot = ld_ss[1][0] - ld_ss[0][0]
		mov_y_tot = ld_ss[1][1] - ld_ss[0][1]
		for i in range(0, len(scale)):
			lds_vec[i, 0] = ld_ss[0][0] + mov_x_tot * scale[i]  # left
			lds_vec[i, 1] = ld_ss[0][1] + mov_y_tot * scale[i]  # left

		return scale, lds_vec

	return scale


