
from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer
from src import PARAMS as P
from src.gen_colors import gen_colors
# import copy
import numpy as np

import random


class Ship(AbstractLayer):

    def __init__(s, ship_info, pic):
        super().__init__()
        s.ship_info = ship_info
        s.pic = pic
        s.frame_ss = ship_info['move']['frame_ss']
        s.frames_tot = s.ship_info['move']['frame_ss'][1] - s.ship_info['move']['frame_ss'][0]
        s.extent, s.extent_t, lds_log, s.scale_vector = gen_extent(ship_info['move'], pic, padded=False)  # left_down_log
        s.tri_base, s.tris, s.tri_max_x, s.tri_max_y, s.tri_min_x, s.tri_min_y, s.mask_x, s.mask_y = \
            gen_triangles(s.extent_t, s.extent, ship_info['move'], pic)
        assert(len(s.extent) == len(s.tris))
        if ship_info['id'] == '7':
            s.pic = gen_colors(pic)  # TEMP (not gonna be used by ship).
            s.z_shear = s.gen_col_transforms()
        # s.mov_black()

        s.sails = {}

    def mov_black(s):
        """
        Extra roll movement. Unique to ship
        """
        
        mov_black = np.zeros(shape=(s.frames_tot, 2))

        CYCLES = s.ship_info['move']['roll_cycles']
        F_x = 5.6
        F_y = 0.24

        if P.MAP_SIZE == 'small':
            F_x = 10.3  # vid25: 2.0
            F_y = 0.1

        cycles_currently = s.frames_tot / (2 * np.pi)
        d = cycles_currently / CYCLES
        frames_p_cycle = s.frames_tot // CYCLES
        random_shift = random.uniform(-2.0, 2.0) * frames_p_cycle  # probably in radians
        for i in range(s.frames_tot):
            mov_black[i, 0] = F_x * np.sin(i / d + random_shift)
            mov_black[i, 1] = F_y * np.sin(i / d + random_shift)

            s.tris[i][1, 0] += mov_black[i, 0]

    def add_sail(s, sail):
        s.sails[sail.id] = sail
        
    def gen_col_transforms(s):
        """
        WILL BE MOVED Only gonna be for sail (but easier to work with base layer; sail is anchored)
        Think about whether this can be generalized
        cycling and shifting shear
        For cycling noise is required since it's too obvious otherwise
        """
        shear_cycles = 4
        shear_min = -0.1  # these guys seem to affect the direction of the shear
        shear_max = 0.2
        shear_range = (shear_max - shear_min) / 2  # div by 2 since it's applied to both pos and neg numbers
        shear_distribution = [0.99, 0.01]  # shifting and cycling

        # SHIFTING
        z_shear_shifting = np.linspace(shear_min, shear_max, s.frames_tot)

        # CYCLING
        z_shear_cycling_x = np.linspace(0, shear_cycles*2*np.pi, s.frames_tot)
        z_shear_cycling_rand_x = np.zeros((s.frames_tot))

        cur_pos = z_shear_cycling_x[0]
        for i in range(s.frames_tot):  # OBS range of values odn\t matter here since sin will be taken
            z_shear_cycling_rand_x[i] = cur_pos

            # Linear component and random component (otherwise the random component blows up)
            cur_pos = 0.8 * z_shear_cycling_x[i] + 0.2 * (cur_pos + random.random() * random.choice([-1, 1]))

        # aa = np.sin(z_shear_cycling_rand_x * 6)/6
        z_shear_cycling = (0.6 * np.sin(z_shear_cycling_x) + 0.4 * np.sin(z_shear_cycling_rand_x * 2)) * shear_range + shear_range + shear_min

        assert(max(z_shear_shifting) <= shear_max)
        assert(min(z_shear_shifting) >= shear_min)
        assert (max(z_shear_cycling) <= shear_max)
        assert (min(z_shear_cycling) >= shear_min)

        z_shear = z_shear_shifting * shear_distribution[0] + z_shear_cycling * shear_distribution[1]

        return z_shear

    def apply_col_transform(s, expl_coords):
        """
        This is run on the readonly pic of ship at the internal clock
        col_diff: 0-1 Heights and troughs in the pic
        """

        col_diff = 0.05  # 0.1

        # THIS SHOULD BE PRECOMPUTED!!!
        num_cycles_x = 5
        num_cycles_y = 1
        x_ver = np.zeros((s.pic.shape[0], s.pic.shape[1]))
        x_hor = np.zeros((s.pic.shape[0], s.pic.shape[1]))
        for i in range(s.pic.shape[0]):
            x_ver[i, :] = np.linspace(0, int(num_cycles_x * (2 * np.pi)), num=s.pic.shape[1])
            x_hor[i, :] = np.linspace(0, int(num_cycles_y * (2 * np.pi)), num=s.pic.shape[1])
            num_cycles_x += 0.01  # too much=slows down movement
            num_cycles_y += 0.1

        # THIS SHOULD NOT BE PRECOMPUTED (CAN'T BECAUSE CLOCK NEEDED HERE)
        y_ver = np.zeros((s.pic.shape[0], s.pic.shape[1]))
        y_hor = np.zeros((s.pic.shape[0], s.pic.shape[1]))
        for i in range(s.pic.shape[0]):
            # col diff first squeezes the curve down to desired range, then shifts it up to positive
            y_ver[i, :] = (np.sin(x_ver[i, :] + i * s.z_shear[s.clock])) * col_diff + (1 - col_diff)  # / 4 means y range is -.25 to .25
            y_hor[i, :] = (np.sin(x_hor[i, :] + i * s.z_shear[s.clock])) * col_diff + (1 - col_diff)

        y = y_ver * y_hor
        pic = s.pic.copy()  # REQUIRED
        pic[:, :, 0] = pic[:, :, 0] * y  # more y=more red, less=more green
        pic[:, :, 1] = pic[:, :, 1] * y  # more y=more green, less=more red
        pic[:, :, 2] = pic[:, :, 2] * y  # DOESN'T DO ANYTHING???
        pic[:, :, 3] = pic[:, :, 3] * y  # will prob not be y

        return pic


