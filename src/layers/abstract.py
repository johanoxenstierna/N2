


class AbstractLayer:
    """
    Obs doesn't have access to the ax itself, only the info about it.
    Obs if an object is to change its movement it needs a new layer instance.
    """

    def __init__(s):
        s.drawn = 0  # 0: not drawn, 1: start drawing, 2. continue drawing, 3. end drawing
        s.clock = 0
        s.frames_num = None  # number of frames to animate for
        s.frame_ss = None
        s.index_im_ax = None

    def set_clock(s, i):
        """
        The layer classes don't have access to the ax, so
        this essentially tells the ax what to do.
        """

        if i == s.frame_ss[0]:
            s.drawn = 1
        elif i > s.frame_ss[0] and i < s.frame_ss[1]:
            s.drawn = 2
            s.clock += 1
        elif i == s.frame_ss[1]:
            s.drawn = 3
            s.clock = 0  # ONLY PLACE WHERE RESET
        else:
            s.drawn = 0

