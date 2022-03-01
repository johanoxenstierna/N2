from src.gen_extent_triangles import *
from copy import deepcopy
from src.layers.abstract import AbstractLayer
import random

class Smoke(AbstractLayer):

	def __init__(_s, id, pic, ship, ch, type):
		super().__init__()
		_s.pic = pic
		_s.id = id
		_s.ship = ship

		id_split = _s.id.split('_')  # the last index (number of same pictures) needs removing for gi
		id_gi = id_split[0] + '_' + id_split[1] + '_' + id_split[2]
		_s.gi = deepcopy(ship.gi['xtras'][id_gi])  # gona be written

		# FRAME_SS MAKES SENSE TO FIRST COMPUTE IN CH, SEE GET_LD_SS() NEEDS INPUT
		_s.frame_ss = ch['ships'][ship.id]['xtras'][id_gi]['frame_sss'][id]
		_s.ld_ss = _s.get_ld_ss()
		# _s.ld_ss = ch['ships'][ship.id]['xtras'][id_gi]['ld_sss'][id]

		# THIS ONE PROBABLY ALSO NEEDS TO BE DONE IN FUNCTINO
		_s.scale_ss = ch['ships'][ship.id]['xtras'][id_gi]['scale_sss'][id]

		_s.gi['frame_ss'] = _s.frame_ss
		_s.gi['ld_ss'] = _s.ld_ss
		_s.gi['scale_ss'] = _s.scale_ss

		_s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(_s.gi, pic, ship)
		_s.finish_smoke_info()
		_s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
			gen_triangles(_s.extent_t, _s.extent, _s.gi, pic)


	def finish_smoke_info(_s):
		"""
		This will be same as sail except that its much simpler cuz extent_black not used
		Just takes max from extent[:, 1]
		"""
		_s.gi['max_ri'] = np.max(_s.extent[:, 1])

	def get_ld_ss(_s):

		extent_ship_at_smoka_start = _s.ship.extent[_s.frame_ss[0]]
		extent_ship_at_smoka_stop = _s.ship.extent[_s.frame_ss[1]]

		# FIRST SET IT TO BE SAME LD AS SHIP AT FRAME
		ld_ss = [[extent_ship_at_smoka_start[0], extent_ship_at_smoka_start[2]],
		         [extent_ship_at_smoka_stop[0], extent_ship_at_smoka_stop[2]]]

		# ADD SMOKA OFFSET
		ld_ss[0][0] += _s.ship.gi['smoka_offset'][0]
		ld_ss[0][1] += _s.ship.gi['smoka_offset'][1]
		ld_ss[1][0] += _s.ship.gi['smoka_offset'][0]
		ld_ss[1][1] += _s.ship.gi['smoka_offset'][1]

		# ADD RAND
		ld_ss[0][0] += random.randint(-10, 5)
		ld_ss[0][1] += random.randint(-10, 5)
		ld_ss[1][0] += -140  #random.randint(-10, 5)
		ld_ss[1][1] += random.randint(-10, 5)

		return ld_ss





