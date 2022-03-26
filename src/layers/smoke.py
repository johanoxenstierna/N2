from src.gen_extent_triangles import *
from src.gen_alpha import gen_alpha
from copy import deepcopy
from src.layers.abstract import AbstractLayer, AbstractSSS
import random


class Smoke(AbstractLayer, AbstractSSS):

	def __init__(_s, id, pic, ship, ch, type):
		AbstractLayer.__init__(_s)

		_s.id = id
		id_split = _s.id.split('_')  # the last index (number of same pictures) needs removing for gi
		id_gi = id_split[0] + '_' + id_split[1] + '_' + id_split[2]
		_s.gi = deepcopy(ship.gi['xtras'][id_gi])  # OBS CERTAIN THINGS HERE MUST BE THERE FOR ALL

		AbstractSSS.__init__(_s, ship, id, pic)
		_s.NUM_FRAMES_SMOKA = 50

		'''
		FIXED MAJOR REFACTOR NEEDED. NOT PLAUSIBLE TO PREGEN EVERYTHING FOR SMOKRS (AND EXPLS) and maybe even smokas
		Instead each ship gets a token amount of smokrs and expls and maintains the queue system. TODO
		OLD: Hence separate out the below into a function and only pregen it for smokas (if possible). 
		New: Smokas are gonna use same queing system as smokrs, sails and expls
		'''

		# This need to be dynamic ===========
		# _s.ld_ss = _s.get_ld_ss()
		#
		# # THIS ONE PROBABLY ALSO NEEDS TO BE DONE IN FUNCTINO
		# _s.scale_ss = ch['ships'][ship.id]['xtras'][id_gi]['scale_sss'][id]
		#
		# _s.gi['frame_ss'] = _s.frame_ss
		# _s.gi['ld_ss'] = _s.ld_ss
		# _s.gi['scale_ss'] = _s.scale_ss

		# _s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, pic, ship)
		# _s.finish_smoke_info()
		# _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
		# 	gen_triangles(_s.extent_t, _s.extent, _s.gi, pic)

	def gen_dyn_extent_alpha(_s):
		"""Needs to be here cuz finish_smoke_info is"""
		_s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, _s.pic, _s.ship)
		_s.finish_smoke_info()
		_s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
			gen_triangles(_s.extent_t, _s.extent, _s.gi, _s.pic)
		_s.alpha = gen_alpha(_s.gi, fun_plot='smoka')
		aa = 5

	def finish_smoke_info(_s):
		"""
		This will be same as sail except that its much simpler cuz extent_black not used
		Just takes max from extent[:, 1]
		"""
		_s.gi['max_ri'] = np.max(_s.extent[:, 1])

	# def get_ld_ss(_s, ii):
	#
	# 	extent_ship_at_smoka_start = _s.ship.extent[_s.frame_ss[0]]
	# 	extent_ship_at_smoka_stop = _s.ship.extent[_s.frame_ss[1]]
	#
	# 	# FIRST SET IT TO BE SAME LD AS SHIP AT FRAME
	# 	ld_ss = [[extent_ship_at_smoka_start[0], extent_ship_at_smoka_start[2]],
	# 	         [extent_ship_at_smoka_stop[0], extent_ship_at_smoka_stop[2]]]
	#
	# 	# ADD SMOKA OFFSET
	# 	ld_ss[0][0] += _s.ship.gi['smoka_offset'][0]
	# 	ld_ss[0][1] += _s.ship.gi['smoka_offset'][1]
	# 	# ld_ss[1][0] += _s.ship.gi['smoka_offset'][0]
	# 	# ld_ss[1][1] += _s.ship.gi['smoka_offset'][1]
	#
	# 	# ADD RAND
	# 	ld_ss[0][0] += random.randint(-30, 30)  # left start
	# 	ld_ss[0][1] += random.randint(-10, 5)  # down  start
	# 	ld_ss[1][0] = ld_ss[0][0] + random.randint(-150, -100)  # left stop
	# 	ld_ss[1][1] = ld_ss[0][1] + random.randint(-30, -10)  # down stop
	#
	# 	return ld_ss





