MAP_SIZE = 'small'  # 488, 185
# MAP_SIZE = 'big'  # 1280 720
FRAMES_START = 0
FRAMES_STOP = 200  # frames info: 1200/min 12000 for 10 min.   Takes ~30 min to gen 1000 frames
if MAP_SIZE == 'small':
    FRAMES_START = 0
    FRAMES_STOP = 100
FRAMES_TOT = FRAMES_STOP - FRAMES_START

# A (what to animate) ========
A_AFFINE_TRANSFORM = 1
A_SAILS = 0
A_COLORS = 1

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
NUM_SMOKAS = 10  # 10 NUM per type.
NUM_SMOKRS = 20  # 20 NUM per type.
SMOKE_R_F_FRAMES = 720  # 540
SMOKA_FRAMES = 960  # 480
NUM_SPLS = 20 #20  # num per type.
NUM_WAVES = 15 #15  # NUM per type.

# DEFAULT ZORDERS =====
Z_SMOKR = 5
Z_SMOKA = 4
Z_SHIP = 6
Z_XTRA = 7
Z_EXPL = 8