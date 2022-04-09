
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
        _s.frame_ss = ship_info['move']['frame_ss']
        _s.frames_tot = _s.gi['move']['frame_ss'][1] - _s.gi['move']['frame_ss'][0]
        _s.extent, _s.extent_t, lds_log, _s.scale_vector = gen_extent(ship_info['move'], pic)  # left_down_log
        _s.tri_base, _s.tris, _s.tri_ext, _s.mask_ri, _s.mask_do = \
            gen_triangles(_s.extent_t, _s.extent, ship_info['move'], pic)
        assert(len(_s.extent) == len(_s.tris))
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

        CYCLES = _s.gi['move']['roll_cycles']
        F_x = 5.6
        F_y = 0.24

        if P.MAP_SIZE == 'small':
            F_x = 2.3  # 5.6
            F_y = 0.1

        cycles_currently = _s.frames_tot / (2 * np.pi)
        d = cycles_currently / CYCLES
        frames_p_cycle = _s.frames_tot // CYCLES
        random_shift = random.uniform(-2.0, 2.0) * frames_p_cycle  # probably in radians
        for i in range(_s.frames_tot):
            mov_black[i, 0] = F_x * np.sin(i / d + random_shift)
            mov_black[i, 1] = F_y * np.sin(i / d + random_shift)

            _s.tris[i][1, 0] += mov_black[i, 0]

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
        random.shuffle(li_ids)
        for key in li_ids:
            obj = _di[key]
            if obj.drawn == 0:  # object is not drawn
                return obj

        return None  # no object found

    # def add_sail(_s, sail):
    #     _s.sails[sail.id] = sail
        
    # def gen_col_transforms(_s):
    #     """
    #     WILL BE MOVED Only gonna be for sail (but easier to work with base layer; sail is anchored)
    #     Think about whether this can be generalized
    #     cycling and shifting shear
    #     For cycling noise is required since it's too obvious otherwise
    #     """
    #     shear_cycles = 4
    #     shear_min = -0.1  # these guys seem to affect the direction of the shear
    #     shear_max = 0.2
    #     shear_range = (shear_max - shear_min) / 2  # div by 2 since it's applied to both pos and neg numbers
    #     shear_distribution = [0.99, 0.01]  # shifting and cycling
    #
    #     # SHIFTING
    #     z_shear_shifting = np.linspace(shear_min, shear_max, _s.frames_tot)
    #
    #     # CYCLING
    #     z_shear_cycling_x = np.linspace(0, shear_cycles*2*np.pi, _s.frames_tot)
    #     z_shear_cycling_rand_x = np.zeros((_s.frames_tot))
    #
    #     cur_pos = z_shear_cycling_x[0]
    #     for i in range(_s.frames_tot):  # OBS range of values odn\t matter here since sin will be taken
    #         z_shear_cycling_rand_x[i] = cur_pos
    #
    #         # Linear component and random component (otherwise the random component blows up)
    #         cur_pos = 0.8 * z_shear_cycling_x[i] + 0.2 * (cur_pos + random.random() * random.choice([-1, 1]))
    #
    #     # aa = np.sin(z_shear_cycling_rand_x * 6)/6
    #     z_shear_cycling = (0.6 * np.sin(z_shear_cycling_x) + 0.4 * np.sin(z_shear_cycling_rand_x * 2)) * shear_range + shear_range + shear_min
    #
    #     assert(max(z_shear_shifting) <= shear_max)
    #     assert(min(z_shear_shifting) >= shear_min)
    #     assert (max(z_shear_cycling) <= shear_max)
    #     assert (min(z_shear_cycling) >= shear_min)
    #
    #     z_shear = z_shear_shifting * shear_distribution[0] + z_shear_cycling * shear_distribution[1]
    #
    #     return z_shear

    # def apply_col_transform(_s, firing_frames, iii):
    #     """
    #     This is run on the readonly pic of ship at the internal clock
    #     col_diff: 0-0.5  Heights and troughs in the pic. Can't be more than 0.5 since  0.5 neg + 0.5 pos = 1.0 i.e. max
    #     """
    #
    #     col_diff = 0.1  # 0.1
    #
    #     # THIS SHOULD BE PRECOMPUTED!!!
    #     num_cycles_x = 5
    #     num_cycles_y = 1
    #     x_ver = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
    #     x_hor = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
    #     for i in range(_s.pic.shape[0]):
    #         x_ver[i, :] = np.linspace(0, int(num_cycles_x * (2 * np.pi)), num=_s.pic.shape[1])
    #         x_hor[i, :] = np.linspace(0, int(num_cycles_y * (2 * np.pi)), num=_s.pic.shape[1])
    #         num_cycles_x += 0.01  # too much=slows down movement
    #         num_cycles_y += 0.1
    #
    #     # THIS SHOULD NOT BE PRECOMPUTED (CAN'T BECAUSE CLOCK NEEDED HERE)
    #     y_ver = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
    #     y_hor = np.zeros((_s.pic.shape[0], _s.pic.shape[1]))
    #     for i in range(_s.pic.shape[0]):
    #         # col diff first squeezes the curve down to desired range, then shifts it up to positive
    #         y_ver[i, :] = (np.sin(x_ver[i, :] + i * _s.z_shear[_s.clock])) * col_diff + (1 - col_diff)  # / 4 means y range is -.25 to .25
    #         y_hor[i, :] = (np.sin(x_hor[i, :] + i * _s.z_shear[_s.clock])) * col_diff + (1 - col_diff)
    #
    #     y = y_ver * y_hor
    #     ex = 1
    #     if iii in firing_frames:
    #         ex = 0.8
    #     pic = _s.pic.copy()  # REQUIRED
    #     pic[:, :, 0] = pic[:, :, 0] * y  # more y=more red, less=more green
    #     pic[:, :, 1] = pic[:, :, 1] * ex * y  # more y=more green, less=more red
    #     pic[:, :, 2] = pic[:, :, 2] * ex * y  # Needed to complement red and green
    #     # pic[:, :, 3] = pic[:, :, 3] * y  # will prob not be y
    #
    #     return pic

    # def ani_update_step(_s, ax, im_ax):
    #
    #     if _s.drawn == 0:  # not drawn,
    #         return False
    #     elif _s.drawn == 1: # start and continue
    #         _s.index_im_ax = len(im_ax)
    #         # im_ax[_s.gi['id']] = ax.imshow(_s.pic, zorder=1, alpha=1)
    #         im_ax.append(ax.imshow(_s.pic, zorder=1, alpha=1))
    #         return True
    #     elif _s.drawn == 2:  # continue drawing
    #         return True
    #     elif _s.drawn == 3:  # end drawing
    #         im_ax[_s.index_im_ax].remove()  # might save CPU-time
    #         im_ax.pop(_s.index_im_ax)
    #         return False


