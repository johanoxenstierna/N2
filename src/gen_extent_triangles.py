import numpy as np


def gen_extent(move_info, pic, padded=False):
    """returns extent through time"""

    frame_num = move_info['frame_end'] - move_info['frame_start']

    extent = np.zeros((frame_num, 4))  # left, right, bottom, top borders

    # LEFT BOTTOM POSITION THROUGH TIME ================
    # pos_log = np.zeros((frame_num, 2))
    if padded == False:
        lds_log = np.linspace(move_info['ld_start'], move_info['ld_end'], frame_num)  # left downs through time
    else:
        lds_log = np.linspace([0, move_info['ld_start'][1]], move_info['ld_end'], frame_num)  # left downs through time

    # SCALING =============
    scale_vector = np.linspace(move_info['scale_start'], move_info['scale_end'], frame_num)

    extent[:, 0] = lds_log[:, 0]  # left border
    extent[:, 2] = lds_log[:, 1]  # bottom border

    width = pic.shape[1]
    height = pic.shape[0]

    for i in range(frame_num):  # could be inside above loop whatever

        width_m = width * scale_vector[i]
        height_m = height * scale_vector[i]

        extent[i, 1] = lds_log[i, 0] + width_m  # right border
        extent[i, 3] = lds_log[i, 1] - height_m  # top border

    return extent, lds_log, scale_vector


def gen_triangles(extent_log, lds_log, pic, scale_vector):
    """
    No shifting done here. Triangle always starts at top left
    tri_max is needed for warpAffine. Since the warp is only on a subpic, tri_max gives the needed extent.
    padding returned, NOT shape after warpAffine obviously since this is not known at this stage
    """

    width = pic.shape[1]
    height = pic.shape[0]

    tris = []  # not using np since it's nested
    padding = np.zeros((extent_log.shape[0], 2))

    p0 = [0, height]
    p1 = [0 + (width / 2), 0]
    p2 = [0 + width, height]

    tris.append(np.float32([p0, p1, p2]))
    ext_base = extent_log[0]

    tri_max_x = -9999
    tri_max_y = -9999
    tri_min_x = 9999
    tri_min_y = 9999

    for i in range(1, extent_log.shape[0]):

        ext = extent_log[i]

        if ext_base[0] < 0:  # if it goes out to left, don't do fancy padding
            mov_x = ext[0]
        else:
            mov_x = ext[0] - ext_base[0]

        mov_y = ext[2] - ext_base[2]

        width = ext[1] - ext[0]
        height = ext[2] - ext[3]

        if np.min(extent_log) < 0:
            p0 = [ext[0], ext[3] + (height)]
            p1 = [ext[0] + (width / 2), ext[3]]
            p2 = [ext[0] + (width), ext[3] + (height)]
        else:
            # p0 = [mov_x, mov_y + height]
            # p1 = [mov_x + (width / 2), mov_y]
            # p2 = [mov_x + width, mov_y + height]

            p0 = [mov_x, mov_y + pic.shape[0]]
            p1 = [mov_x + (width / 2), mov_y + pic.shape[0] - height]
            p2 = [mov_x + width, mov_y + pic.shape[0]]

        tri = np.float32([p0, p1, p2])
        tris.append(tri)

        # Max's needed to be able to pad. OBS min here means left or up
        if p2[0] > tri_max_x:
            tri_max_x = p2[0]
        if p2[1] > tri_max_y:
            tri_max_y = p2[1]
        if p0[0] < tri_min_x:
            tri_min_x = p0[0]
        if p1[1] < tri_min_y:
            tri_min_y = p1[1]

    padding_x = int(np.max(extent_log[:, 1]))  # covers whole movement in y
    padding_y = int(np.max(extent_log[:, 2]))  # covers whole movement in y

    # if tri_min_y < 0:
    #     padding_y = int(padding_y - tri_min_y)  # larger pad needed
        # padding_y = 330

    return tris, tri_max_x, tri_max_y, tri_min_x, tri_min_y, padding_x, padding_y


