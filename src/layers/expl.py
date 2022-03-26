

from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
import random

class Expl(AbstractLayer, AbstractSSS):

	def __init__(_s, id, pic, ship, ch):
		AbstractLayer.__init__(_s)

		# _s.pic = pic
		# _s.id = id

		_s.gi = deepcopy(ship.gi['xtras'][ship.id + "_expls"])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_EXPL = 1

	def set_extent_expl(_s):
		left = _s.ship.extent[_s.frame_ss[0]][0] + _s.gi['offset'][0] + \
		       random.randint(-_s.gi['offset_rand'][0], _s.gi['offset_rand'][0])
		right = left + _s.pic.shape[1]
		down = _s.ship.extent[_s.frame_ss[0]][2] + _s.gi['offset'][1] + \
		       random.randint(-_s.gi['offset_rand'][1], _s.gi['offset_rand'][1])
		up = down - _s.pic.shape[0]
		# _s.extent = np.array([[left, right, down, up], [left, right, down, up], [left, right, down, up], [left, right, down, up]])
		_s.extent = np.array([left, right, down, up])
		aa = 5
	# def set_expl_clock(_s):
	# 	pass






