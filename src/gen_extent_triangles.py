import numpy as np
from copy import deepcopy

def gen_extent(mi, pic, padded=False):
    """
    returns linear motion extent through time
    extent_t is the same thing but shifted to origin at tl (since tri's have origin there).
    extent_t == UNSHIFTED FRAME
    """

    frame_num = mi['frame_ss'][1] - mi['frame_ss'][0]
    y_mid = mi['y_mid']

    extent = np.zeros((frame_num, 4))  # left, right, bottom, top borders
    extent_t = np.zeros((frame_num, 4))  # left, right, bottom, top borders

    # LEFT BOTTOM POSITION THROUGH TIME ================
    # pos_log = np.zeros((frame_num, 2))
    # if padded == False:
    lds_log = np.linspace(mi['ld_ss'][0], mi['ld_ss'][1], frame_num)  # left downs through time
    # else:
    #     lds_log = np.linspace([0, mi['ld_start'][1]], mi['ld_end'], frame_num)  # left downs through time

    # SCALING =============
    scale_vector = np.linspace(mi['scale_ss'][0], mi['scale_ss'][1], frame_num)
    width = pic.shape[1]
    height = pic.shape[0]

    for i in range(frame_num):  # could be inside above loop whatever

        width_m = width * scale_vector[i]
        height_m = height * scale_vector[i]

        extent[i] = [lds_log[i, 0],  # left
                     lds_log[i, 0] + width_m,  # right
                     lds_log[i, 1] + (1 - y_mid) * height_m,  # down
                     lds_log[i, 1] - y_mid * height_m]  # up

        extent_t[i] = [extent[i, 0] - extent[0, 0],  # left
                       extent[i, 1] - extent[0, 0],  # right
                       extent[i, 2] - extent[0, 3],  # down
                       extent[i, 3] - extent[0, 3]]  # up

        aa = 6

    assert(np.isclose(a=extent_t[0, 0], b=0.0))
    assert(np.isclose(a=extent_t[0, 3], b=0.0))

    # WHEN y_mid IS LESS THAN 1.0, THE WHOLE THING NEEDS TO BE SHIFTED

    # # UNSHIFT WHEN EXTENT FRAME IS LARGER THAN WHAT IS PERMITTED BY LDS_LOG
    diff_do = extent[0, 2] - lds_log[0, 1]  # if the first tri wants to go further down than what lds_log permits
    if diff_do > 0:  # This means y_mid is less than 1
        extent[:, 2] -= diff_do
        extent[:, 3] -= diff_do
        extent_t[:, 2] -= diff_do
        extent_t[:, 3] -= diff_do

    diff_le = extent[0, 0] - lds_log[0, 0]  # if the first tri wants to go further down than what lds_log permits
    if diff_le > 0:  # This means y_mid is less than 1
        extent[:, 2] -= diff_le
        extent[:, 3] -= diff_le
        extent_t[:, 2] -= diff_le
        extent_t[:, 3] -= diff_le

    return extent, extent_t, lds_log, scale_vector


