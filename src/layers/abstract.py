
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
        # _s.frame_ss_start_offset = None
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
        OBS major bug discovered: im_ax.pop(index_im_ax) OBVIOUSLY results in that all index_im_ax after popped get
        screwed.
        0: don't draw
        1: draw
        2: don't draw and decrement all index_im_ax's
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






