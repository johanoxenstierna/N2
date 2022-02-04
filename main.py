"""
warpAffine current solution: The extent of the warp is always by the maximum triangle value.
WARP AFFINE DOES NOT WORK WITH NEGATIVE VALUES!!!! CANNOT WARP TO NEGATIVE VALUE (PIC WILL JUST DISSAPEAR)
im_ax li: 2.9  35 min/vid
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

from src import gen_layers
from src.ani_helpers import *
import P as P
from src.chronicler import Chronicler

Chronicler() # just outputs the json below
with open('./src/chronicle.json', 'r') as f:
    ch = json.load(f)


WRITE = 0  #60  # change IMMEDIATELY back to zero (it immediately kills old file when re-run)
FPS = 20

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)

fig, ax = plt.subplots(figsize=(12, 8))

# im_ax = {}
im_ax = []
g = gen_layers.GenLayers(ch)
g.gen_backgr(ax, im_ax)  # ax is the canvas, im_ax contains pointers to what is plotted on canvas
ships = g.gen_ships(ax, im_ax)  # ships is dict of pointers to all info about ship (except in im_ax)
if P.A_SAILS:
    ships = g.gen_sails(ax, im_ax, ships)

if P.A_SMOKAS:
    ships = g.gen_smokes(ax, im_ax, ships, type='a')

aa = 2

def init():
    return im_ax


def animate(i):

    # if i % 10 == 0:
    print("i: " + str(i), "  len_im_ax: " + str(len(im_ax)))

    for ship_id, ship in ships.items():

        ship.set_clock(i)  # sets drawn if clock is within draw range

        # THIS SHOULD BE GENERALIZED FOR ALL AFFINE LAYERS = MOVE TO FUNCTION
        drawBool = ship.ani_update_step(ax, im_ax)  # uses clock set above
        if drawBool == False:
            continue

        # PERHAPS MOVE ALL THIS INTO A FUNCTION (IN SHIP CLASS WITH IM_AX AS INPUT)
        if P.A_AFFINE_TRANSFORM == 0:
            im_ax[ship_id].set_extent(ship.extent[ship.clock])
        else:

            warp_affine(i, ax, im_ax, ship, ch)

            # im_ax[ship.index_im_ax].remove()  # BOTH NECESSARY
            # im_ax.pop(ship.index_im_ax)  # BOTH NECESSARY
            #
            # t0 = ship.tri_base
            # t1 = ship.tris[ship.clock]
            # # img = g.pics['ships']['7']['ship']
            # img = ship.pic  # pic with base scale always used.
            # # if P.A_COLORS:
            # #     img = ship.apply_col_transform(ch['ships'][ship_id]['firing_frames'], i)
            #
            # M = cv2.getAffineTransform(t0, t1)
            # dst = cv2.warpAffine(img, M, (int(ship.tri_ext['max_ri']), int(ship.tri_ext['max_do'])))
            # img = np.zeros((ship.mask_do, ship.mask_ri, 4))
            # img[img.shape[0] - dst.shape[0]:, img.shape[1] - dst.shape[1]:, :] = dst
            # im_ax.insert(ship.index_im_ax, ax.imshow(img, zorder=ship.ship_info['zorder'], alpha=1))

        if P.A_SAILS:  # NOT CONVERTED TO LIST YET
            for sail_id, sail in ships[ship_id].sails.items():
                if i == 20:
                    gg = 6
                sail.set_clock(i)
                drawBool = sail.ani_update_step(ax, im_ax)
                if drawBool == False:
                    continue

                warp_affine(i, ax, im_ax, sail, ch, parent_obj=ship)  # parent obj required for sail


                #
                # im_ax[sail.index_im_ax].remove()
                # im_ax.pop(sail.index_im_ax)
                #
                # t0 = sail.tri_base
                # t1 = sail.tris[sail.clock]
                # img = sail.pic  # SHOULD WORK
                # # img = g.pics['ships']['7']['sails']['7_s_0']
                # if P.A_COLORS:
                #     img = sail.apply_transform(ch['ships'][ship_id]['firing_frames'], i)
                # M = cv2.getAffineTransform(t0, t1)
                # dst = cv2.warpAffine(img, M, (int(sail.tri_ext['max_ri']), int(sail.tri_ext['max_do'])))
                # img = np.zeros((sail.mask_do, sail.mask_ri, 4))
                # img[img.shape[0] - dst.shape[0]:, img.shape[1] - dst.shape[1]:, :] = dst
                # im_ax.insert(sail.index_im_ax, ax.imshow(img, zorder=sail.gi['zorder'], alpha=0.7))

    # INFO IS FOUND IN SHIPS, BUT IM_AX IS STORED SEPARATELY (BECAUSE SHIPS CAN GO AWAY WHILE SMOKE PERSISTS)
    if P.A_SMOKAS:
        for ship_id, ship in ships.items():
            for smoka_id, smoka in ships[ship_id].smokas.items():
                pass
        pass


    return im_ax  # if run live, it runs until window is closed


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