import json
import uuid
import random
import numpy as np
from src.trig_functions import _normal

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
		_s.final_tests()
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

		_s.ch['backgr'] = {"brightness_frame_value": [[20, -0.01], [50, 0.01], [999999, 0.0]],
		                   "clock": 0}

		# with open('./utils/bc_template.json', 'r') as f:
		# _s.bc_template = json.load(f)

		_s.init_bc()

		ship_infos_name = 'ship_infos'
		if P.MAP_SIZE == 'small':
			ship_infos_name = 'ship_infos_small'

		for ship_nid in P.SHIPS_TO_SHOW:  # number_id
			try:
				with open('./sh_info/' + P.MAP_SIZE + '/' + ship_nid + '.json', 'r') as f:
					ship_info = json.load(f)
			except:
				raise Exception("Haven't done ship info for big yet: " + str(ship_nid))

			_s.ch['ships'][ship_nid] = ship_info  # needed for chronicler AI
			kk = 8

	def run(_s):
		"""Think about how this is gona be iterated. Per ship or per iteration"""

		for ship_id, ship in _s.ch['ships'].items():
			_s.firing_init_frames(ship)
			_s.smoka_init_frames(ship)  # use firing means
		pass

	def firing_init_frames(_s, ship):

		X = np.arange(0, P.FRAMES_TOT)  # large: 960
		YS = []  # combination of normal distribution centered at pre-specified locations
		num_tot = np.sum([x for x in ship['firing_info']['nums']])

		for i in range(len(ship['firing_info']['nums'])):
			num = ship['firing_info']['nums'][i]
			try:
				mean = ship['firing_info']['means'][i]
			except:
				raise Exception("different number of numns and mean in firing_info for ship: " + str(ship['id']))
			var = ship['firing_info']['var']

			Y = _normal(X, mean=mean, var=var, y_range=[0, 1])

			# TODO weigh y_range with num (so that bigger broadsides will be shown)

			YS.append((num / num_tot) * Y)

		Y = np.sum(YS, axis=0)  # sum along rows (element wise)
		Y = Y / np.sum(Y)  # this makes it sum to 1.

		# THIS IS INSTEAD CHECKED BY THE SMOKES THEMSELVES
		# flag_no_frames_too_late = True
		# while flag_no_frames_too_late:
		# 	frames = np.random.choice(range(len(Y)), size=num_tot, p=Y)
		# 	for frame in frames:
		# 		aa = 5
		# frames.sort()
		# aa = list(map(int, frames))

		frames = np.random.choice(range(len(Y)), size=num_tot, p=Y)
		frames.sort()
		ship['firing_frames'] = list(map(int, frames))

		if frames[-1] >= P.FRAMES_STOP:
			raise Exception("firing frame outside frame_ss max ship: " + str(ship['id']))

	def smoka_init_frames(_s, ship):
		"""
		ship IS the gi at this point (just the JSON)
		OBS Strictly 1 per smoka (following same indexing as pic names generated later)
		frame_sss IS WITH REFERENCE TO THE SHIPS frame_ss.
		Smokas not tied to expls frames, smokrs are
		CURRENTLY THESE ARE ALL HARDCODED
		"""

		aa = 5

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

	def final_tests(_s):

		# try:
		sh_3 = _s.ch['ships']['3']

		for frame_start in sh_3['smokas_hardcoded']['frames_start']:
			if sh_3['smokas_hardcoded']['frames_start'].count(frame_start) > 1:
				raise Exception("can't be same start frame AAAREHHF")
		# except:
		# 	print("cant test ship 3")


		for ship_id, ship in _s.ch['ships'].items():
			f_nums = ship['firing_info']['nums']
			f_means = ship['firing_info']['means']
			if len(f_nums) != len(f_means):
				raise Exception("nums and means must be same length id: " + ship_id)

			smokas_h_frames_start = ship['smokas_hardcoded']['frames_start']
			smokas_h_frames_stop = ship['smokas_hardcoded']['frames_stop']
			smokas_h_ids = ship['smokas_hardcoded']['ids']
			if len(smokas_h_frames_start) != len(smokas_h_frames_stop):
				raise Exception("smokas_h_frames_start) != len(smokas_h_frames_stop: " + ship_id)

			if len(smokas_h_frames_stop) != len(smokas_h_ids):
				raise Exception("smokas_h_frames_stop) != len(smokas_h_ids): " + ship_id)

		if '3' in _s.ch['ships']:
			if _s.ch['ships']['3']['move']['frame_ss'][1] * 1.1 < P.FRAMES_STOP:
				raise Exception("Ship 3 must go whole way otherwise smokhs wont work")

		# TODO: check that smokhs lists are equal length for each ship


	def export(_s):

		if OVERWRITE:
			name = 'chronicle'
		else:
			name = 'chronicle_' + str(uuid.uuid4())[0:4]

		with open('./src/' + name + '.json', 'w') as f:
			json.dump(_s.ch, f, indent=4)


if __name__ == "__main__":
	Chronicler()


