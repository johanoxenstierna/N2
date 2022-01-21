import numpy as np
from src.layers.abstract import AbstractLayer
from src.gen_extent_triangles import *
import cv2


class Sail(AbstractLayer):

	def __init__(_s, id, pic, ship):
		super().__init__()
		_s.pic = pic
		_s.id = id
		_s.ship = ship
		_s.sail_info = ship.ship_info['xtras'][id]

		_s.frame_ss = [ship.frame_ss[0] + _s.sail_info['frame_ss'][0], ship.frame_ss[0] + _s.sail_info['frame_ss'][1]]
		tl = _s.gen_tl(ship)
		_s.finish_sail_info(tl)
		_s.extent_t, _s.extent, _s.scale_vector = _s.gen_extent_black(pic, ship, tl)
		# _s.tri_base, _s.tris, _s.tri_max_x, _s.tri_max_y, _s.tri_min_x, _s.tri_min_y, _s.mask_x, _s.mask_y = \
		# 	gen_triangles(_s.extent_t, _s.extent, _s.sail_info, pic)

		_s.tri_base, _s.tris, _s.tri_max_le, _s.tri_max_ri, _s.tri_max_do, _s.tri_min_x, _s.tri_min_y, \
			_s.mask_ri, _s.mask_do = gen_triangles(_s.extent_t, _s.extent, _s.sail_info, pic)

		_s.alpha_array = _s.gen_alpha()

	def finish_sail_info(_s, tl):
		_s.sail_info['ld_start'] = tl[0] + _s.pic.shape[0] * _s.sail_info['scale_ss'][0]
		_s.sail_info['ld_end'] = tl[-1] + _s.pic.shape[0] * _s.sail_info['scale_ss'][0]


	def gen_tl(_s, ship):
		"""
		Since the offset is given for extent, but mov_black is for triangles,
		a tl is needed in tri space.
		DONT FORGET SCALE
		"""
		assert(len(ship.tris) >= _s.sail_info['frame_ss'][1])
		tl = np.zeros((_s.sail_info['frame_ss'][1] - _s.sail_info['frame_ss'][0], 2))

		offset = [_s.sail_info['offset'][0] * ship.scale_vector[0], _s.sail_info['offset'][1] * ship.scale_vector[1]]
		offset[0] += ship.extent[0, 0]
		offset[1] += ship.extent[0, 3]

		for i in range(len(tl)):  # OBS CURRENTLY IT IS ASSUMED ALL THE MOVEMENT IS FOR TOP TRI POINT
			mov_x = ship.tris[_s.sail_info['frame_ss'][0] + i][1, 0] - ship.tris[_s.sail_info['frame_ss'][0]][1, 0]
			mov_y = ship.tris[_s.sail_info['frame_ss'][0] + i][1, 1] - ship.tris[_s.sail_info['frame_ss'][0]][1, 1]
			tl[i, 0] = offset[0] + mov_x
			tl[i, 1] = offset[1] + mov_y

		return tl

	def gen_extent_black(_s, pic, ship, tl):
		"""
		This function is unique to sails i.e. kept inside this class since they must follow the roll movement.
		TODO
		"""

		width = pic.shape[1]
		height = pic.shape[0]

		scale_vector = np.linspace(_s.sail_info['scale_ss'][0], _s.sail_info['scale_ss'][1], len(tl))

		extent = np.zeros((len(tl), 4))
		extent_t = np.zeros((len(tl), 4))

		for i in range(len(tl)):

			width_m = width * scale_vector[i]
			height_m = height * scale_vector[i]

			extent[i, 0] = tl[i, 0]
			extent[i, 1] = tl[i, 0] + width
			extent[i, 2] = tl[i, 1] + height
			extent[i, 3] = tl[i, 1]

			extent_t[i] = [extent[i, 0] - extent[0, 0],  # left
			               extent[i, 1] - extent[0, 0],  # right
			               extent[i, 2] - extent[0, 3],  # down
			               extent[i, 3] - extent[0, 3]]  # up

		return extent, extent_t, scale_vector

	def ani_update_step(_s, ax, im_ax):

		if _s.drawn == 0:  # not drawn,
			return False
		elif _s.drawn == 1:  # start and continue
			_s.index_im_ax = len(im_ax)
			im_ax.append(ax.imshow(_s.pic, zorder=1, alpha=1))
			return True
		elif _s.drawn == 2:  # continue drawing
			return True
		elif _s.drawn == 3:  # end drawing
			# im_ax[ship_id].remove()  # might save CPU-time
			return False

	def DEPRgen_triangles(_s, pic, ship):
		"""
		DEPR: Just use extent_log
		Similar to default function but specialized to follow ship movements.
		ONLY POSITIVE VALUES HERE
		"""

		width = pic.shape[1]
		height = pic.shape[0]

		tris = []

		p0 = [0, height]
		p1 = [0 + (width / 2), 0]
		p2 = [0 + width, height]

		tris.append(np.float32([p0, p1, p2]))
		ext_base = np.array([0., width, height, 0])
		num_iters_temp = 30

		for i in range(1, num_iters_temp):

			# ext = extent_log[i]

			p0 = [0, height]
			p1 = [0 + (width / 2), 0]
			p2 = [0 + width, height]

			# mov_x = ext[0] - ext_base[0]
			#
			# mov_y = ext[2] - ext_base[2]
			#
			# width = ext[1] - ext[0]
			# height = ext[2] - ext[3]
			#
			# if np.min(extent_log) < 0:  # For neg values, larger mask has to be used.
			# 	p0 = [ext[0], ext[3] + (height)]
			# 	p1 = [ext[0] + (width / 2), ext[3]]
			# 	p2 = [ext[0] + (width), ext[3] + (height)]
			# else:
			# 	# p0 = [mov_x, mov_y + height]
			# 	# p1 = [mov_x + (width / 2), mov_y]
			# 	# p2 = [mov_x + width, mov_y + height]
			#
			# 	p0 = [mov_x, mov_y + pic.shape[0]]
			# 	p1 = [mov_x + (width / 2), mov_y + pic.shape[0] - height]
			# 	p2 = [mov_x + width, mov_y + pic.shape[0]]

			tri = np.float32([p0, p1, p2])
			tris.append(tri)

			# # Max's needed to be able to pad. OBS min here means left or up
			# if p2[0] > tri_max_x:
			# 	tri_max_x = p2[0]
			# if p2[1] > tri_max_y:
			# 	tri_max_y = p2[1]
			# if p0[0] < tri_min_x:
			# 	tri_min_x = p0[0]
			# if p1[1] < tri_min_y:
			# 	tri_min_y = p1[1]

		# padding_x = int(np.max(extent_log[:, 1]))  # covers whole movement in y
		# padding_y = int(np.max(extent_log[:, 2]))  # covers whole movement in y

		# if tri_min_y < 0:
		#     padding_y = int(padding_y - tri_min_y)  # larger pad needed
		# padding_y = 330

		# TEMPS ==================
		# HERE
		tri_max_x = 100  # HERE
		tri_max_y = 100
		tri_min_x = 0
		tri_min_y = 0
		padding_x = 200
		padding_y = 200

		return tris, tri_max_x, tri_max_y, tri_min_x, tri_min_y, padding_x, padding_y

	def gen_alpha(_s):
		return 0

	def change_brightness(value, ship_pic):
		"""
        OBS if brightness reaches threshold things WILL get messed up, e.g. brightness cannot be restored ok.
        :param value:
        :param ship_pic:
        :return:
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




