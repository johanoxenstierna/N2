
from matplotlib.pyplot import imread
from src.gen_extent_triangles import *
pic = imread('./images/processed/ships/7/7.png')

mi = {
    "1": {"ld_start": [100, 300], "ld_end": [200, 100],
          "scale_ss": [0.5, 0.5],
          "y_mid": 1.0,
          "frame_ss": [5, 100],
          "roll_cycles": 5,
          "t": {"extent[0]": [100, 150, 300, 200], "extent[-1]": [200, 250, 100, 0],
                "extent_t[0]": [0, 50, 100, 0], "extent_t[-1]": [100, 150, -100, -200],
                "tri_base": [[0, 200], [50, 0], [100, 200]],
                "tris[0]": [[0, 300], [25, 200], [50, 300]], "tris[-1]": [[100, 100], [125, 0], [150, 100]],
                "mask_x": 250, "mask_y": 300}},
    "2": {"ld_start": [100, 400], "ld_end": [200, 200],
          "scale_ss": [0.5, 1.0],
          "y_mid": 1.0,
          "frame_ss": [5, 100],
          "roll_cycles": 5,
          "t": {"extent[0]": [100, 150, 300, 200], "extent[-1]": [200, 250, 100, 0],
                "extent_t[0]": [0, 50, 100, 0], "extent_t[-1]": [100, 150, -100, -200],
                "tri_base": [[0, 200], [50, 0], [100, 200]],
                "tris[0]": [[0, 300], [25, 200], [50, 300]], "tris[-1]": [[100, 100], [125, 0], [150, 100]],
                "mask_x": 250, "mask_y": 300}
          },
    "3": {"ld_start": [100, 300], "ld_end": [200, 100],
          "scale_ss": [0.5, 1.0],
          "y_mid": 1.0,
          "frame_ss": [5, 100],
          "roll_cycles": 5
          }
}


extent, extent_t, lds_log, scale_vector = gen_extent(mi['1'], pic, padded=False)  # left_down_log
tri_base, tris, tri_max_x, tri_max_y, tri_min_x, tri_min_y, mask_x, mask_y = \
    gen_triangles(extent_t, extent, mi['1'], pic)

# TEST 4'S
for i in range(4):
    assert(abs(mi['1']['t']['extent[0]'][i] - extent[0][i]) < 1)
    assert(abs(mi['1']['t']['extent[-1]'][i] - extent[-1][i]) < 1)
    assert(abs(mi['1']['t']['extent_t[0]'][i] - extent_t[0][i]) < 1)
    assert(abs(mi['1']['t']['extent_t[-1]'][i] - extent_t[-1][i]) < 1)

# TEST TRIs
for i in range(3):
    assert(abs(mi['1']['t']['tri_base'][i][0] - tri_base[i][0]) < 1)
    assert(abs(mi['1']['t']['tri_base'][i][1] - tri_base[i][1]) < 1)
    assert(abs(mi['1']['t']['tris[0]'][i][0] - tris[0][i][0]) < 1)
    assert(abs(mi['1']['t']['tris[0]'][i][1] - tris[0][i][1]) < 1)
    assert (abs(mi['1']['t']['tris[-1]'][i][0] - tris[-1][i][0]) < 1)
    assert (abs(mi['1']['t']['tris[-1]'][i][1] - tris[-1][i][1]) < 1)

assert(abs(mi['1']['t']['mask_x'] - mask_x) < 1)
assert(abs(mi['1']['t']['mask_y'] - mask_y) < 1)

aa = 6