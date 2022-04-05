import numpy as np

import P
from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
from src.trig_functions import _normal
import random

class Spl(AbstractLayer, AbstractSSS):

	"""Each ship gets X copies of all the expls (1 each per default)"""

	def __init__(_s, id, pic, ship, ch):
		AbstractLayer.__init__(_s)

		_s.gi = deepcopy(ship.gi['xtras'][ship.id + "_spls"])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_SPL = 130


	def comp_extent_alpha_spl(_s):
		left = _s.ship.extent[_s.frame_ss[0]][0] + _s.gi['offset'][0] + \
		       random.randint(-_s.gi['offset_rand'][0], _s.gi['offset_rand'][0])
		right = left + _s.pic.shape[1]
		down = _s.ship.extent[_s.frame_ss[0]][2] + _s.gi['offset'][1] + \
		       random.randint(-_s.gi['offset_rand'][1], _s.gi['offset_rand'][1])
		up = down - _s.pic.shape[0]

		_s.extent = [[left, right, down, up]]  # * _s.NUM_FRAMES_EXPL
		_s.extent = np.asarray(_s.extent * _s.NUM_FRAMES_SPL)
		# _s.extent = np.array([[left, right, down, up], [left, right, down, up], [left, right, down, up]])
		scale = _normal(np.arange(0, _s.NUM_FRAMES_SPL), mean=_s.NUM_FRAMES_SPL // 2, var=_s.NUM_FRAMES_SPL // 4, y_range=[0, 0.999])

		aa = 5
		# _s.extent = gen_extent_normal()








