
from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer
import P as P
from src.gen_colors import gen_colors
# import copy
import numpy as np

import random


class Ship(AbstractLayer):

    def __init__(_s, ship_info, pic):
        super().__init__()
        _s.id = ship_info['id']
        _s.gi = ship_info
        _s.pic = pic  # NOT SCALED
        _s.fill_info()
        _s.frame_ss = [0, P.FRAMES_STOP - 100]
        _s.gi['move']['frame_ss'] = _s.frame_ss  # NEW
        _s.frames_tot = _s.frame_ss[1] - _s.frame_ss[0]
        zigzag = ()
        if P.PR_ZIGZAG:
            zigzag = gen_zig_zag(_s.frames_tot, cycles=10, max_delta_width=0.06)
        _s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(ship_info['move'], pic, zigzag=zigzag)  # left_down_log
        _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
            gen_triangles(_s.extent_t, _s.extent, ship_info['move'], pic)

        assert(len(_s.extent) == len(_s.tris))

        # check tris
        assert(_s.extent_t[0, 0] < 0.0001)
        assert(_s.extent_t[0, 1] - _s.tri_base[2, 0] < 0.0001)

        # if ship_info['id'] == '7':
        #     _s.pic = gen_colors(pic)  # TEMP (not gonna be used by ship).
        #     _s.z_shear = _s.gen_col_transforms()

        if P.PR_MOVE_BLACK == 1:
            _s.mov_black()

        _s.sails = {}
        _s.smokas = {}
        _s.smokrs = {}
        _s.expls = {}
        _s.spls = {}

        _s.zorder = _s.gi['zorder']
        _s.smoka_latest_drawn_id = "99_99_99_99"

    def fill_info(_s):
        """
        Some values in ship_info are not gonna be there,
        e.g. sail scale_vectors.
        Have to be computed
        """
        # Compute the maximum extent right of move_info (needed to get transforms right)
        # a = _s.gi['move']['ld_ss'][0][0]
        # b = _s.gi['move']['ld_ss'][1][0]
        # aa = _s.gi['move']['ld_ss']

        # EITHER FIRST OR LAST INDEX WILL CONTAIN MAX_X (ld_ss starts with ss, then ld)
        index_with_most_ld_x = np.argmax([_s.gi['move']['ld_ss'][0][0], _s.gi['move']['ld_ss'][1][0]])

        _s.gi['move']['max_ri'] = _s.gi['move']['ld_ss'][index_with_most_ld_x][0] + _s.pic.shape[1] * _s.gi['move']['scale_ss'][index_with_most_ld_x]
        # _s.tc[str(i)]['ld_ss'][index_with_most_ld_x][0] + pic.shape[1] * _s.tc[str(i)]['scale_ss'][index_with_most_ld_x]

        gg=5

    def mov_black(_s):
        """
        Extra roll movement. Unique to ship
        """
        
        mov_black = np.zeros(shape=(_s.frames_tot, 2))

        CYCLES = _s.gi['move']['black']['cycles']
        F_x = _s.gi['move']['black']['fxy'][0]
        F_y = _s.gi['move']['black']['fxy'][1]

        # if P.MAP_SIZE == 'small':
        #     F_x = _s.gi['move']['black']['fxy'][0]
        #     F_y = _s.gi['move']['black']['fxy'][1]

        cycles_currently = _s.frames_tot / (2 * np.pi)
        d = cycles_currently / CYCLES
        frames_p_cycle = _s.frames_tot // CYCLES
        random_shift = random.uniform(-2.0, 2.0) * frames_p_cycle  # probably in radians
        for i in range(_s.frames_tot):
            mov_black[i, 0] = F_x * np.sin(i / d + random_shift)
            mov_black[i, 1] = F_y * np.sin(i / d + random_shift)

            _s.tris[i][1, 0] += mov_black[i, 0]
            # TODO y not asdjusted currently

    def find_free_obj(_s, type):

        _di = None
        if type == 'expl':
            _di = _s.expls
        elif type == 'smokr':
            _di = _s.smokrs
        elif type == 'smoka':
            _di = _s.smokas
        elif type == 'spl':
            _di = _s.spls
        li_ids = list(_di.keys())

        random.shuffle(li_ids)  # TODO: REPLACE WITH INDEX FOR SMOKA
        # flag_found = False # only used by smoka
        for key in li_ids:
            obj = _di[key]
            if obj.drawn == 0:  # object is not drawn
                if type == 'smoka':
                    id_split_smoka = obj.id.split('_')
                    id_split_ship_latest_smoka = _s.smoka_latest_drawn_id.split('_')
                    if id_split_smoka[2] == id_split_ship_latest_smoka[2]:
                        continue
                return obj

        # SPECIAL SMOKA CASE. MAY BECOME DEPRECATED IF ALL SHIPS GET SEVERAL SMOKAS
        if type == 'smoka':  # if return above has not happened it means that none has been found (e.g. if only 1 type available)
            for key in li_ids:
                obj = _di[key]
                if obj.drawn == 0:  # object is not drawn
                    return obj

        return None  # no object found

