import numpy as np

import P
from src.layers.abstract import AbstractLayer
from src.gen_extent_triangles import *
from src.gen_colors import gen_colors
import cv2
import random

class Sail(AbstractLayer):
	"""
	si denotes sail_info
	"""

	def __init__(_s, id, pic, ship):
		super().__init__()
		_s.pic = pic
		_s.id = id
		_s.ship = ship
		_s.gi = ship.gi['xtras'][id]

		# _s.frame_ss = [ship.frame_ss[0] + _s.gi['frame_ss'][0], ship.frame_ss[0] + _s.gi['frame_ss'][1]]
		_s.frame_ss = ship.frame_ss  # NEW
		lts = _s.gen_lts(ship)  # NOT T ANYMORE
		_s.finish_sail_info(lts)
		_s.extent, _s.extent_t, _s.scale_vector = _s.gen_extent_black(pic, ship, lts)
		_s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
			gen_triangles(_s.extent_t, _s.extent, _s.gi, pic)

		# if ship_info['id'] == '7':
		# _s.pic = gen_colors(pic)  # WILL BE USED
		_s.z_shear, _s.t_x_ver, _s.t_x_hor  = _s.gen_heights_troughs_transform()
		_s.zorder = _s.ship.gi['zorder'] - 1

		# _s.alpha_array = _s.gen_alpha()
		sfg = 6

	def finish_sail_info(_s, lts):
		"""
		max_ri is needed by warp_affine to limit the warp space
		"""

		# scale from ship
		_s.gi['scale_ss'] = _s.ship.gi['move']['scale_ss']

		# Convert from tl to ld since this is what the
		# ld_start = [lts_t[0][0], int(lts_t[0][1] + _s.pic.shape[0] * _s.ship.scale_vector[0])]  # left start stop
		# ld_stop = [lts_t[-1][0], int(lts_t[-1][1] + _s.pic.shape[0] * _s.ship.scale_vector[-1])]

		ld_start = [lts[0, 0], int(lts[0, 1] + _s.pic.shape[0] * _s.ship.scale_vector[0])]  # left start stop
		ld_stop = [lts[-1, 0], int(lts[-1, 1] + _s.pic.shape[0] * _s.ship.scale_vector[-1])]

		_s.gi['ld_ss'] = [ld_start, ld_stop]

		# _s.gi['ld_start'] = tl[0] + _s.pic.shape[0] * _s.gi['scale_ss'][0]
		# _s.gi['ld_end'] = tl[-1] + _s.pic.shape[0] * _s.gi['scale_ss'][0]
		index_with_most_ld_x = np.argmax([_s.gi['ld_ss'][0][0], _s.gi['ld_ss'][1][0]])
		_s.gi['max_ri'] = _s.gi['ld_ss'][index_with_most_ld_x][0] + _s.pic.shape[1] * \
		                                 _s.gi['scale_ss'][index_with_most_ld_x]

		adf = 5

	def gen_lts(_s, ship):
		"""
		Since the offset is given for extent, but mov_black is for triangles,
		a lt is needed in tri space. OBS BUT THE RETURN IS FOR extent domain, not extent_t!!!
		d_offset: OBS OBS OBS IS THE THING TO TUNE. LOOK HERE: ITS HOW HIGH RATIO THAT SAIL SITS FROM BOTTOM
		Since mov_black concerns the highest tri point but the sail starts somewhere below, this
		is manually set to reduce the amount of mov_black for sail.

		DEPRECATED replaced with normalize_ship_mov_black... tri_ship_mid_base:
		This is the mid-point (x) from which mov_x is computed. Since the sail starts at some
		random frame and doesn't know the base point from the ships frame of reference, mid_base is here computed
		as the mean of all ship tri mid point x coords. IS NOT GONNA BE EXACT
		"""

		# DECREASE_OFFSET = 0.7  # USED SINCE OFFSET IS FOR TOP TRI POINT (perhaps gona be unique for ship)
		# PEND DEL
		# assert(len(ship.tris) >= (_s.gi['frame_ss'][1] - _s.gi['frame_ss'][0]))

		lts = np.zeros((_s.frame_ss[1] - _s.frame_ss[0], 2))

		# PROB DEPR: OFFSET OBVIOUSLY NEEDS ADJUSTMENT W FRAMES
		# offset = [_s.gi['offset'][0] * ship.scale_vector[0], _s.gi['offset'][1] * ship.scale_vector[1]]
		# offset[0] += ship.extent[0, 0]
		# offset[1] += ship.extent[0, 3]

		# tri_ship_mid_x_base = np.mean([x[1][0] for x in ship.tris])  # OBS THIS MAY BE IMPRECICE: ITS NOT NORMALIZED WRT MOVEMENT. But at least it's done per frame
		tri_ship_mid_x_deltas = _s.normalize_ship_mov_black()  # OBS THIS MAY BE IMPRECICE: ITS NOT NORMALIZED WRT MOVEMENT. But at least it's done per frame

		for i in range(len(lts)):  # OBS CURRENTLY IT IS ASSUMED ALL THE MOVEMENT IS FOR TOP TRI POINT

			# tri_ship_mid_x_at_frame = ship.tris[_s.frame_ss[0] + i][1, 0]  # OBS this is second tri SO NEEDS D_OFFSET
			# tri_ship_mid_x_at_frame = ship.tris[i][1, 0]  # OBS this is second tri SO NEEDS D_OFFSET
			# if P.PR_MOVE_BLACK:  # FAILS BCS THIS IS EXTENT_T, NOT EXTENT
				# mov_x_mid = tri_ship_mid_x_at_frame - tri_ship_mid_x_base
			# else:
			mov_x_mid = 0  # MAJOR BUG DISCOVERED HERE. SAIL WAS MOVING FASTER THAN SHIP
			lt = [ship.extent[i, 0], ship.extent[i, 3]]  # start with ship lt
			lt[0] += _s.gi['offset'][0] * ship.scale_vector[i]  # offset wrt ship scale at frame LT

			if _s.id not in ['3_s_0', '2_s_0']:  # TODO: THIS HACKS THE 3_s_0 sail
				# lt[0] += mov_x_mid * ship.scale_vector[i] * _s.gi['d_offset']  # offset wrt mov black
				lt[0] += tri_ship_mid_x_deltas[i]
				# pass

			lt[1] += _s.gi['offset'][1] * ship.scale_vector[i]

			# DEPR DONT SEE WHY MOV_Y_TOP IS NEEDED
			# mov_y_top = ship.tris[_s.gi['frame_ss'][0] + i][1, 1] - ship.tris[_s.gi['frame_ss'][0]][1, 1]  # assuming linear motion of course

			lts[i, 0] = lt[0]
			lts[i, 1] = lt[1]

		return lts  # left tops WRT t!

	def normalize_ship_mov_black(_s):
		"""In order to know how mucht top of mast moves, the x, y movement must be eliminated"""
		tri_ship_mid_x_deltas = np.zeros((_s.frame_ss[1] - _s.frame_ss[0], 1))
		# ship_tot_x_mov = _s.ship.extent[-1, 0] - _s.ship.extent[0, 0]
		# ship_tot_y_mov = _s.ship.extent[-1, 2] - _s.ship.extent[0, 2]

		# BELOW FOR LOOP FAILS IF MOV_BLACK DOES NOT START IN MIDDLE HENCE THIS IS NEEDED:
		first_without_mov_black_x = (_s.ship.tris[0][0, 0] + _s.ship.tris[0][2, 0]) / 2
		first_actual_x = _s.ship.tris[0][1, 0]
		constant_shift = (first_actual_x - first_without_mov_black_x) * -1  # neg means shift to right needed

		for i, tri in enumerate(_s.ship.tris):
			without_mov_black_x = (tri[0, 0] + tri[2, 0]) / 2  # WITHOUT MOV BLACK. SAME AS EXTENT_T
			actual_x = tri[1, 0]  # MID TRI X
			delta_x = (actual_x - without_mov_black_x) * _s.gi['d_offset']  # d_offset to reduce effect of movement since sail does not start at top of mast
			tri_ship_mid_x_deltas[i] = delta_x + constant_shift

		return tri_ship_mid_x_deltas

	def gen_extent_black(_s, pic, ship, lts):
		"""
		This function is unique to sails i.e. kept inside this class since they must follow the roll movement.
		TODO
		"""

		width = pic.shape[1]
		height = pic.shape[0]

		scale_vector = np.linspace(_s.gi['scale_ss'][0], _s.gi['scale_ss'][1], len(lts))

		extent = np.zeros((len(lts), 4))
		extent_t = np.zeros((len(lts), 4))

		for i in range(len(lts)):

			width_m = width * scale_vector[i]
			height_m = height * scale_vector[i]

			extent[i, 0] = lts[i, 0]  # NOT CORRECT BCS LTS IS t!
			extent[i, 1] = lts[i, 0] + width_m
			extent[i, 2] = lts[i, 1] + height_m
			extent[i, 3] = lts[i, 1]

			extent_t[i] = [extent[i, 0] - extent[0, 0],  # left
			               extent[i, 1] - extent[0, 0],  # right
			               extent[i, 2] - extent[0, 3],  # down
			               extent[i, 3] - extent[0, 3]]  # up

		return extent, extent_t, scale_vector

	def gen_alpha(_s):
		return 0

	def change_brightness(value, ship_pic):
		"""
		NOt used currently
        OBS if brightness reaches threshold things WILL get messed up, e.g. brightness cannot be restored ok.
        """
		img = ship_pic
		hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
		h, s, v = cv2.split(hsv)
		v += value
		final_hsv = cv2.merge((h, s, v))
		img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
		img[:, :, 0:3] = img2

		# think this is just the operation to sort out alpha
		idx0 = np.argwhere(img[:, :, 0:3] < 0.0)
		idx1 = np.argwhere(img[:, :, 0:3] > 1.0)

		for row, col, ch in idx0:
			img[row, col, ch] = 0.0

		for row, col, ch in idx1:
			img[row, col, ch] = 1.0

		return img

	def gen_heights_troughs_transform(_s):
		"""
		NEW FIX: EVERYTHING HORIZ REMOVED (NOT NEEDED)
		ALSO, ALL THE SINNING IS DONE WHEN ANIMATING (SINCE SHIFT NEEDED INSIDE SIN)
		WILL BECOME ABSTRACT FOR ALL LAYERS THAT NEED TRIGONOMETRIC COLOR TRANSFORMS
		cycling and shifting shear
		For cycling noise is required since it's too obvious otherwise: CURRENTLY NOT VERY GOOD, TODO: FIX
		ver denotes axis at which the trough/high follows (think shirt).
		One special thing about e.g. sails is that they take the scaling vector from ship its parent.

		PARAMS:
		cycles: ???
		sh_cyc: shear_cycles  (NO REAL IMPACT SINCE CYCLES NOT REALLY USED)
		sh_mm: shear min/max GIVES INTENSITY
		sh_dist: shear distribution between shifting and cycling
		num_cyc_ver: ver here is what looks like horizontal lines (transform for each col)
		num_cyc_hor: hor here is what looks like vertical lines (transform for each row)
		sh_ver_incr: increase_in_shear_ver. SEEMS TO AFFECT DIRECTION EVENLY THROUGHOUT ITERS
		sh_hor_incr
		"""

		# shear_cycles = 5  # 16 HOW MANY TIMES IT GOES BACK/FORTH
		# shear_min = 0.2  # 0.1 these guys seem to affect the speed and direction of the shear
		# shear_max = 0.9  # 0.5
		# shear_range = (_s.gi['sh_mm'][1] - _s.gi['sh_mm'][0]) / 2  # div by 2 since it's applied to both pos and neg numbers
		# shear_distribution = [0.98, 0.02]  # shifting and cycling
		#
		# # THESE DICTATE HOW MANY THROUGHT/TOPS THERE WILL BE
		# num_cycles_ver = 1.2  # 30  # hor here is what looks like vertical lines
		# num_cycles_hor = 1.2  # 10
		# weird_multiplier_ver = 50
		# weird_multiplier_hor = 5
		# increase_in_shear_ver = 0.08
		# increase_in_shear_hor = 0.03

		# SHIFTING  # lines going in one direction
		# z_shear_shifting = np.linspace(_s.gi['sh_mm'][0], _s.gi['sh_mm'][1], _s.ship.frames_tot)

		# CYCLING  # lines going back and forth
		# z_shear_cycling_x = np.linspace(0, _s.gi['sh_cyc'] * 2 * np.pi, _s.ship.frames_tot)
		# z_shear_cycling_rand_x = np.zeros((_s.ship.frames_tot))

		# cur_pos = z_shear_cycling_x[0]
		# for i in range(_s.ship.frames_tot):  # OBS range of values odn\t matter here since sin will be taken
		# 	z_shear_cycling_rand_x[i] = cur_pos
		#
		# 	# Linear component and random component (otherwise the random component blows up)
		# 	cur_pos = 0.9 * z_shear_cycling_x[i] + 0.1 * (cur_pos + random.random() * random.choice([-1, 1]))

		# aa = np.sin(z_shear_cycling_rand_x * 6)/6
		# z_shear_cycling = (0.9 * np.sin(z_shear_cycling_x) + 0.1 * np.sin(
		# 	z_shear_cycling_rand_x * 2)) * shear_range + shear_range + _s.gi['sh_mm'][0]

		# assert (max(z_shear_shifting) <= _s.gi['sh_mm'][1])
		# assert (min(z_shear_shifting) >= _s.gi['sh_mm'][0])
		# assert (max(z_shear_cycling) <= _s.gi['sh_mm'][1])
		# assert (min(z_shear_cycling) >= _s.gi['sh_mm'][0])

		# z_shear = z_shear_shifting * _s.gi['sh_dist'][0] + z_shear_cycling * _s.gi['sh_dist'][1]
		# z_shear *= 10  # THIS IS HOW MUCH SAIL IS SHIFTED PER FRAME

		# SUPER IMPORTANT: THIS GIVES THE SHEAR SPEED (3 for 300, 12 for 600
		z_shear = np.linspace(0, P.FRAMES_TOT // 25, num=_s.ship.frames_tot)  # 53: 28. OBS sinned later TUNE stop value for number of frames

		# THESE GIVE HOW MUCH THE SHEAR SHOULD CHANGE THROUGH TIME (CYCLES
		t_x_ver = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))  # will be sinned
		t_x_hor = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))

		# # PEND DEL VERTICAL SHAPE (TRANS APPLIED TO ROWS)
		# start_val = 0  # THE ONLY THING THAT ARANGE CONTRIBUTES HERE IS REMOVAL OF SQUARY SHAPE IN ANIMATION
		# stop_val = _s.gi['num_cyc_ver']
		# # step_size = 1.0001 * _s.gi['num_cyc_ver'] / t_x_ver.shape[1]  # distance between hills?
		# for i in range(_s.pic.shape[0]):
		# 	# ver_x_base = np.linspace(0, int(_s.gi['num_cyc_ver']), num=_s.pic.shape[1])  # QUALITY LOSS HERE
		# 	ver_x_base = np.arange(start=start_val, stop=stop_val, step=step_size)
		# 	# t_x_ver[i, :len(ver_x_base)] = _s.gi['weird_multiplier_ver'] * (np.sin(ver_x_base) * 0.5 + (1 - 0.5))
		# 	t_x_ver[i, :] =np.sin(ver_x_base) * 0.5 + (1 - 0.5)
		#
		# 	_s.gi['num_cyc_ver'] += _s.gi['sh_ver_incr']  # too much=slows down movement
		# 	start_val += _s.gi['sh_ver_incr']
		# 	stop_val += _s.gi['sh_ver_incr'] / 2
		# 	# step_size += 0.001 * step_size

		ver_x_base = np.linspace(0, np.pi * 5, num=_s.pic.shape[1])  # /pi = number of hills
		multiplier = 1  # how much shorter the hills become the further down on the sail
		for i in range(_s.pic.shape[0]):
			# t_x_ver[i, :] = np.sin(ver_x_base) * _s.gi['col_diff'] + (1 - _s.gi['col_diff'])
			t_x_ver[i, :] = ver_x_base * multiplier
			multiplier *= 1.01

		# # PEND DEL HORIZ SHAPE (TRANS APPLIED TO COLS)
		# start_val = 0
		# stop_val = _s.gi['num_cyc_hor']
		# step_size = 1.000001 * _s.gi['num_cyc_hor'] / t_x_hor.shape[0]  # never changes. Mult makes sure it's always fittable within t_x_ver
		# for i in range(_s.pic.shape[1]):
		# 	# hor_x_base = np.linspace(0, int(_s.gi['num_cyc_ver']), num=_s.pic.shape[0])
		# 	hor_x_base = np.arange(start=start_val, stop=stop_val, step=step_size)
		# 	t_x_hor[:len(hor_x_base), i] = _s.gi['weird_multiplier_hor'] * np.sin(hor_x_base) * 0.5 + (1 - 0.5)
		# 	_s.gi['num_cyc_hor'] += _s.gi['sh_hor_incr']  # too much=slows down movement
		# 	start_val += _s.gi['sh_hor_incr']
		# 	stop_val += _s.gi['sh_hor_incr'] / 2
		# 	step_size += 0.001 * step_size

		# # TEMP (to debug viewer)
		y_ver = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
		aa = np.sin(t_x_ver + z_shear[0]) * _s.gi['col_diff'] + (1 - _s.gi['col_diff'])
		aa *= _s.gi['col_diff'] + (1 - _s.gi['col_diff'])

		# hor_x_base = np.linspace(0, 20, num=_s.pic.shape[0])  # /pi = number of hills
		# multiplier = 1  # how much shorter the hills become the further down on the sail
		# for i in range(_s.pic.shape[1]):
		# 	# t_x_ver[i, :] = np.sin(ver_x_base) * _s.gi['col_diff'] + (1 - _s.gi['col_diff'])
		# 	t_x_hor[:, i] = hor_x_base * multiplier
		# 	multiplier *= 1.01

		return z_shear, t_x_ver, t_x_hor

	def apply_heights_troughs_transform(_s, pic, iii):

		"""
		This is run on the readonly pic of ship at the internal clock
		col_diff: 0-0.5  Heights and troughs in the pic. Can't be more than 0.5 since  0.5 neg + 0.5 pos = 1.0 i.e. max
		col_diff DOES not have the same range for colors (0.5-1.0) as it does for alpha (0.0 - 1.0). It is
		therefore NORMALIZED to 0-1 range
		"""

		# alpha_diff = 0.6
		
		# APPLY SIN TO T_X_ MATS[i] AND Z_SHEAR VECTORS (CAN'T BE PRECOMPUTED BECAUSE CLOCK NEEDED HERE)
		y_ver = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
		# y_hor = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
		# y_hor = np.ones((_s.pic.shape[0], _s.pic.shape[1]))
		# for i in range(_s.pic.shape[0]):  # per row
		# 	# col diff first squeezes the curve down to desired range, then shifts it up to positive
		# 	# y_ver[i, :] = (np.sin(_s.t_x_ver[i, :]) + _s.z_shear[_s.clock]) * _s.gi['col_diff'] + \
		# 	#               (1 - _s.gi['col_diff'])  # / 4 means y range is -.25 to .25
		# 	y_ver[i, :] = np.sin(_s.t_x_ver[i, :]) * _s.gi['col_diff'] + (1 - _s.gi['col_diff'])  # / 4 means y range is -.25 to .25

		y_ver = np.sin(_s.t_x_ver + _s.z_shear[_s.clock]) * _s.gi['col_diff'] + (1 - _s.gi['col_diff'])
		# y_ver /= np.max(y_ver)

		# for i in range(_s.pic.shape[1]):
		# 	y_hor[:, i] = (np.sin(_s.t_x_hor[:, i] * _s.z_shear[_s.clock])) * _s.gi['col_diff'] + \
		# 	              (1 - _s.gi['col_diff'])

		# y_col = y_ver * y_hor
		# y_alpha = (y_ver * 0.5 + y_hor * 0.5) / 2
		y_alpha = y_ver
		y_col = y_ver

		# NORMALIZATION FOR ALPHA CHANGE
		mn, mx = np.min(y_alpha), np.max(y_alpha)
		y_alpha = (((y_alpha - mn) / (mx - mn)) * _s.gi['alpha_diff']) + (1 - _s.gi['alpha_diff'])

		ex = 1.0
		# if iii in firing_frames:
		# 	ex = 0.84  # decrease in green and blue
		# pic = _s.pic.copy()  # REQUIRED
		pic[:, :, 0] = pic[:, :, 0] * y_col  # more y=more red, less=more green
		pic[:, :, 1] = pic[:, :, 1] * ex * y_col  # more y=more green, less=more red
		pic[:, :, 2] = pic[:, :, 2] * ex * y_col  # Needed to complement red and green
		alpha_shift = pic[:, :, 3] * y_alpha  # will prob not be y
		pic[:, :, 3] = alpha_shift

		return pic




