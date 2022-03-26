import numpy as np

from src.layers.abstract import AbstractLayer
from src.gen_extent_triangles import *
from src.gen_alpha import gen_alpha
import P as P
import random

class Wave(AbstractLayer):
	"""Some of the sss stuff generated here may overlap with sss """

	def __init__(_s, id, pic):
		super().__init__()
		_s.id = id
		_s.pic = pic

		_s.NUM_FRAMES_AVG = 20  # 40
		_s.NUM_FRAMES_RAND_MAX = 10  # 30
		_s.NUM_REPEATS_OF_SAME_WAVE = 3
		_s.DEST_RAND_MIN_MAX = [[-30, -10], [-10, -2]]

		_s.frame_sss = _s.gen_frame_sss()
		ld_sss = _s.gen_ld_sss()
		_s.extent, _s.alpha = _s.gen_extent_alpha_wave(ld_sss)  # left_down_log

		# _s.frame_ss = _s.frame_sss[0]
		_s.frame_ss = [_s.frame_sss[0][0], _s.frame_sss[-1][1]]
		# _s.ld_ss = _s.ld_sss[0]

	    # _s.alpha = gen_alpha(_s.gi, fun_plot='normal')

	def gen_frame_sss(_s):
		"""
		Generates several frame_ss
		"""
		frame_sss = []
		frame_start = random.randint(3, 30)
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
		"""lower downs start stop"""
		id_split = _s.id.split('_')
		origin_xy = [int(id_split[2]), int(id_split[3])]
		dest_xy = [origin_xy[0] + random.randint(_s.DEST_RAND_MIN_MAX[0][0], _s.DEST_RAND_MIN_MAX[0][1]),
		           origin_xy[1] + random.randint(_s.DEST_RAND_MIN_MAX[1][0], _s.DEST_RAND_MIN_MAX[1][1])]

		ld_sss = []
		for i in range(len(_s.frame_sss)):  # makes sure each sss outputs different trajectory
			rand_hor = random.randint(-20, 20)
			rand_ver = random.randint(-20, 20)
			ld_ss = [[origin_xy[0] + rand_hor, origin_xy[1] + rand_ver],
			         [dest_xy[0] + rand_hor, dest_xy[1] + rand_ver]]
			ld_sss.append(ld_ss)
		assert(len(ld_sss) == len(_s.frame_sss))
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
			       "y_mid": 1.0,
			       "scale_ss": [1.0, 1.0]
			       }
			extent, extent_t, lds_log, scale_vector = gen_extent(_gi, _s.pic, padded=False)  # left_down_log
			extent_agg += [[0, 1, 1, 0]]  # better too long than too short since clock only risks going out of bounds otherwise
			extent_agg += list(extent)

			alpha = gen_alpha(_gi, fun_plot='normal')
			alpha_agg += [0.0]
			alpha_agg += list(alpha)
			aa = 5

		# extent_agg = extent_agg + [[0, 1, 1, 0], [0, 1, 1, 0]]
		extent = np.asarray(extent_agg)
		alpha = np.asarray(alpha_agg)
		return extent, alpha