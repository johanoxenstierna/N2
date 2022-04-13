import numpy as np

import P
from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
from src.trig_functions import _normal
from src.gen_trig_fun import gen_alpha, gen_scale_lds
import random

class Spl(AbstractLayer, AbstractSSS):

	"""Each ship gets X copies of all the expls (1 each per default)"""

	def __init__(_s, id, pic, ship, ch):
		AbstractLayer.__init__(_s)

		_s.gi = deepcopy(ship.gi['xtras'][ship.id + "_spls"])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_SPL = 50
		_s.zorder = None  # defaults to waves zorder + 1  (i.e. 2 + 1 = 3)

	def finish_spl_info(_s):
		"""
		This will be same as sail except that its much simpler cuz extent_black not used
		Just takes max from extent[:, 1]
		"""
		_s.gi['max_ri'] = np.max(_s.extent[:, 1])

	def gen_scale_vector(_s, frames_num):
		_s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale_lds(frames_num, fun_plot='spl', ld_ss=_s.gi['ld_ss'])

	def gen_dyn_extent_alpha(_s):
		"""Needs to be here cuz finish_spl_info is TODO: for warp_affine this is needed"""
		_s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, _s.pic, _s.gi['scale_vector'], _s.gi['lds_vec'])

		# BELOW WORKS (April 13).
		# _s.finish_spl_info()
		# _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
		# 	gen_triangles(_s.extent_t, _s.extent, _s.gi, _s.pic)
		# _s.alpha = gen_alpha(_s.gi, fun_plot='spl')
		aa = 5

	def comp_zorder(_s, ships, ii):
		"""
		Check if any ship is in the way (OBS only at the first frame). If yes, take ships z-order and + 1.
		If not, take water z-order + 1 (default)
		For each ship the bounding box is computed as lt and dr and then checking against thos
		"""

		left_max = max(_s.gi['lds_vec'][:, 0])  # max(_s.extent[:, 0])
		down_max = max(_s.gi['lds_vec'][:, 1])  # since its at water level
		ld = [left_max, down_max]
		for ship_id, ship in ships.items():
			s_ext = ship.extent[ii, :]
			if ld[0] >= s_ext[0] and ld[0] <= s_ext[1] and \
				ld[1] <= s_ext[2] and ld[1] >= s_ext[3]:  # between l and r and between d and t (u)
				_s.zorder = ship.zorder + 1
				_s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale_lds(_s.NUM_FRAMES_SPL, fun_plot='spl_hard', ld_ss=_s.gi['ld_ss'])
				return

		_s.zorder = 3  # DEFAULT








