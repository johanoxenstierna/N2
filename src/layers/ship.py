
from src.gen_extent_triangles import *
from src.layers.abstract import AbstractLayer


class Ship(AbstractLayer):

    def __init__(s, ship_info, pic):
        super().__init__()
        s.ship_info = ship_info
        s.extent, lds_log, scale_vector = gen_extent(ship_info['move'], pic, padded=False)  # left_down_log
        s.tris, s.tri_max_x, s.tri_max_y, s.tri_min_x, s.tri_min_y, s.padding_x, s.padding_y = \
            gen_triangles(s.extent, lds_log, pic, scale_vector)
        s.frame_start = ship_info['move']['frame_start']
        s.frame_end = ship_info['move']['frame_end']
