import os
import json
from src.load_pics import load_pics
import P as P
from src.layers.ship import Ship
from src.layers.sail import Sail
from src.layers.smoke import Smoke
from src.layers.wave import Wave
from src.layers.expl import Expl
from src.layers.spl import Spl

class GenLayers:

    """
    OBS this time it's only the background that is being ax.shown here. The other ax objects are gona be added and
    deleted within the animation loop.
    """

    def __init__(self, ch):
        self.pics = load_pics(ch)
        self.PATH_IMAGES = './images/processed/'
        self.ch = ch

    def gen_backgr(self, ax, im_ax):
        im_ax.append(ax.imshow(self.pics['backgr'], zorder=1, alpha=1))
        im_ax.append(ax.imshow(self.pics['frame'], zorder=99999))
        if P.MAP_SIZE == 'small':
            ax.axis([0, 571, 0, 500])
        else:
            ax.axis([0, 1280, 0, 720])
        ax.invert_yaxis()
        # ax.grid()
        ax.axis('off')  # TURN ON FOR FINAL

    def gen_ships(self, ax, im_ax):

        ships = {}
        for ship_id in P.SHIPS_TO_SHOW:  # number_id
            # with open('./ship_info/' + P.MAP_SIZE + '/' + ship_id + '.json', 'r') as f:
            #     ship_info = json.load(f)

            ships[ship_id] = Ship(self.ch['ships'][ship_id], self.pics['ships'][ship_id]['ship'])

        return ships

    def gen_sails(self, ax, im_ax, ships):
        """ax im_ax stuff not only in animate()"""

        for ship_id in ships:  # ships is a key-val dict

            _, _, file_names = os.walk(self.PATH_IMAGES + '/ships/' + ship_id).__next__()

            for file_name in file_names:
                name_split = file_name.split('_')
                if len(name_split) > 1 and name_split[1] == 's' and len(name_split) < 4 and \
                        file_name[:-4] in ships[ship_id].gi['xtras']:
                    sail = Sail(file_name[:-4],
                                self.pics['ships'][ship_id]['sails'][file_name[:-4]],
                                ships[ship_id])
                    # ships[ship_id].add_sail(sail)
                    ships[ship_id].sails[sail.id] = sail
        return ships

    def gen_smokas(self, ax, im_ax, ships, ch):
        """
        OBS difference to waves is that here one object is created
        ch needed to trigger when smoke to launch
        """
        for ship_id in ships:  # ships is a key-val dict

            for smoka_id, smoka_pic in self.pics['ships'][ship_id]['smokas'].items():

                smoka = Smoke(smoka_id, smoka_pic, ships[ship_id], ch, type='a')
                ships[ship_id].smokas[smoka.id] = smoka

        return ships

    def gen_smokrs(self, ax, im_ax, ships, ch, type='both'):
        """
        OBS difference to waves is that here one object is created
        ch needed to trigger when smoke to launch
        """
        for ship_id in ships:  # ships is a key-val dict

            for smokr_id, smokr_pic in self.pics['ships'][ship_id]['smokrs'].items():
                smokr = Smoke(smokr_id, smokr_pic, ships[ship_id], ch, type='r')
                ships[ship_id].smokrs[smokr.id] = smokr

        return ships

    def gen_expls(self, ax, im_ax, ships, ch):
        """
        Each ship gets multiple expls
        """
        for ship_id in ships:
            for expl_id, expl_pic in self.pics['ships'][ship_id]['expls'].items():
                expl = Expl(expl_id, expl_pic, ships[ship_id], ch)
                ships[ship_id].expls[expl.id] = expl

        return ships

    def gen_spls(self, ax, im_ax, ships, ch):

        for ship_id in ships:
            for spl_id, spl_pic in self.pics['ships'][ship_id]['spls'].items():
                spl = Spl(spl_id, spl_pic, ships[ship_id], ch)
                ships[ship_id].spls[spl.id] = spl

        return ships

    def gen_waves(self, ax, im_ax):
        waves = {}
        for wave_id, wave_pic in self.pics['waves'].items():
            wave = Wave(wave_id, self.pics['waves'][wave_id])
            waves[wave_id] = wave
        return waves
