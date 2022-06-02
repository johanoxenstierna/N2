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
		_s.NUM_FRAMES_SPL = 150
		_s.pic = pic
		_s.zorder = None  # defaults to waves zorder + 1  (i.e. 2 + 1 = 3)

	def finish_spl_info(_s):
		"""
		This will be same as sail except that its much simpler cuz extent_black not used
		Just takes max from extent[:, 1]
		"""
		_s.gi['max_ri'] = np.max(_s.extent[:, 1])

	def gen_scale_vector(_s, frames_num, ssas):
		"""TODO: fix so that gen_triangles work for objects that grow then shrink
		OBS for spl the lds_vec is here only a placeholder! Prob bcs there are two cases (in water and on top
		of ship)"""
		_s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale_lds(frames_num, fun_plot='spl', ld_ss=_s.gi['ld_ss'])
		# _s.gi['scale_vector'] = np.linspace(0, 2, num=frames_num)  # this works...
		aa = 5

	def gen_dyn_extent_alpha(_s):
		"""Needs to be here cuz finish_spl_info is TODO: for warp_affine this is needed"""
		_s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, _s.pic, _s.gi['scale_vector'], _s.gi['lds_vec'])

		#TODO:No it doesn't WORK. gen_triangles seems to fail for objects that grow then shrink
		# _s.finish_spl_info()
		# _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
		# 	gen_triangles(_s.extent_t, _s.extent, _s.gi, _s.pic)
		_s.alpha = gen_alpha(_s.gi, fun_plot='spl')
		aa = 5

	def comp_zorder(_s, ships, ii):
		"""
		Check if any ship is in the way (OBS only at the first frame) of randomly generated spl coord.
		For each ship the bounding box is computed as lt and dr and then checking against thos.
		IT OVERWRITES scale_lds IF NECESSARY
		"""

		left_max = max(_s.gi['lds_vec'][:, 0])  # max(_s.extent[:, 0])
		down_max = max(_s.gi['lds_vec'][:, 1])  # since its at water level
		top_max = down_max - _s.pic.shape[0]
		ld = [left_max, down_max]  # top_max == down_min
		lt = [left_max, top_max]  # top_max == down_min
		flag_on_top_of_obj = False
		FORBIDDEN_REGIONS = [[728, 812, 615, 560]]  # left right down up
		for reg in FORBIDDEN_REGIONS:
			if ld[0] >= reg[0] and ld[0] <= reg[1] and \
				ld[1] <= reg[2] and ld[1] >= reg[3]:
				flag_on_top_of_obj = True

		if _s.ship.id == '5':
			adsf = 5

		_s.zorder = 3  # default

		for ship_id, ship in ships.items():
			if len(ship.extent) >= ii:
				s_ext = ship.extent[ii, :]
			else:
				return

			if (ld[0] >= s_ext[0] and ld[0] <= s_ext[1] and \
				ld[1] <= s_ext[2] and ld[1] >= s_ext[3]) or \
					flag_on_top_of_obj == True:  # ON TOP OF SHIP between l and r and between d and t (u)
				_s.zorder = ship.zorder + 1
				_s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale_lds(_s.NUM_FRAMES_SPL, fun_plot='spl_hard', ld_ss=_s.gi['ld_ss'])
				return
			elif lt[0] >= s_ext[0] and lt[0] <= s_ext[1] and \
				lt[1] <= s_ext[2] and lt[1] >= s_ext[3]:  # PARTLY ON TOP OF SHIP
				_s.zorder = ship.zorder + 1
				# _s.gi['scale_vector'], _s.gi['lds_vec'] = gen_scale_lds(_s.NUM_FRAMES_SPL, fun_plot='spl_hard',
				#                                                         ld_ss=_s.gi['ld_ss'])
				return  # MUST RETURN CUZ OTHERWISE THE ZORDER GONNA BE MESSED UP NEXT ITER








