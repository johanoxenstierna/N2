"""
warpAffine current solution: The extent of the warp is always by the maximum triangle value.
WARP AFFINE DOES NOT WORK WITH NEGATIVE VALUES!!!! CANNOT WARP TO NEGATIVE VALUE (PIC WILL JUST DISSAPEAR)
"""

# geometric image transformations.

import numpy as np
import random
random.seed(7)  # ONLY HERE
np.random.seed(7)  # ONLY HERE
import time
import json
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
from copy import deepcopy

from src import gen_layers, PARAMS as P, load_pics


WRITE = 0  #60  # change IMMEDIATELY back to zero (it immediately kills old file when re-run)
FPS = 20

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)

fig, ax = plt.subplots(figsize=(12, 8))

# im_ax = {}
im_ax = []
g = gen_layers.GenLayers()
g.gen_backgr(ax, im_ax)  # ax is the canvas, im_ax contains pointers to what is plotted on canvas
ships = g.gen_ships(ax, im_ax)  # ships is dict of pointers to all info about ship (except in im_ax)
# ships = g.gen_sails(ax, im_ax, ships)

aa = 5

def init():
    return im_ax


def animate(i):

    if i % 10 == 0:
        print(i)

    # EXPLOSION EVENT. IF THIS HAPPENS A LIST OF COORDINATES SHOULD BE INITED AND THEN COL-CHANGES SHOULD BE AFFECTED

    for ship_id, ship in ships.items():

        ship.set_clock(i)  # sets drawn if clock is within draw range

        # THIS SHOULD BE GENERALIZED FOR ALL AFFINE LAYERS = MOVE TO FUNCTION
        if ship.drawn == 0:  # 0: not drawn, 1: start drawing, 2. continue drawing, 3. end drawing
            continue
        elif ship.drawn == 1:
            ship.index_im_ax = len(im_ax)
            # im_ax[ship_id] = ax.imshow(ship.pic, zorder=1, alpha=1)
            im_ax.append(ax.imshow(ship.pic, zorder=1, alpha=1))
        elif ship.drawn == 2:
            pass
        elif ship.drawn == 3:
            # im_ax[ship_id].remove()  # might save CPU-time
            continue

        # PERHAPS MOVE ALL THIS INTO A FUNCTION (IN SHIP CLASS WITH IM_AX AS INPUT)
        if P.A_AFFINE_TRANSFORM == 0:
            im_ax[ship_id].set_extent(ship.extent[ship.clock])
        else:
            # im_ax[ship_id].remove()
            im_ax.pop(ship.index_im_ax)
            t0 = ship.tri_base
            t1 = ship.tris[ship.clock]
            # image = g.pics['ships']['7']['ship']
            image = ship.pic

            if P.A_COLORS:
                image = ship.apply_col_transform(expl_coords=[[50, 50]])

            M = cv2.getAffineTransform(t0, t1)
            dst = cv2.warpAffine(image, M, (int(ship.tri_max_x), int(ship.tri_max_y)))
            image = np.zeros((ship.mask_y, ship.mask_x, 4))
            image[image.shape[0] - dst.shape[0]:, image.shape[1] - dst.shape[1]:, :] = dst

            # im_ax[ship_id] = ax.imshow(image, zorder=5, alpha=1)
            ship.index_im_ax = len(im_ax)
            im_ax.append(ax.imshow(image, zorder=5, alpha=1))

        if P.A_SAILS:  # NOT CONVERTED TO LIST YET
            for sail_id, sail in ships[ship_id].sails.items():
                sail.set_clock(i)
                if sail.drawn == 0:  # 0: not drawn, 1: start drawing, 2. continue drawing, 3. end drawing
                    continue
                elif sail.drawn == 1:
                    im_ax[sail_id] = ax.imshow(g.pics['ships'][ship_id]['sails'][sail_id], zorder=6, alpha=1)
                elif sail.drawn == 2:
                    pass
                elif sail.drawn == 3:
                    im_ax[sail_id].remove()  # might save CPU-time
                    # im_ax[sail_id].remove()  # might save CPU-time
                    continue

                im_ax[sail_id].remove()
                t0 = sail.tris[0]
                t1 = sail.tris[sail.clock]
                image = g.pics['ships'][ship_id]['sails'][sail_id]
                M = cv2.getAffineTransform(t0, t1)
                dst = cv2.warpAffine(image, M, (int(sail.tri_max_x), int(sail.tri_max_y)))
                pad = np.zeros((sail.padding_y, sail.padding_x, 4))
                pad[pad.shape[0] - dst.shape[0]:, pad.shape[1] - dst.shape[1]:, :] = dst
                im_ax[sail_id] = ax.imshow(pad, zorder=6, alpha=1)


    return im_ax


sec_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS)
min_vid = ((P.FRAMES_STOP - P.FRAMES_START) / FPS) / 60
print("len of vid: " + str(sec_vid) + " s" + "    " + str(min_vid) + " min")


start_t = time.time()
ani = animation.FuncAnimation(fig, animate, frames=range(P.FRAMES_START, P.FRAMES_STOP),
                              blit=True, interval=1, init_func=init,
                              repeat=False)  # interval only affects live ani. blitting seems to make it crash

if WRITE == 0:
    plt.show()
else:
    ani.save('./vids/vid_' + str(WRITE) + '.mp4', writer=writer)

tot_time = round((time.time() - start_t) / 60, 4)
print("minutes to make animation: " + str(tot_time) + " |  min_gen/min_vid: " + str(tot_time / min_vid))  #