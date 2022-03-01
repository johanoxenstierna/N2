
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np
from src.trig_functions import _normal

def gen_alpha(gi, fun_plot, plot=False):
	X = np.arange(0, gi['frame_ss'][-1] - gi['frame_ss'][0])
	alpha = None
	if fun_plot == 'normal':
		alpha = _normal(X, mean=len(X)//2, var=len(X)//4, y_range=[0, 0.2])
	return alpha



