
import cv2
import numpy as np
import P

def warp_affine_and_color(ii, ax, im_ax, g_obj, ch, parent_obj=None):
	"""
	color has to be done here too to avoid multiple removing popping
	ax and im_ax are needed since the ax is removed from im_ax
	g_obj is the info container of the ax (class)
	g_obj is ship, sail or likewise
	Note expl color changes are applied for sails and smokes for the ship that fires.
	Waves have to be sorted out some other way.
	"""

	im_ax[g_obj.index_im_ax].remove()  # BOTH NECESSARY
	im_ax.pop(g_obj.index_im_ax)  # BOTH NECESSARY

	t0 = g_obj.tri_base
	t1 = g_obj.tris[g_obj.clock]
	pic_c = g_obj.pic.copy()  # pic with base scale always used.
	if P.A_STATIC_DARKENING:  # and parent_obj != None:
		static_darkening(pic_c, ii, g_obj)  # OBS ALSO overwrites the static image AND changes pic copy
	if P.A_FIRING_BRIGHTNESS and g_obj.__class__.__name__ != 'Ship':  # temp?
		fire_brightness(pic_c, ii, g_obj)

	if P.A_SAIL_HEIGHTS_TROUGHS_TRANSFORM and g_obj.__class__.__name__ == 'Sail':
		g_obj.apply_heights_troughs_transform(pic_c, ii)  # changes the pic copy

	M = cv2.getAffineTransform(t0, t1)
	dst = cv2.warpAffine(pic_c, M, (int(g_obj.tri_ext['max_ri']), int(g_obj.tri_ext['max_do'])))
	img = np.zeros((g_obj.mask_do, g_obj.mask_ri, 4))
	img[img.shape[0] - dst.shape[0]:, img.shape[1] - dst.shape[1]:, :] = dst
	im_ax.insert(g_obj.index_im_ax, ax.imshow(img, zorder=g_obj.gi['zorder'], alpha=1))


def decrement_all_index_im_ax(index_removed, ships, waves):
	"""
	Whenever an im_ax is popped from the list, all index_im_ax with higher index will be wrong and
	need to be decremented by 1.
	"""

	for ship in ships.values():
		if ship.index_im_ax != None:
			if ship.index_im_ax > index_removed:
				ship.index_im_ax -= 1
		for sail in ship.sails.values():
			if sail.index_im_ax != None:
				if sail.index_im_ax > index_removed:
					sail.index_im_ax -= 1
		for smoka in ship.smokas.values():
			if smoka.index_im_ax != None:
				if smoka.index_im_ax > index_removed:
					smoka.index_im_ax -= 1
		for smokr in ship.smokrs.values():
			if smokr.index_im_ax != None:
				if smokr.index_im_ax > index_removed:
					smokr.index_im_ax -= 1
		for expl in ship.expls.values():
			if expl.index_im_ax != None:
				if expl.index_im_ax > index_removed:
					expl.index_im_ax -= 1

	for wave in waves.values():
		if wave.index_im_ax != None:
			if wave.index_im_ax > index_removed:
				wave.index_im_ax -= 1


def static_darkening(pic, ii, g_obj):
	"""
	R   G   B   !   !   !
	https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv

	Might get super expensive to do this for ships at each frame. So instead set
	expl_at_coords: coordinates where there are active expls this frame (the expl "event" continues more frames
	than the expl is shown).

	Not applied for expls

	"""
	if g_obj.__class__.__name__ != 'Sail':  # TEMP
		return pic

	ship_ab_at_clock = g_obj.ship.gi['alpha_and_bright'][g_obj.ship.ab_clock]
	if ii == ship_ab_at_clock[0]:

		# brightness TODO: will need lots of tuning
		g_obj.pic[:, :, 0] = g_obj.pic[:, :, 0] * ship_ab_at_clock[2]
		g_obj.pic[:, :, 1] = g_obj.pic[:, :, 1] * ship_ab_at_clock[2]
		g_obj.pic[:, :, 2] = g_obj.pic[:, :, 2] * ship_ab_at_clock[2]

	# HSV (perhaps not needed)
	# img = ship_pic
	# hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
	# h, s, v = cv2.split(hsv)
	# v += value
	# final_hsv = cv2.merge((h, s, v))
	# img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
	# img[:, :, 0:3] = img2
	#
	# # think this is just the operation to sort out alpha
	# idx0 = np.argwhere(img[:, :, 0:3] < 0.0)
	# idx1 = np.argwhere(img[:, :, 0:3] > 1.0)
	#
	# for row, col, ch in idx0:
	# 	img[row, col, ch] = 0.0
	#
	# for row, col, ch in idx1:
	# 	img[row, col, ch] = 1.0

	return pic


def fire_brightness(pic, ii, g_obj):

	if g_obj.__class__.__name__ not in ['Sail', 'Wave']:  # TEMP
		return pic

	# FIRING UPDATES = ===================
	if ii in g_obj.ship.gi['firing_frames']:
		ex = 5.84
		# if iii in firing_frames:
		# 	ex = 0.84  # decrease in green and blue
		# pic = _s.pic.copy()  # REQUIRED
		pic[:, :, 0] = pic[:, :, 0] * ex  # more y=more red, less=more green
		pic[:, :, 0][pic[:, :, 0] > 1.0] = 1.0
		pic[:, :, 1] = pic[:, :, 1] * ex  # more y=more green, less=more red
		pic[:, :, 1][pic[:, :, 1] > 1.0] = 1.0
		pic[:, :, 2] = pic[:, :, 2] * ex  # Needed to complement red and green
		pic[:, :, 2][pic[:, :, 2] > 1.0] = 1.0


def find_all_ax_at_coord():  # probably wont be used

	return ""

