import json
import uuid
import random

import P as P

OVERWRITE = 1



class Chronicler:
	"""
	Class that says when explosions, splashes and smokes are triggered.
	"""

	def __init__(_s):
		_s.ch = {}
		_s.possible_bc_locs, _s.zorders = _s.get_possible_bc_locs(P.MAP_SIZE)
		_s.init_chronicle()
		_s.run()
		_s.export()

	def get_possible_bc_locs(_s, map_size):
		if map_size == 'small':
			locs = [[405, 83], [288, 130], [49, 134]]
			zorders = [6, 6, 6]
		else:
			# d_0,  battleshipfar, d_1,d_2, d_3, d_4,  d_5
			locs = [[1148, 466],
			        [1168, 467],
			        [1111, 425], [1034, 456], [1015, 456], [888, 450], [906, 452],
			        [660, 433], [487, 429], [433, 422], [272, 419], [196, 411],
			        [127, 448]]
			zorders = [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
		return locs, zorders

	def init_chronicle(_s):
		"""
		For ships it just loads ship_info into memory.
		"""

		_s.ch['ships'] = {}
		_s.ch['bc'] = []

		if P.MAP_SIZE == 'small':
			spl_zone_centroids = [[], [300, 100], [350, 100], [350, 150], [350, 100], [350, 100], [100, 130], [100, 50]]
		else:
			spl_zone_centroids = [[], [848, 477], [687, 464], [468, 548], [660, 584], [300, 497], [973, 468], [1100, 476]]
		_s.ch['backgr'] = {"brightness_frame_value": [[20, -0.01], [50, 0.01], [999999, 0.0]],
		                   "clock": 0,
		                   "spl_zone_centroids": spl_zone_centroids}

		# with open('./utils/bc_template.json', 'r') as f:
		# _s.bc_template = json.load(f)

		_s.init_bc()

		ship_infos_name = 'ship_infos'
		if P.MAP_SIZE == 'small':
			ship_infos_name = 'ship_infos_small'

		for ship_nid in P.SHIPS_TO_SHOW:  # number_id
			try:
				with open('./ship_info/' + P.MAP_SIZE + '/' + ship_nid + '.json', 'r') as f:
					ship_info = json.load(f)
			except:
				raise Exception("Haven't done ship info for big yet")

			_s.ch['ships'][ship_nid] = ship_info  # needed for chronicler AI
			kk = 8

	def run(_s):
		"""Think about how this is gona be iterated"""
		# _s.smoka_init_frames()
		pass
	# aa = _s.ch['ships']['7']
	# aa = 5

	def smoka_init_frames(_s):
		"""
		OBS Strictly 1 per smoka (following same indexing as pic names generated later)
		frame_sss IS WITH REFERENCE TO THE SHIPS frame_ss.
		Smokas not tied to expls frames, smokrs are
		TODO: currently it's just some random values here
		"""

		for ship_id, ship in _s.ch['ships'].items():
			num_frames_ship = ship['move']['frame_ss'][1] - ship['move']['frame_ss'][0]
			for xtra_id, xtra in ship['xtras'].items():
				if xtra_id.split('_')[1] == 'a':
					for i in range(0, P.NUM_SMOKAS):
						xtra_id_2 = xtra_id + '_' + str(i)
						rand_frame_start = random.randint(5, 10)
						rand_frame_stop = 200  #rand_frame_start + random.randint(10, 20)
						# AGAIN OBS, THIS IS WRT SHIP FRAME_SS, SO IF SHIP SS IS [5, 50] AND SMOKE SS IS [10, 20], THE SMOKE WILL START AT FRAME 15
						assert(rand_frame_stop < num_frames_ship)

						xtra['frame_sss'][xtra_id_2] = [rand_frame_start, rand_frame_stop]

						xtra['scale_sss'][xtra_id_2] = [0.1, 1.0]
						aa = 5

			fdf = 5
		adf = 5

	def check_arrays_not_empty(_s):

		for ship_id, ship in _s.ch['ships'].items():
			if len(ship['firing_frames']) < 1:
				ship['firing_frames'].append([P.FRAMES_START, P.FRAMES_START + 10, P.FRAMES_START + 20, P.FRAMES_START + 30])
				print("WARNIGN FEW firing_frames for ship " + ship_id)

			if len(ship['splash_zones']) < 1:
				ship['splash_zones'].append([P.FRAMES_START, P.FRAMES_START + 10, P.FRAMES_START + 20, P.FRAMES_START + 30])
				print("WARNIGN FEW splash_zones for ship " + ship_id)

			if len(ship['xtra_init_frames']) < 1:
				ship['xtra_init_frames'].append([P.FRAMES_START, P.FRAMES_START + 10, P.FRAMES_START + 20, P.FRAMES_START + 30])
				print("WARNIGN FEW xtra_init_frames for ship " + ship_id)



		aa = 5

	def init_bc(_s):
		"""
		So that bc smokas appear at beg of video
		"""
		frame = 1
		for ind in range(1, len(_s.possible_bc_locs)):  # EXCLUDES rightmost ship
			# bc = deepcopy(_s.bc_template)
			bc = {}
			bc['frame'] = frame
			bc['tl'] = _s.possible_bc_locs[ind]
			bc['zorder'] = _s.zorders[ind]
			bc['left_right'] = 'l'  # not sure about this (think the right one is fixed in animate
			_s.ch['bc'].append(bc)
			frame += 1

	def export(_s):

		if OVERWRITE:
			name = 'chronicle'
		else:
			name = 'chronicle_' + str(uuid.uuid4())[0:4]

		with open('./src/' + name + '.json', 'w') as f:
			json.dump(_s.ch, f, indent=4)


if __name__ == "__main__":
	Chronicler()


