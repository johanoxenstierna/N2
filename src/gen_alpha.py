
from scipy.stats import norm
import matplotlib.pyplot as plt
import numpy as np

def gen_alpha(num_frames, plot=False):
	x = np.linspace(0, 1.0, 100)
	y = norm.pdf(x, loc=0.5, scale=0.15) / 2.7


	if plot == True:
		fig, ax = plt.subplots(figsize=(12, 8))
		ax.plot(x, y, 'r-', lw=5, alpha=0.6, label='norm pdf')
		plt.show()
	return y


if __name__ == "__main__":

	a = gen_alpha(100, plot=True)