import os
from src import PARAMS as P
from matplotlib.pyplot import imread

def load_pics():

    pics = {}
    pics['waves'] = {}
    pics['spls'] = {}
    pics['ships'] = {}
    pics['xtra'] = {}
    pics['smokas'] = {}
    pics['smokrs'] = {}
    pics['expls'] = {}
    pics['specials'] = {}

    if P.MAP_SIZE == 'small':
        pics['backgr'] = imread('./images/raw/backgr_small0.png')  # 482, 187
    else:
        pics['backgr'] = imread('./images_raw/backgr_new1.png')  # 482, 187
        pics['frame'] = imread('./images_raw/frame_pic.png')
    PATH = './images_mut/waves/'

    # _, _, file_names = os.walk(PATH).__next__()
    # for i in range(PARAMS.NUM_WAVES):
    #     for file_name in file_names:
    #         if PARAMS.MAP_SIZE == 'small' and file_name[5] == 's':
    #             pics['waves'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
    #         elif PARAMS.MAP_SIZE != 'small' and file_name[5] != 's':
    #             pics['waves'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
    #
    # PATH = './images_mut/spls/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for i in range(PARAMS.NUM_SPLS):
    #     for file_name in file_names:
    #         pics['spls'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
    #
    # PATH = './images_mut/smokrs/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for i in range(PARAMS.NUM_SMOKRS):
    #     for file_name in file_names:
    #         pics['smokrs'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
    #
    # PATH = './images_mut/smokas/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for i in range(PARAMS.NUM_SMOKAS):
    #     for file_name in file_names:
    #         pics['smokas'][file_name[:-4] + '_' + str(i)] = imread(PATH + file_name)  # without .png
    #
    # PATH = './images_mut/specials/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for file_name in file_names:
    #     pics['specials'][file_name[:-4]] = imread(PATH + file_name)  # without .png

    PATH = './images/processed/ships/'
    _, _, file_names = os.walk(PATH).__next__()
    for file_name in file_names:
        pics['ships'][file_name[:-4]] = imread(PATH + file_name)  # without .png
    # pics['ships']['ship_3'] = imread('./images_mut/ships/ship_3.png')  # 105, 145
    # pics['ships']['ship_1'] = imread('./images_mut/ships/ship_1.png')  # 105, 145
    # pics['explosions']['explosion_0'] = imread('./images_mut/expls/explosion_0.png')

    # PATH = './images_mut/expls/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for file_name in file_names:
    #     pics['expls'][file_name[:-4]] = imread(PATH + file_name)  # without .png
    #
    # PATH = './images_mut/xtra/'
    # _, _, file_names = os.walk(PATH).__next__()
    # for file_name in file_names:
    #     pics['xtra'][file_name[:-4]] = imread(PATH + file_name)  # without .png


    # pics['sails']['sail_3_0_20_68'] = imread('./images_mut/sails/sail_3_0_20_68.png')
    # pics['sails']['sail_3_1_53_79'] = imread('./images_mut/sails/sail_3_1_53_79.png')
    return pics