#
# def gen_layers(ax, FRAMES_START, FRAMES_STOP, chronicle):
#     waves = {}
#     spls = {}  # splashes
#     smokas = {}
#     smokrs = {}
#     ships = {}
#     im_ax = {}
#     explosions = {}
#     specials = {}
#
#     pics = load_pics()
#     ships_info = chronicle['ships']
#
#     im_ax['backgr'] = ax.imshow(pics['backgr'], zorder=1, alpha=1)
#
#     # im_ax['backgr'].set_extent([0, 200, 720, 0])
#
#     # lays['backgr'].extent = [0, pics['backgr'].shape[1], pics['backgr'].shape[0], 0]
#
#     scale_vector = generate_scaling(pics['backgr'])
#     control_extents(pics, ships_info, scale_vector)
#
#     # WAVES =================================
#     zorder = 3
#     for wave_id, wave_pic in pics['waves'].items():
#
#         found_coords = False
#         wave_id_s = wave_id.split('_')
#         while found_coords == False:
#             try:
#                 if P.MAP_SIZE == 'small':
#                     x = random.randint(0, pics['backgr'].shape[1] - wave_pic.shape[1] * 1)
#                     y = random.randint(int(pics['backgr'].shape[0] * 1 / 10), pics['backgr'].shape[0] - wave_pic.shape[0] * 2)
#                     tl = [x, y]
#                 else:
#                     tl = get_wave_tl(wave_id, wave_id_s, wave_pic)
#                 found_coords = True
#             except:
#                 print("failed to find coords1")
#
#         waves[wave_id] = layers.Wave(id=wave_id, tl=tl, pic=wave_pic, zorder=zorder,FRAMES_START=FRAMES_START,
#                                      FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector)
#         wave_ax = ax.imshow(wave_pic, zorder=zorder, alpha=1)
#         im_ax[wave_id] = wave_ax
#
#     # SPLASHES ================
#     zorder=14  # THESE ARE SET IN ANIMATION (maybe)
#     for spl_id, spl_pic in pics['spls'].items():
#         spls[spl_id] = layers.Splash(id=spl_id, zorder=zorder, tl=[0, 0], pic=spl_pic, scale_vector=scale_vector)
#         im_ax[spl_id] = ax.imshow(spl_pic, zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
#
#     # SMOKRS ====================
#     zorder = P.Z_SMOKR  # 5  THESE ARE SET IN ANIMATION
#     for smokr_id, smokr_pic in pics['smokrs'].items():
#         bc = False
#         if smokr_id.split("_")[1] == 'bc':
#             bc = True
#         smokrs[smokr_id] = layers.Smoke(id=smokr_id, zorder=zorder, tl=[0, 0], pic=pics['smokrs'][smokr_id],
#                                         scale_vector=scale_vector, s_type='r', left_right=None, bc=bc)  # set inside
#         im_ax[smokr_id] = ax.imshow(pics['smokrs'][smokr_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
#
#     # SMOKAS ========
#     zorder = P.Z_SMOKA
#     for smoka_id, smoka_pic in pics['smokas'].items():
#         smoka_ship_id = "ship_" + smoka_id.split("_")[1]
#         if smoka_ship_id not in ships_info:
#             continue
#
#         zorder = P.Z_SMOKA
#         smokas[smoka_id] = layers.Smoke(id=smoka_id, zorder=zorder, tl=[0, 0], pic=pics['smokas'][smoka_id],
#                                         scale_vector=scale_vector, s_type='a', left_right='r', bc=False)
#         smoka = ax.imshow(pics['smokas'][smoka_id], zorder=zorder, alpha=0., extent=[0, 1, 1, 0])
#         im_ax[smoka_id] = smoka
#
#     # SPECIALS =========
#     specials['smoka_left'] = layers.Smoke(id='smoka_left', zorder=6, tl=None, pic=pics['specials']['smoka_left'],
#                                           scale_vector=scale_vector, s_type='a', left_right='r', bc=True)
#     special = ax.imshow(pics['specials']['smoka_left'], zorder=6, alpha=0., extent=[0, 1, 1, 0])
#     im_ax['smoka_left'] = special
#
#     # EXPLOSIONS =================================
#     zorder = P.Z_EXPL
#     for expl_id, expl_pic in pics['expls'].items():
#         explosions[expl_id] = layers.LayerAbstract(id=expl_id, zorder=zorder, tl=None, pic=expl_pic, scale_vector=scale_vector)
#         im_ax[expl_id] = ax.imshow(pics['expls'][expl_id], zorder=zorder, alpha=0.9, extent=[0, 1, 1, 0])
#
#     # SHIPS ===================================
#     zorder = 6
#     for ship_id, ship_pic in pics['ships'].items():
#
#         if ship_id[-1] not in P.SHIPS_TO_SHOW:
#             continue
#         else:
#             zorder = ships_info[ship_id]["zorder"]
#
#         # SAILS CREATED BEFORE SHIP (BECAUSE Ship class does not take pics as input)
#         xtra_pics = {}  # for a specific ship (extra nesting needed)
#         for xid in ships_info[ship_id]['xtras']:  # objects created in Sail class
#             xtra_pics[xid] = pics['xtra'][xid]
#             sail_ax = ax.imshow(pics['xtra'][xid], zorder=P.Z_XTRA, alpha=0)
#             im_ax[xid] = sail_ax
#
#         ships[ship_id] = layers.Ship(id=ship_id, zorder=zorder, tl=ships_info[ship_id]['tl'], pic=ship_pic,
#                                      FRAMES_START=FRAMES_START, FRAMES_STOP=FRAMES_STOP, scale_vector=scale_vector,
#                                      xtra_pics=xtra_pics, ship_info=ships_info[ship_id], ship_ch=chronicle['ships'][ship_id])
#
#         init_val_bright = ships[ship_id].bright_start_array[P.FRAMES_START]
#         ship_pic = change_brightness(init_val_bright, ship_pic)
#         im_ax[ship_id] = ax.imshow(ship_pic, zorder=zorder, alpha=0.0)  #, extent=ships[ship_id].extent[0])
#         # im_ax[ship_id] = ax.imshow(ship_pic, zorder=zorder)  #, alpha=0.8, extent=ships[ship_id].extent[0])
#
#     return im_ax, waves, spls, smokas, smokrs, explosions, specials, ships, pics
#
#
# def get_wave_tl(wave_id, wave_id_s, wave_pic):
#
#     x_le = -400
#     x_ri = 100
#     y_up = -50
#     y_do = 50
#
#     if int(wave_id_s[1]) < 500:  # le
#         x_le = -int(wave_id_s[1])
#     if int(wave_id_s[1]) > 1000:  # ri
#         x_ri = 0
#     if int(wave_id_s[2]) > 590:  # do
#         y_do = 30
#     if wave_id == 'w_700_461' or wave_id == 'w_850_430':
#         y_up = 0
#     if wave_id == 'w_1000_500':
#         y_up = -20
#
#     x_r = random.randint(x_le, x_ri)  # random
#     y_r = random.randint(y_up, y_do)
#
#     le_boundary = random.randint(210, 270)
#
#     x = min(max(le_boundary, int(wave_id_s[1]) + x_r), 1280 - wave_pic.shape[1] * 2 + x_r)
#     y = min(max(0, int(wave_id_s[2]) + y_r), 720 - wave_pic.shape[0] * 2 + y_r)
#     tl = [x, y]
#     return tl

