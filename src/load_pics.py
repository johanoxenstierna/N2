import os
import P as P
from matplotlib.pyplot import imread

def load_pics(ch):
    """LOADS BGR
    ch needed to see if smoka_hardcoded is used """

    pics = {}
    pics['waves'] = {}
    # pics['spls'] = {}
    pics['ships'] = {}
    # pics['xtra'] = {}
    # pics['smokas'] = {}
    # pics['smokrs'] = {}
    # pics['expls'] = {}
    pics['specials'] = {}

    if P.MAP_SIZE == 'small':
        pics['backgr'] = imread('./images/raw/backgr_small0.png')  # 482, 187
    else:
        pics['backgr'] = imread('./images/raw/backgr.png')  # 482, 187
        # pics['frame'] = imread('./images/raw/frame_pic.png')



    # PATH = './images_mut/specials/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for file_name in file_names:
    #     pics['specials'][file_name[:-4]] = imread(PATH + file_name)  # without .png

    # UNIQUE PICTURES FOR A CERTAIN SHIP
    PATH = './images/processed/ships/'
    _, folder_names, _ = os.walk(PATH).__next__()
    for folder_name in folder_names:  # ships
        if folder_name not in ch['ships']:
            continue

        pics['ships'][folder_name] = {}
        pics['ships'][folder_name]['sails'] = {}
        pics['ships'][folder_name]['smokas'] = {}
        pics['ships'][folder_name]['smokrs'] = {}
        pics['ships'][folder_name]['expls'] = {}
        pics['ships'][folder_name]['spls'] = {}
        _, _, file_names = os.walk(PATH + '/' + folder_name).__next__()
        for file_name in file_names:

            name_split = file_name.split('_')
            if len(name_split) < 2:  # SHIP LOADED HERE
                pics['ships'][folder_name]['ship'] = imread(PATH + '/' + folder_name + '/' + file_name)  # without .png
            elif len(name_split) > 1 and name_split[1] == 's' and P.A_SAILS:
                # aa = imread(PATH + '/' + folder_name + '/' + file_name)
                pics['ships'][folder_name]['sails'][file_name[:-4]] = imread(PATH + '/' + folder_name + '/' + file_name)
            elif len(name_split) > 1 and len(name_split) < 4 and name_split[1] == 'a' and P.A_SMOKAS:

                # Only 1 copy of hardcoded smokas used
                aa = ch['ships'][folder_name]['smokas_hardcoded']['ids']
                if file_name[:-4] in ch['ships'][folder_name]['smokas_hardcoded']['ids']:
                    pics['ships'][folder_name]['smokas'][file_name[:-4]] = \
                        imread(PATH + '/' + folder_name + '/' + file_name)
                else:  # several copies
                    for i in range(P.NUM_SMOKAS):
                        # aa = imread(PATH + '/' + folder_name + '/' + file_name)
                        pics['ships'][folder_name]['smokas'][file_name[:-4] + '_' + str(i)] = \
                            imread(PATH + '/' + folder_name + '/' + file_name)

    PATH = './images/processed/waves/'
    _, _, file_names = os.walk(PATH).__next__()
    if P.A_WAVES:
        for file_name in file_names:
            for i in range(P.NUM_WAVES):  # OBS THIS IS NUM OF COPIES PER WAVE, NOT AGGREGATE
                # for file_name in file_names:
                #     if int(file_name.split('_')[1]) == i:
                pics['waves'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
                # break  # found wave
                # if P.MAP_SIZE == 'small' and file_name[5] == 's':
                # pics['waves'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png

                # elif P.MAP_SIZE != 'small' and file_name[5] != 's':
                #     pics['waves'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png


    # pics['ships']['ship_3'] = imread('./images_mut/ships/ship_3.png')  # 105, 145
    # pics['ships']['ship_1'] = imread('./images_mut/ships/ship_1.png')  # 105, 145
    # pics['explosions']['explosion_0'] = imread('./images_mut/expls/explosion_0.png')

    # COPIES OF THE SAME EXPLS ARE ADDED TO EACH SHIP
    PATH = './images/processed/expls/'
    _, _, file_names = os.walk(PATH).__next__()
    for file_name in file_names:
        pic = imread(PATH + file_name)
        for ship_id, ship in pics['ships'].items():
            for i in range(P.NUM_EXPLS):
                ship['expls'][file_name[:-4] + '_' + str(i)] = pic

    # COPIES OF THE SAME SPL ARE ADDED TO EACH SHIP
    PATH = './images/processed/spls/'
    _, _, file_names = os.walk(PATH).__next__()
    for file_name in file_names:
        pic = imread(PATH + file_name)
        for ship_id, ship in pics['ships'].items():
            for i in range(P.NUM_EXPLS):
                ship['spls'][file_name[:-4] + '_' + str(i)] = pic

    # COPIES OF THE SAME SMOKR ARE ADDED TO EACH SHIP
    PATH = './images/processed/smokrs/'
    _, _, file_names = os.walk(PATH).__next__()
    for file_name in file_names:
        pic = imread(PATH + file_name)
        for ship_id, ship in pics['ships'].items():
            for i in range(P.NUM_SMOKRS):
                ship['smokrs'][file_name[:-4] + '_' + str(i)] = pic

    aa = 5
    #
    # PATH = './images/processed/xtra/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for file_name in file_names:
    #     pics['xtra'][file_name[:-4]] = imread(PATH + file_name)  # without .png


    # pics['sails']['sail_3_0_20_68'] = imread('./images_mut/sails/sail_3_0_20_68.png')
    # pics['sails']['sail_3_1_53_79'] = imread('./images_mut/sails/sail_3_1_53_79.png')
    return pics