
import cv2
import numpy as np
import P

def warp_affine_and_color(ii, ax, im_ax, g_obj, ch, parent_obj=None):
	"""
	color has to be done here too to avoid multiple removing popping
	ax and im_ax are needed since the ax is removed from im_ax
	g_obj is the info container of the ax (class)
	g_obj is ship, sail or likewise

	"""

	im_ax[g_obj.index_im_ax].remove()  # BOTH NECESSARY
	im_ax.pop(g_obj.index_im_ax)  # BOTH NECESSARY

	t0 = g_obj.tri_base
	t1 = g_obj.tris[g_obj.clock]
	pic = g_obj.pic.copy()  # pic with base scale always used.
	if P.A_HSV_TRANSFORM:  # and parent_obj != None:
		pic = change_brightness_contrast(pic, ii, g_obj)

	if P.A_SAIL_HEIGHTS_TROUGHS_TRANSFORM and g_obj.__class__.__name__ == 'Sail':
		# pic = g_obj.apply_heights_troughs_transform(pic, ch['ships'][parent_obj.gi['id']]['firing_frames'], i)
		pic = g_obj.apply_heights_troughs_transform(pic, ii)
		# pic = g_obj.apply_heights_troughs_transform(pic, i)


	M = cv2.getAffineTransform(t0, t1)
	dst = cv2.warpAffine(pic, M, (int(g_obj.tri_ext['max_ri']), int(g_obj.tri_ext['max_do'])))
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


def change_brightness_contrast(pic, ii, g_obj):
	"""
	https://stackoverflow.com/questions/39308030/how-do-i-increase-the-contrast-of-an-image-in-python-opencv

	Might get super expensive to do this for ships at each frame
	expl_at_coords: coordinates where there are active expls this frame (the expl "event" continues more frames
	than the expl is shown).

	OBS if brightness reaches threshold things WILL get messed up, e.g. brightness cannot be restored ok.
		:param value:
		:param ship_pic:
		:return:

	"""
	if g_obj.__class__.__name__ != 'Sail':  # TEMP
		return pic

	if ii in g_obj.ship.gi['firing_frames']:
		ex = 0.95
		# if iii in firing_frames:
		# 	ex = 0.84  # decrease in green and blue
		# pic = _s.pic.copy()  # REQUIRED
		pic[:, :, 0] = pic[:, :, 0]   # more y=more red, less=more green
		pic[:, :, 1] = pic[:, :, 1] * ex   # more y=more green, less=more red
		pic[:, :, 2] = pic[:, :, 2] * ex  # Needed to complement red and green



	aa = 5

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



def find_all_ax_at_coord():  # probably wont be used

	return ""

