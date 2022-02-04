


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




