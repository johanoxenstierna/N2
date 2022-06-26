"""
warpAffine current solution: The extent of the warp is always by the maximum triangle value.
WARP AFFINE DOES NOT WORK WITH NEGATIVE VALUES!!!! CANNOT WARP TO NEGATIVE VALUE (PIC WILL JUST DISSAPEAR)
OBS d e c r e m e n t _ a l l _ i n d e x _ i m _ a x (index_removed, ships, waves)  FOROGT 5 times

gi: general info. OBS is unique to each layer
spl kept separate from expl cuz spl lasts much longer

im_ax li: 2.9  35 min/vid

BUG CHECK:
1. Firing frames cannot exceed the ship visible frames (duh)
"""

# geometric image transformations.



import numpy as np
import random
random.seed(6)  # ONLY HERE
np.random.seed(6)  # ONLY HERE
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

WRITE = 53  #FIX: smoka frames, waves  # change IMMEDIATELY back to zero (it immediately kills old file when re-run)
FPS = 20

Writer = animation.writers['ffmpeg']
writer = Writer(fps=FPS, metadata=dict(artist='Me'), bitrate=3600)

fig, ax = plt.subplots(figsize=(10, 6))
# fig, ax = plt.subplots()

# im_ax = {}
im_ax = []
g = gen_layers.GenLayers(ch)
g.gen_backgr(ax, im_ax)  # ax is the canvas, im_ax contains pointers to what is plotted on canvas

# BELOW THE PY OBJECTS THAT TRACK THEIR IM_AX COUNTERPARTS ARE GENERATED
ships = g.gen_ships(ax, im_ax)  # ships is dict of pointers to all info about ship (except in im_ax)
if P.A_SAILS:
    ships = g.gen_sails(ax, im_ax, ships)

if P.A_SMOKAS:
    ships = g.gen_smokas(ax, im_ax, ships, ch)

if P.A_SMOKRS:
    ships = g.gen_smokrs(ax, im_ax, ships, ch)

if P.A_EXPLS:  # all expls put in for each ship (convenient and memory cheap)
    ships = g.gen_expls(ax, im_ax, ships, ch)

if P.A_SPLS:  # all expls put in for each ship (convenient and memory cheap)
    ships = g.gen_spls(ax, im_ax, ships, ch)

# if P.A_WAVES:
waves = g.gen_waves(ax, im_ax)  # can't use if P.A_WAVES bcs empty list is needed always (to decrement index thingy)
# TODO: cross verify loaded objs vs loaded pics
aa = 2

def init():
    return im_ax


