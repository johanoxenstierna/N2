
import numpy as np
import random
from copy import deepcopy
from src.gen_extent_triangles import *

import P


class AbstractLayer:
    """
    This class is supposed to be ridicilously simple
    Obs doesn't have access to the ax itself, only the info about it.
    Obs if an object is to change its movement it needs a new layer instance.
    """

    def __init__(_s):
        _s.drawn = 0  # 0: not drawn, 1: start drawing, 2. continue drawing, 3. end drawing, 4: dynamic flag usage
        _s.clock = 0
        _s.ab_clock = 0  # alpha_brightness clock for static changes (i.e. non-expl)
        _s.frames_num = None  # number of frames to animate for
        _s.frame_ss = None
        # _s.frame_ss_start_offset = None
        _s.index_im_ax = None
        _s.pic = None
        _s.extent = "asdf"

    def set_clock(_s, i):
        """
        The layer classes don't have access to the ax, so
        this essentially tells the ax what to do.
        """

        if i == _s.frame_ss[0]:
            _s.drawn = 1
        elif i > _s.frame_ss[0] and i < _s.frame_ss[1]:
            _s.drawn = 2  # needed bcs ani_update_step will create a new im_ax otherwise
            _s.clock += 1
        elif i == _s.frame_ss[1]:
            _s.drawn = 3
            _s.clock = 0  # ONLY PLACE WHERE RESET
        else:  # NEEDED BCS OTHERWISE _s.drawn just stays on 3
            _s.drawn = 0

    def ani_update_step(_s, ax, im_ax):
        """
        Based on the drawn condition, draw, remove
        If it's drawn, return True (used in animation loop)
        OBS major bug discovered: im_ax.pop(index_im_ax) OBVIOUSLY results in that all index_im_ax after popped get
        screwed.
        Returns the following index:
        0: don't draw
        1: draw (will result in warp_affine)
        2: ax has just been removed, so decrement all index_im_ax
        """

        if _s.drawn == 0:  # not drawn,
            return 0, None
        elif _s.drawn == 1: # start and continue
            _s.index_im_ax = len(im_ax)
            # im_ax[_s.ship_info['id']] = ax.imshow(_s.pic, zorder=1, alpha=1)
            im_ax.append(ax.imshow(_s.pic, zorder=1, alpha=1))
            return 1, None
        elif _s.drawn == 2:  # continue drawing
            return 1, None
        elif _s.drawn == 3:  # end drawing
            try:
                im_ax[_s.index_im_ax].remove()  # might save CPU-time
                im_ax.pop(_s.index_im_ax)  # OBS OBS!!! MAKES im_ax shorter hence all items after index_im_ax now WRONG
            except:
                raise Exception("ani_update_step CANT REMOVE AX")
            index_removed = _s.index_im_ax
            _s.index_im_ax = None  # THIS IS NEEDED BUT NOT SURE WHY
            return 2, index_removed


class AbstractSSS:
    """
    class for all objects that have ship as parent and need to repeat using the queing system
    (except for waves currently).
    Hence functions in this class will be called several times in the animation loop.
    This class takes over all id etc from the child class since theyre needed to sort out gi
    """

    def __init__(_s, ship, id, pic):
        # _s.occupied = False
        _s.ship = ship
        _s.frame_ss = [None, None]
        _s.id = id
        _s.pic = pic


    def init_dyn_obj(_s, ii, NUM_FRAMES):
        _s.frame_ss[0] = ii
        _s.frame_ss[1] = ii + NUM_FRAMES
        assert(_s.frame_ss[1] < P.FRAMES_STOP)
        ld_ss = _s.get_ld_ss()  # not used by expl

        _s.scale_ss = [0.1, 1.0]

        _s.gi['frame_ss'] = _s.frame_ss
        _s.gi['ld_ss'] = ld_ss
        _s.gi['scale_ss'] = _s.scale_ss

    # def gen_dyn_extent(_s):
    #
    #

    def get_ld_ss(_s):
        """TODO Needs generalization. Probably needs splitting"""
        extent_ship_at_start = _s.ship.extent[_s.frame_ss[0]]
        extent_ship_at_stop = _s.ship.extent[_s.frame_ss[1]]

        # FIRST SET IT TO BE SAME LD AS SHIP AT FRAME
        ld_ss = [[extent_ship_at_start[0], extent_ship_at_start[2]],
                 [extent_ship_at_stop[0], extent_ship_at_stop[2]]]

        # ADD SMOKA OFFSET
        ld_ss[0][0] += _s.gi['offset'][0]  # this is ld!
        ld_ss[0][1] += _s.gi['offset'][1]
        # ld_ss[1][0] += _s.ship.gi['smoka_offset'][0]
        # ld_ss[1][1] += _s.ship.gi['smoka_offset'][1]

        # ADD RAND
        ld_ss[0][0] += random.randint(-30, 30)  # left start
        ld_ss[0][1] += random.randint(-10, 5)  # down  start
        ld_ss[1][0] = ld_ss[0][0] + random.randint(-150, -100)  # left stop
        ld_ss[1][1] = ld_ss[0][1] + random.randint(-30, -10)  # down stop

        return ld_ss






