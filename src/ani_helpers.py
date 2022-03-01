


import cv2
import numpy as np
import P

def warp_affine(i, ax, im_ax, g_obj, ch, parent_obj=None):
	"""
	g_obj is ship, sail or likewise

	"""

	im_ax[g_obj.index_im_ax].remove()  # BOTH NECESSARY
	im_ax.pop(g_obj.index_im_ax)  # BOTH NECESSARY

	t0 = g_obj.tri_base
	t1 = g_obj.tris[g_obj.clock]
	img = g_obj.pic  # pic with base scale always used.
	if P.A_COLORS and g_obj.__class__.__name__ == 'Sail':
		img = g_obj.apply_transform(ch['ships'][parent_obj.gi['id']]['firing_frames'], i)

	M = cv2.getAffineTransform(t0, t1)
	dst = cv2.warpAffine(img, M, (int(g_obj.tri_ext['max_ri']), int(g_obj.tri_ext['max_do'])))
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

	for wave in waves.values():
		if wave.index_im_ax != None:
			if wave.index_im_ax > index_removed:
				wave.index_im_ax -= 1