def animate(i):
    """
    Conjecture: Obs expls and halo can't be precomputed
    """

    # if i % 10 == 0:
    prints = "i: " + str(i) + "  len_im_ax: " + str(len(im_ax))

    for ship_id, ship in ships.items():

        ship.set_clock(i)  # sets drawn if clock is within draw range
        drawBool, index_removed = ship.ani_update_step(ax, im_ax)  # uses clock set above
        if drawBool == 0:
            continue
        elif drawBool == 2:  # ship is removed this frame
            decrement_all_index_im_ax(index_removed, ships, waves)
            continue

        # SHIP WARPED BELOW EXPL (EXPLAIN WHY FFS) (BECAUSE EXPL SHOULD AFFECT IT?)
        warp_affine_and_color(i, ax, im_ax, ship, ch)

        if P.A_EXPLS:
            if i in ship.gi['firing_frames']:
                expl = ship.find_free_obj(type='expl')
                if expl != None:
                    expl.drawn = 1  # this variable is needed to avoid the frame_ss check
                    expl.frame_ss[0] = i
                    expl.frame_ss[1] = i + expl.NUM_FRAMES_EXPL
                    expl.comp_extent_alpha_expl()
                else:
                    prints += "  no free expl"

            for expl_id, expl in ship.expls.items():

                if expl.drawn != 0:  # same 1 from above gatekeeper used here but REMEMBER 4 might be necessary.
                    expl.set_clock(i)
                    drawBool, index_removed = expl.ani_update_step(ax, im_ax)
                    if drawBool == 0:
                        continue
                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, ships, waves)
                        continue

                    # im_ax[expl.index_im_ax].set_extent(expl.extent)
                    im_ax[expl.index_im_ax].set_extent(expl.extent[expl.clock])
                    im_ax[expl.index_im_ax].set_alpha(1.0)  # replace with invisibility after 1st frame OR the tracer event
                    # Perhaps it won't be needed if 3 frames is not too much for expl (when tracer not used).
                    im_ax[expl.index_im_ax].set_zorder(expl.zorder)  # TEMP

        # SHIP WARP

        '''
        Conjecture: It won't be enough to just plot the expl, it also needs to affect brightness/contr of other 
        ax object (especially when the special red explosions start (fire)).
        expl only needs to be displayed 1-5 frames (e.g. tracer), but it still needs to be added and then removed from im_ax.
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

        if P.A_SPLS:
            '''If warp_affine NOT gonna be used each spl needs a copy pic which is a brighter version, to be shown
             when spl is on top of ship. 
            '''
            if i in ship.gi['firing_frames']:  # add rand
                spl = ship.find_free_obj(type='spl')
                if spl != None:
                    exceeds_frame_max, how_many = spl.check_frame_max(i, spl.NUM_FRAMES_SPL)
                    if exceeds_frame_max == True:
                        prints += "  cant add spl"
                        spl.NUM_FRAMES_SPL = how_many
                        # continue
                    spl.drawn = 1  # this variable is needed to avoid the frame_ss check

                    spl.init_dyn_obj(i, spl.NUM_FRAMES_SPL)
                    spl.comp_zorder(ships, i)
                    spl.gen_dyn_extent_alpha()

                else:
                    prints += "  no free spl"

            for spl_id, spl in ship.spls.items():
                '''NEED WARP_AFFINE SINCE COLOR OF SPL SHOULD CHANGE BASED ON WHETHER ITS OVER SHIP OR NOT
                ALSO, spl will be part of the fire so need to look good. 
                '''
                if spl.drawn != 0:  # same 1 from above gatekeeper used here but REMEMBER 4 might be necessary.
                    spl.set_clock(i)
                    drawBool, index_removed = spl.ani_update_step(ax, im_ax)
                    if drawBool == 0:
                        continue
                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, ships, waves)
                        continue

                    im_ax[spl.index_im_ax].set_extent(spl.extent[spl.clock])
                    # warp_affine_and_color(i, ax, im_ax, spl, ch)  # doesn't work for objects that grow then shrink
                    im_ax[spl.index_im_ax].set_alpha(spl.alpha[spl.clock])  # replace with invisibility after 1st frame OR the tracer event
                    # im_ax[spl.index_im_ax].set_alpha(1)  # replace with invisibility after 1st frame OR the tracer event
                    # im_ax[spl.index_im_ax].set_zorder(999)  # SHOULD NOT BE NEEDED SINCE ITS DONE IN ANI_UPDATE_STEP

        if P.A_SMOKRS:
            if i in ship.gi['firing_frames']:  # add rand
                smokr = ship.find_free_obj(type='smokr')
                if smokr != None:
                    exceeds_frame_max, how_many = smokr.check_frame_max(i, smokr.NUM_FRAMES_SMOKE)
                    if exceeds_frame_max == True:
                        prints += "  smokr exceeds max"
                        smokr.NUM_FRAMES_SMOKE = how_many
                        # continue
                    smokr.drawn = 4  # NEEDED TO SET STATIC_DARKENING FIRST FRAME
                    smokr.init_dyn_obj(i, smokr.NUM_FRAMES_SMOKE)
                    smokr.gen_dyn_extent_alpha()
                else:
                    prints += "  no free smokr"

            for smokr_id, smokr in ship.smokrs.items():
                if smokr.drawn != 0:  # the 4 from above is needed only the very first iteration it becomes visible
                    smokr.set_clock(i)
                    drawBool, index_removed = smokr.ani_update_step(ax, im_ax)
                    if drawBool == 0:
                        continue
                    elif drawBool == 2:
                        decrement_all_index_im_ax(index_removed, ships, waves)
                        continue

                    # im_ax[smokr.index_im_ax].set_extent(smokr.extent[smokr.clock])
                    warp_affine_and_color(i, ax, im_ax, smokr, ch)  # parent obj required for sail

                    im_ax[smokr.index_im_ax].set_alpha(smokr.alpha[smokr.clock])
                    im_ax[smokr.index_im_ax].set_zorder(smokr.zorder)

        if P.A_SAILS:
            '''
            TODO implement queue system. Not needed if same sail used for all the frames that ship shown.
            Might be difficult due to movement black though.   
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
                # im_ax[sail.index_im_ax].set_extent(sail.extent[sail.clock])
                im_ax[sail.index_im_ax].set_zorder(sail.zorder)  # TEMP?

        if P.A_SMOKAS:

            if i == 28:
                adf = 5

            if i in ship.gi['smoka_init_frames']:

                smoka = ship.find_free_obj(type='smoka')

                if smoka != None and smoka.id not in ship.gi['smokas_hardcoded']['ids']:
                    exceeds_frame_max, how_many = smoka.check_frame_max(i, smoka.NUM_FRAMES_SMOKE)
                    if exceeds_frame_max == True:
                        prints += "  smoka exceeds max"
                        smoka.NUM_FRAMES_SMOKE = how_many
                        # continue
                    smoka.drawn = 1  # this variable can serve multiple purposes (see below, and in set_clock)
                    ship.smoka_latest_drawn_id = smoka.id
                    smoka.init_dyn_obj(i, smoka.NUM_FRAMES_SMOKE)  # uses AbstractSSS
                    smoka.gen_dyn_extent_alpha()
                else:
                    prints += "  no free smoka"

            if i in ship.gi['smokas_hardcoded']['frames_start']:
                index = ship.gi['smokas_hardcoded']['frames_start'].index(i)
                smoka_id = ship.gi['smokas_hardcoded']['ids'][index]
                smoka = ship.smokas[smoka_id]
                frame_start = ship.gi['smokas_hardcoded']['frames_start'][index]  # this is needed since ani loop must search for start frame
                frame_stop = ship.gi['smokas_hardcoded']['frames_stop'][index]
                # smoka.NUM_FRAMES_SMOKE = frame_stop - frame_start
                smoka.gi['frame_ss'] = [frame_start, frame_stop]  # PENDING DEL NEEDS TO BE SET IN animation loop
                smoka.frame_ss = smoka.gi['frame_ss']
                smoka.drawn = 1  # this variable can serve multiple purposes (see below, and in set_clock)
                # smoka.init_dyn_obj(i, smoka.NUM_FRAMES_SMOKE)  # SHOULD NOT BE NEEDED
                smoka.gen_dyn_extent_alpha()
                # smoka = ship.smokas[ship]
                aa = 5

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
                    # im_ax[smoka.index_im_ax].set_zorder(smoka.zorder)  # SET IN ANI_UPDATE_STEP

        if i == ship.gi['alpha_and_bright'][ship.ab_clock][0] and ship.ab_clock < len(ship.gi['alpha_and_bright']) - 1:
            ship.ab_clock += 1

        hardcoded_adjustments(ship, i)

    if P.A_WAVES:  # no queue needed here since they
        '''
        No need to iterate through all ships and their expls for all waves, so instead a ship 
        is picked at random for each wave and its brightness is computed based on distance to the expl 
        '''
        for wave_id, wave in waves.items():
            if i == 15:
                adf = 5

            wave.set_clock(i)  # sets drawn if clock is within draw range NEEDS frame_ss
            drawBool, index_removed = wave.ani_update_step(ax, im_ax)  # uses clock set above
            if drawBool == 0:
                continue
            elif drawBool == 2:
                decrement_all_index_im_ax(index_removed, ships, waves)
                continue

            # DRAW ================
            ship__ = random.choice(list(ships.values()))
            im_ax[wave.index_im_ax].set_extent(wave.extent[wave.clock])
            im_ax[wave.index_im_ax].set_alpha(wave.alpha[wave.clock])
            if i in ship__.gi['firing_frames'] and P.A_FIRING_BRIGHTNESS:  # alpha might be enough here (changing brightness is tricky without using the warp affine wrapper function)
                ship_ld = np.asarray([ship__.extent[i][0], ship__.extent[i][2]])
                wave_ld = np.asarray([wave.extent[wave.clock][0], wave.extent[wave.clock][2]])
                distance = int(np.linalg.norm(ship_ld - wave_ld))
                im_ax[wave.index_im_ax].set_alpha(wave.alpha_wave_expl[distance])

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