def gen_triangles(extent_t, extent, mi, pic):
    """
    tri_max is needed for warpAffine. Since the warp is only on a subpic, tri_max gives the needed extent.
    padding returned, NOT shape after warpAffine obviously since this is not known at this stage
    tri_base not the same as tris (u f* idiot) A REFERENCE TO ORIG SCALE NEEDED.
    Mask is not part of warp!
    """

    # 1 BUILD TRIANGLES in extent_t domain ==============================
    # ext = extent_t[0]
    width = pic.shape[1]
    height = pic.shape[0]

    tris = []

    # CORRESPONDS TO EXTENT_T[0]
    p0 = [0, height]
    p1 = [0 + (width / 2), 0]
    p2 = [0 + width, height]

    tri_base = np.float32([p0, p1, p2])

    tri_ext = {'min_le': 9999, 'min_le_i': None,
               'max_le': -9999, 'max_le_i': None,
               'max_ri': -9999, 'max_ri_i': None,
               'min_do': 9999, 'min_do_i': None,
               'max_do': -9999, 'max_do_i': None
               }
    # tri_min_le, tri_min_le_i = 9999, None
    # tri_max_le, tri_max_le_i = -9999, None
    # tri_max_ri, tri_max_ri_i = -9999, None
    # tri_min_do, tri_min_do_i = 9999, None
    # tri_max_do, tri_max_do_i = -9999, None

    for i in range(0, extent_t.shape[0]):

        ext = extent_t[i]

        width = ext[1] - ext[0]
        height = ext[2] - ext[3]

        p0 = [ext[0], ext[3] + height]
        p1 = [ext[0] + (width / 2), ext[3]]
        p2 = [ext[0] + width, ext[3] + height]

        tri = np.float32([p0, p1, p2])
        tris.append(tri)

        if p0[0] < tri_ext['min_le']:
            tri_ext['min_le'] = p0[0]
            tri_ext['min_le_i'] = i
        if p0[0] > tri_ext['max_le']:
            tri_ext['max_le'] = p0[0]
            tri_ext['max_le_i'] = i
        if p2[0] > tri_ext['max_ri']:
            tri_ext['max_ri'] = p2[0]
            tri_ext['max_ri_i'] = i
        if p1[1] < tri_ext['min_do']:
            tri_ext['min_do'] = p1[1]
            tri_ext['min_do_i'] = i
        if p0[1] > tri_ext['max_do']:
            tri_ext['max_do'] = p0[1]
            tri_ext['max_do_i'] = i

    # SHIFT TRIANGLES
    tris_s = shift_triangles(deepcopy(tris), mi, extent_t, tri_ext)

    ## 3. BUILD MASK SHAPE: If ===================================
    if tri_ext['max_le'] <= max(mi['ld_ss'][0][0], mi['ld_ss'][1][0]):
        diff = max(mi['ld_ss'][0][0], mi['ld_ss'][1][0]) - tri_ext['max_le']
        mask_ri = int(tris_s[tri_ext['max_le_i']][2][0] + diff)  # the tri with the max le, then use third point and its x
    else:
        mask_ri = int(tri_ext['max_ri'])  # no right shifting

    if tri_ext['max_do'] <= max(mi['ld_ss'][0][1], mi['ld_ss'][1][1]):
        diff = max(mi['ld_ss'][0][1], mi['ld_ss'][1][1]) - tri_ext['max_do']
        mask_do = int(tri_ext['max_do'] + diff)
    else:
        mask_do = int(tri_ext['max_do'])


    # if tri_max_y < max(mi['ld_start'][1], mi['ld_end'][1]):
    #     # mask_y = int(tri_max_y + min(mi['ld_start'][1], mi['ld_end'][1]))
    #     mask_y = int(tri_max_y + min(mi['ld_start'][1], mi['ld_end'][1]))
    # else:
    #     mask_y = int(tri_max_y)  # no down shifting

    tris = tris_s  # undebug
    return tri_base, tris, tri_ext, mask_ri, mask_do


def shift_triangles(tris, mi, extent_t, tri_ext):
    """
    tris are deepcopied
    OBS shift_do only works currently because the scenario where things have to be shifted up, i.e. when things go
    out of bounds down, is not covered.
    :keywordd
    """

    # SHIFT TRIS DOWN (ONLY COVERS 1/2 SCENARIOS)
    shift_do = extent_t[0, 3] - extent_t[-1, 3]  # INCLUDES SCALING!
    if shift_do > 0:  #
        if tri_ext['max_do'] + shift_do > max(mi['ld_ss'][0][1], mi['ld_ss'][1][1]):
            shift_do = abs(mi['ld_ss'][1][1] - mi['ld_ss'][0][1])  # this means all tris need to be shifted down (base stays at tl 0, 0)
        for i in range(0, len(tris)):
            tri = tris[i]
            tri[0, 1] += shift_do
            tri[1, 1] += shift_do
            tri[2, 1] += shift_do

        tri_min_do = np.min([tri[1][1] for tri in tris])
        tri_max_do = np.max([tri[0][1] for tri in tris])

    # SHIFT TRIS HORIZONTAL


    if tri_ext['max_ri'] > mi['max_ri']:  # e.g. case 5: shift left by 100
        shift_hor = mi['max_ri'] - tri_ext['max_ri']
        # if tri_ext['max_ri'] > mi['max_ri']:  # THIS MEANS TRIS HAVE TO BE SHIFTED LEFT BY THE DIFF
        # shift_hor = mi['max_ri'] - tri_ext['max_ri']
        for i in range(0, len(tris)):
            tri = tris[i]
            tri[0, 0] += shift_hor
            tri[1, 0] += shift_hor
            tri[2, 0] += shift_hor



        # if tri_max_ri + shift_ri > max(mi['ld_start'][0], mi['ld_end'][0]):
        #     shift_ri = mi['ld_end'][0] - mi['ld_start'][0] - tri_max_ri


    # # PROB NEEDS FIXING (WORKS EXCEPT CASE 8)
    # if tri_ext['max_ri'] > max(mi['ld_start'][0], mi['ld_end'][0]):  # triangles want to go too far right
    #     shift_le = -abs(mi['ld_end'][0] - mi['ld_start'][0])
    #     for i in range(0, len(tris)):
    #         tri = tris[i]
    #         tri[0, 0] += shift_le
    #         tri[1, 0] += shift_le
    #         tri[2, 0] += shift_le

    return tris


