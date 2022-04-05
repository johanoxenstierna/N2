import numpy as np

import P
from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
import random

class Expl(AbstractLayer, AbstractSSS):

	"""Each ship gets X copies of all the expls (1 each per default)"""

	def __init__(_s, id, pic, ship, ch):
		AbstractLayer.__init__(_s)

		# _s.pic = pic
		# _s.id = id

		_s.gi = deepcopy(ship.gi['xtras'][ship.id + "_expls"])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_EXPL = 3
		_s.TRACER_L_R = _s.gi['tracer_l_r']
		_s.TRACER_PROB = 0.1  # more = more tracer

	def comp_extent_alpha_expl(_s):
		left = _s.ship.extent[_s.frame_ss[0]][0] + _s.gi['offset'][0] + \
		       random.randint(-_s.gi['offset_rand'][0], _s.gi['offset_rand'][0])
		right = left + _s.pic.shape[1]
		down = _s.ship.extent[_s.frame_ss[0]][2] + _s.gi['offset'][1] + \
		       random.randint(-_s.gi['offset_rand'][1], _s.gi['offset_rand'][1])
		up = down - _s.pic.shape[0]

		_s.extent = [[left, right, down, up]] #* _s.NUM_FRAMES_EXPL
		_s.extent = np.asarray(_s.extent * _s.NUM_FRAMES_EXPL)
		if random.random() < _s.TRACER_PROB:
			_s.tracer_expl()  # modifies _s.extent

		# _s.extent = np.array([[left, right, down, up], [left, right, down, up], [left, right, down, up]])

	def tracer_expl(_s):

		cur_l = _s.extent[0][0]
		cur_d = _s.extent[0, 3]  # use up (small arms)
		width = 50
		height = 1
		for i in range(1, _s.NUM_FRAMES_EXPL):  # 1 can be changed here
			if _s.TRACER_L_R == 'left':
				cur_l -= 100
				cur_l = max(0, cur_l)
			else:
				cur_l += 100
				cur_l = min(cur_l, 720)
				if P.MAP_SIZE == 'small':
					cur_l = min(cur_l, 488)

			right = cur_l + width
			right = min(right, 720)
			if P.MAP_SIZE == 'small':
				right = min(right, 488)

			_s.extent[i] = [cur_l, right, cur_d, cur_d - height]  # tracer always added to right of cur_l

		aa =5









