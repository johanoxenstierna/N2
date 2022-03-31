"""
warpAffine current solution: The extent of the warp is always by the maximum triangle value.
WARP AFFINE DOES NOT WORK WITH NEGATIVE VALUES!!!! CANNOT WARP TO NEGATIVE VALUE (PIC WILL JUST DISSAPEAR)

gi: general info. OBS is unique to each layer

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

# BELOW THE PY OBJECTS THAT TRACK THEIR IM_AX COUNTERPARTS ARE GENERATED
ships = g.gen_ships(ax, im_ax)  # ships is dict of pointers to all info about ship (except in im_ax)
if P.A_SAILS:
    ships = g.gen_sails(ax, im_ax, ships)

if P.A_SMOKAS:
    ships = g.gen_smokes(ax, im_ax, ships, ch, type='a')

if P.A_EXPLS:  # all expls put in for each ship (convenient and memory cheap)
    ships = g.gen_expls(ax, im_ax, ships, ch)

# if P.A_WAVES:
waves = g.gen_waves(ax, im_ax)  # can't use if P.A_WAVES bcs empty list is needed always (to decrement index thingy)

aa = 2

def init():
    return im_ax


def animate(i):
    """
    Conjecture: Obs expls and halo can't be precomputed
    """

    # if i % 10 == 0:
    prints = "i: " + str(i) + "  len_im_ax: " + str(len(im_ax))

    # aa = find_all_ax_at_coord()

    for ship_id, ship in ships.items():

        ship.set_clock(i)  # sets drawn if clock is within draw range
        drawBool, index_removed = ship.ani_update_step(ax, im_ax)  # uses clock set above
        if drawBool == 0:
            continue
        elif drawBool == 2:  # ship is removed this frame
            decrement_all_index_im_ax(index_removed, ships, waves)
            continue

        warp_affine_and_color(i, ax, im_ax, ship, ch)

        if P.A_EXPLS:
            if i in ship.gi['firing_frames']:
                expl = ship.find_free_obj(type='expl')
                if expl != None:
                    expl.drawn = 4  # this variable can serve multiple purposes (see below, and in set_clock)
                    expl.frame_ss[0] = i
                    expl.frame_ss[1] = i + expl.NUM_FRAMES_EXPL
                    expl.set_extent_expl()
                else:
                    prints += "  no free expl"

            for expl_id, expl in ship.expls.items():

                if expl.drawn != 0:  # the 4 from above is needed only the very first iteration it becomes visible
                    expl.set_clock(i)
                    drawBool, index_removed = expl.ani_update_step(ax, im_ax)
                    if drawBool == 0:
                        continue
                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, ships, waves)
                        continue

                    im_ax[expl.index_im_ax].set_extent(expl.extent)
                    im_ax[expl.index_im_ax].set_alpha(1.0)  # replace with inverse sigmoid
                    im_ax[expl.index_im_ax].set_zorder(999)  # TEMP

            '''
            Conjecture: It won't be enough to just plot the expl, it also needs to affect brightness/contr of other 
            ax object (especially when the special red explosions start (fire)).
            expl only needs to be displayed 1-2 frames, but it still needs to be added and then removed from im_ax.
            However, it will appear toward the end of im_ax so decrementing im_ax will be cheap. 
            frame_sss for expls could be pre-computed, but there STILL needs to be a check to see if an expl is 
            available for drawing (otherwise one has to find the lower bound on number of expls and produce
            a corresponding number of im_ax's i.e. pictures, which is totally illegit om this implementation
            since pics are pre-loaded).
            Thus expls frames are computed dynamically. Instead of frame_ss, if i corresponds to ship firing_frame, 
            pick free expl instance at random (each ship has 4) to display and coord from expl xtra info. 
            The expl instance contains a clock variable that checks how many frames the expl has been active for.  
            This and its coord are then used by smokes, sails, waves to update brightness_contrast.
            Amount should be inverse sigmoid of the distance to the expl + min-max-scaling. The centroid of 
            the layer at frame i can be obtained using layer.extent
            Only certain pixels for the ships should be affected and they are precomputed. 
            '''

        if P.A_SAILS:
            '''
            TODO implement queue system. Not needed if same sail used for all the frames that ship shown.
            Might be difficult due to movement black.   
            '''
            for sail_id, sail in ships[ship_id].sails.items():

                sail.set_clock(i)
                drawBool, index_removed = sail.ani_update_step(ax, im_ax)
                if drawBool == 0:
                    continue
                elif drawBool == 2:
                    decrement_all_index_im_ax(index_removed, ships, waves)
                    continue

                warp_affine_and_color(i, ax, im_ax, sail, ch, parent_obj=ship)  # parent obj required for sail

        if P.A_SMOKAS:

            if i in ship.gi['smoka_init_frames']:
                smoka = ship.find_free_obj(type='smoka')
                if smoka != None:
                    smoka.drawn = 4  # this variable can serve multiple purposes (see below, and in set_clock)
                    smoka.init_dyn_obj(i, smoka.NUM_FRAMES_SMOKA)  # uses AbstractSSS
                    smoka.gen_dyn_extent_alpha()
                else:
                    prints += "  no free smoka"

            for smoka_id, smoka in ship.smokas.items():
                if smoka.drawn != 0:  # the 4 from above is needed only the very first iteration it becomes visible
                    smoka.set_clock(i)
                    drawBool, index_removed = smoka.ani_update_step(ax, im_ax)
                    if drawBool == 0:
                        continue
                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, ships, waves)
                        continue

                    warp_affine_and_color(i, ax, im_ax, smoka, ch)  # parent obj required for sail

                    im_ax[smoka.index_im_ax].set_alpha(smoka.alpha[smoka.clock])


    if P.A_WAVES:  # no queue needed here since they
        for wave_id, wave in waves.items():
            if i == 15:
                adf = 5
            # wave.set_ss(i)  # special function for wave to set the current frame_ss and ld_ss (since the same wave will be plotted several times)
            # print(str(wave.frame_ss) + "  " + str(wave.clock))
            wave.set_clock(i)  # sets drawn if clock is within draw range NEEDS frame_ss
            drawBool, index_removed = wave.ani_update_step(ax, im_ax)  # uses clock set above
            if drawBool == 0:
                continue
            elif drawBool == 2:
                decrement_all_index_im_ax(index_removed, ships, waves)
                continue

            # DRAW ================
            im_ax[wave.index_im_ax].set_extent(wave.extent[wave.clock])
            # except:
            #     adf = 5
            im_ax[wave.index_im_ax].set_alpha(wave.alpha[wave.clock])


    print(prints)

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