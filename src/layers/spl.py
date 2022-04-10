import numpy as np

import P
from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
from src.trig_functions import _normal
from src.gen_trig_fun import gen_alpha, gen_scale
import random

class Spl(AbstractLayer, AbstractSSS):

	"""Each ship gets X copies of all the expls (1 each per default)"""

	def __init__(_s, id, pic, ship, ch):
		AbstractLayer.__init__(_s)

		_s.gi = deepcopy(ship.gi['xtras'][ship.id + "_spls"])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_SPL = 50
		_s.zorder = None

	def finish_spl_info(_s):
		"""
		This will be same as sail except that its much simpler cuz extent_black not used
		Just takes max from extent[:, 1]
		"""
		_s.gi['max_ri'] = np.max(_s.extent[:, 1])

	def gen_scale_vector(_s, frames_num):
		_s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale(_s.NUM_FRAMES_SPL, fun_plot='spl', ld_ss=_s.gi['ld_ss'])

	def gen_dyn_extent_alpha(_s):
		"""Needs to be here cuz finish_smoke_info is"""
		_s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, _s.pic, _s.gi['scale_vector'], _s.gi['lds_vec'])

		# _s.finish_spl_info()
		# _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
		# 	gen_triangles(_s.extent_t, _s.extent, _s.gi, _s.pic)
		_s.alpha = gen_alpha(_s.gi, fun_plot='spl')
		aa = 5

	def comp_extent_alpha_z_spl(_s, ships):
		left = _s.ship.extent[_s.frame_ss[0]][0] + _s.gi['offset'][0] + \
		       random.randint(-_s.gi['offset_rand'][0], _s.gi['offset_rand'][0])
		right = left + _s.pic.shape[1]
		down = _s.ship.extent[_s.frame_ss[0]][2] + _s.gi['offset'][1] + \
		       random.randint(-_s.gi['offset_rand'][1], _s.gi['offset_rand'][1])
		up = down - _s.pic.shape[0]

		_s.extent = [[left, right, down, up]]  # * _s.NUM_FRAMES_EXPL
		_s.extent = np.asarray(_s.extent * _s.NUM_FRAMES_SPL)
		# _s.extent = np.array([[left, right, down, up], [left, right, down, up], [left, right, down, up]])

		_s.zorder, status = _s.comp_z_order(ships)


		scale_vec = _normal(np.arange(0, _s.NUM_FRAMES_SPL), mean=_s.NUM_FRAMES_SPL // 2, var=_s.NUM_FRAMES_SPL // 4, y_range=[0, 0.999])

		# self.extent_mov = [self.tl[0] - width / 2, self.tl[0] + width / 2, self.tl[1],
		#                    self.tl[1] - height]  # prevent it to go far down
		aa = 5
		# _s.extent = gen_extent_normal()

		#

	def comp_z_order(_s, ships):
		"""
		Check if any ship is in the way. If yes, take ships z-order and + 1.
		If not, take wave z-order + 1
		"""

		status = 'over_ship'

		return 999, status








