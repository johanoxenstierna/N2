
import numpy as np

class AbstractLayer:
    """
    Obs doesn't have access to the ax itself, only the info about it.
    Obs if an object is to change its movement it needs a new layer instance.
    """

    def __init__(_s):
        _s.drawn = 0  # 0: not drawn, 1: start drawing, 2. continue drawing, 3. end drawing
        _s.clock = 0
        _s.frames_num = None  # number of frames to animate for
        _s.frame_ss = None
        _s.index_im_ax = None
        _s.pic = None

    def set_clock(_s, i):
        """
        The layer classes don't have access to the ax, so
        this essentially tells the ax what to do.
        """

        if i == _s.frame_ss[0]:
            _s.drawn = 1
        elif i > _s.frame_ss[0] and i < _s.frame_ss[1]:
            _s.drawn = 2
            _s.clock += 1
        elif i == _s.frame_ss[1]:
            _s.drawn = 3
            _s.clock = 0  # ONLY PLACE WHERE RESET
        else:
            _s.drawn = 0

    def ani_update_step(_s, ax, im_ax):
        """
        Based on the drawn condition, draw, remove
        If it's drawn, return True (used in animation loop)
        """

        if _s.drawn == 0:  # not drawn,
            return False
        elif _s.drawn == 1: # start and continue
            _s.index_im_ax = len(im_ax)
            # im_ax[_s.ship_info['id']] = ax.imshow(_s.pic, zorder=1, alpha=1)
            im_ax.append(ax.imshow(_s.pic, zorder=1, alpha=1))
            return True
        elif _s.drawn == 2:  # continue drawing
            return True
        elif _s.drawn == 3:  # end drawing
            im_ax[_s.index_im_ax].remove()  # might save CPU-time
            im_ax.pop(_s.index_im_ax)
            _s.index_im_ax = None  # THIS IS NEEDED BUT NOT SURE WHY
            return False






