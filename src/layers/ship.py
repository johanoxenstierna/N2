
from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer
from src import PARAMS as P
import random


class Ship(AbstractLayer):

    def __init__(s, ship_info, pic):
        super().__init__()
        s.ship_info = ship_info
        s.frame_ss = ship_info['move']['frame_ss']
        s.extent, s.extent_t, lds_log, s.scale_vector = gen_extent(ship_info['move'], pic, padded=False)  # left_down_log
        s.tri_base, s.tris, s.tri_max_x, s.tri_max_y, s.tri_min_x, s.tri_min_y, s.mask_x, s.mask_y = \
            gen_triangles(s.extent_t, s.extent, ship_info['move'], pic)
        assert(len(s.extent) == len(s.tris))
        # s.mov_black()

        s.sails = {}

    def mov_black(s):
        """
        Extra roll movement. Unique to ship
        """
        total_frames = s.ship_info['move']['frame_ss'][1] - s.ship_info['move']['frame_ss'][0]
        mov_black = np.zeros(shape=(total_frames, 2))

        CYCLES = s.ship_info['move']['roll_cycles']
        F_x = 5.6
        F_y = 0.24

        if P.MAP_SIZE == 'small':
            F_x = 10.3  # vid25: 2.0
            F_y = 0.1

        cycles_currently = total_frames / (2 * np.pi)
        d = cycles_currently / CYCLES
        frames_p_cycle = total_frames // CYCLES
        random_shift = random.uniform(-2.0, 2.0) * frames_p_cycle  # probably in radians
        for i in range(total_frames):
            mov_black[i, 0] = F_x * np.sin(i / d + random_shift)
            mov_black[i, 1] = F_y * np.sin(i / d + random_shift)

            s.tris[i][1, 0] += mov_black[i, 0]

        aa = 5

    def add_sail(s, sail):
        s.sails[sail.id] = sail


