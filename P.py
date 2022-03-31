MAP_SIZE = 'small'  # 488, 185
# MAP_SIZE = 'big'  # 1280 720  # also check ship info (copy-paste)
FRAMES_START = 0
FRAMES_STOP = 250  # frames info: 1200/min 12000 for 10 min.   Takes ~30 min to gen 1000 frames
if MAP_SIZE == 'small':
    FRAMES_START = 0
    FRAMES_STOP = 250
FRAMES_TOT = FRAMES_STOP - FRAMES_START

# A (what to animate) ========
A_AFFINE_TRANSFORM = 1
A_SAILS = 1
A_SAIL_HEIGHTS_TROUGHS_TRANSFORM = 0
A_HSV_TRANSFORM = 1
A_SMOKAS = 0
A_WAVES = 0
A_EXPLS = 1
A_HARDCODED_DARKENING = 0

NUM_WAVES = 7  # NUM per pic!!!
NUM_SMOKAS = 2
NUM_EXPLS = 1  # capability for >1 there but might not be needed
PR_MOVE_BLACK = 1  # what to pre-compute

WAVES_STEPS_P_CYCLE = 90  #
SAIL_STEPS_P_CYCLE = 360  # 120 # (6 sec)
SAIL_CYCLES = 3
WS_STEPS = 40  # 2s  wave front of ship
SPLASH_STEPS_P_CYCLE = 150
# SPL_FRAME_OFFSET = 25  # not good design-wise
EXPL_CYCLES = 8  # how often broadsides happen

SHIPS_TO_SHOW = ['7']

EXPLOSION_WIDTH = 8
EXPLOSION_HEIGHT = 3

# SMOKES ======

# NUM_SMOKRS = 20  # 20 NUM per type.
# SMOKE_R_F_FRAMES = 720  # 540
# SMOKA_FRAMES = 5  # 480  # moved to smoke class
# NUM_SPLS = 20 #20  # num per type.


# DEFAULT ZORDERS =====
Z_SMOKR = 5
Z_SMOKA = 4
Z_SHIP = 6
Z_XTRA = 7
Z_EXPL = 8