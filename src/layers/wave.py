import numpy as np

from src.layers.abstract import AbstractLayer
from src.gen_extent_triangles import *
from src.gen_trig_fun import gen_alpha
from src.trig_functions import _sigmoid
import P as P
import random

class Wave(AbstractLayer):
	"""
	OBS waves dont have info, so its included in the class
	Some of the sss stuff generated here may overlap with sss
	"""

	def __init__(_s, id, pic):
		super().__init__()
		_s.id = id
		_s.pic = pic

		_s.NUM_FRAMES_AVG = 120  # 40
		_s.NUM_FRAMES_RAND_MAX = 30  # 30  # this is rand PER REPEAT
		_s.NUM_REPEATS_OF_SAME_WAVE = 1  # this times AVG * RAND must be less than frames
		# num_frames_avg * num_repeats_of_same_wave should give
		_s.DEST_RAND_MIN_MAX = [[-80, -0], [-20, 0]]  # first is X, second is Y

		_s.frame_sss = _s.gen_frame_sss()
		ld_sss = _s.gen_ld_sss()
		ld_sss = _s.gen_zigzag_sss(ld_sss)
		_s.extent, _s.alpha = _s.gen_extent_alpha_wave(ld_sss)  # left_down_log
		_s.alpha_wave_expl = _s.gen_alpha_wave_expl()

		# _s.frame_ss = _s.frame_sss[0]
		_s.frame_ss = [_s.frame_sss[0][0], _s.frame_sss[-1][1]]
		# _s.ld_ss = _s.ld_sss[0]
		_s.zorder = 2

		# _s.alpha = gen_alpha(_s.gi, fun_plot='normal')

	def gen_frame_sss(_s):
		"""
		Generates several frame_ss
		"""
		frame_sss = []
		frame_start = random.randint(3, _s.NUM_FRAMES_AVG)
		# NUM_REPEATS_OF_SAME_WAVE = 2

		for i in range(_s.NUM_REPEATS_OF_SAME_WAVE):
			# frame_start_rand = random.randint(3, 5)
			# frame_start = frame_start + frame_start_rand
			num_frames_rand = random.randint(0, _s.NUM_FRAMES_RAND_MAX)
			num_frames = _s.NUM_FRAMES_AVG + num_frames_rand
			frame_end = frame_start + num_frames
			assert(frame_end < P.FRAMES_STOP)
			frame_sss.append([frame_start, frame_end])
			# frame_break = random.randint(3, 6)  # how many frames to wait until next wave
			frame_start = frame_end + 1

		return frame_sss

	# def set_ss(_s, ii):
	# 	"""runs through frame_sss and checks which frame_ss is to be used"""
	#
	# 	for i in range(len(_s.frame_sss)):
	# 		frame_ss = _s.frame_sss[i]
	# 		if ii >= frame_ss[0] and ii < frame_ss[1]:
	# 			_s.frame_ss = frame_ss
	# 			_s.ld_ss = _s.ld_sss[i]

	def gen_ld_sss(_s):
		"""left downs start stop for each wave. So each class instance gets an ld_sss linked list which says where
		it starts and stops. This is then used to aggregate extent
		"""
		id_split = _s.id.split('_')

		x_rand0 = random.randint(_s.DEST_RAND_MIN_MAX[0][0], _s.DEST_RAND_MIN_MAX[0][1])
		y_rand0 = random.randint(_s.DEST_RAND_MIN_MAX[1][0], _s.DEST_RAND_MIN_MAX[1][1])
		origin_xy = [int(id_split[2]) + x_rand0, int(id_split[3]) + y_rand0]
		dest_xy = [origin_xy[0] + x_rand0, origin_xy[1] + y_rand0]

		ld_sss = []
		for i in range(len(_s.frame_sss)):  # PER WAVE TRAJECTORY  makes sure each sss outputs different trajectory
			x_rand1 = random.randint(-20, 20)  # both orig and dest
			y_rand1 = random.randint(-10, 0)  # both orig and dest
			ld_ss = [[origin_xy[0] + x_rand1, origin_xy[1] + y_rand1],
			         [dest_xy[0], dest_xy[1]]]
			ld_sss.append(ld_ss)
		assert(len(ld_sss) == len(_s.frame_sss))
		return ld_sss

	def gen_zigzag_sss(_s, ld_sss):
		"""For each ld_sss, generate normal distribution """
		ld_zz_sss = []
		for i in range(len(ld_sss)):  # PER WAVE zig zag
			pass

		return ld_sss


	def gen_extent_alpha_wave(_s, ld_sss):
		"""
		OBS be ware this is rather 'unusual' since gen_extent has to be the concatenation of extents generated
		for each sss
		"""
		rand_start = 3
		rand_stop = 10
		# _s.frame_ss = [5 + rand_start, 40 + rand_stop]  # not sure this is needed outside

		# num_rows = _s.frame_sss[-1][1] - _s.frame_sss[0][0]
		# extent_agg = np.zeros((num_rows, 4))
		extent_agg = []
		alpha_agg = []

		# BUILD gi what is needed to call gen_extent

		for i in range(len(_s.frame_sss)):
			_gi = {"frame_ss": _s.frame_sss[i],
			       "ld_ss": ld_sss[i],
			       "scale_ss": [1.0, 0.5]
			       }

			extent, extent_t, lds_log, scale_vector = gen_extent(_gi, _s.pic)  # left_down_log
			extent_agg += [[0, 1, 1, 0]]  # better too long than too short since clock only risks going out of bounds otherwise
			extent_agg += list(extent)

			alpha = gen_alpha(_gi, fun_plot='normal', y_range=[0, 0.1])  # 0.,05
			alpha_agg += [0.0]
			alpha_agg += list(alpha)
			aa = 5

		# extent_agg = extent_agg + [[0, 1, 1, 0], [0, 1, 1, 0]]
		extent = np.asarray(extent_agg)
		alpha = np.asarray(alpha_agg)
		return extent, alpha

	def gen_alpha_wave_expl(_s):
		"""
		Since alpha is sufficient to make wave brighter when expl happens, there needs to be a
		sigmoid to provide the amount of alpha given a certain distance to an expl.
		"""
		# alpha = gen_alpha(_gi, fun_plot='normal')
		X = np.arange(0, 1200, 1)  # large: 960
		# Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len( X) / 10, x_shift=-2, y_magn=18, y_shift=0) for x in X]))
		Y = np.asarray(([_sigmoid(x, grad_magn_inv=- len( X) / 10, x_shift=-2, y_magn=40, y_shift=0) for x in X]))
		return Y