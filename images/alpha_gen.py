# TODO: Stray white pixels over areas where some movement is desired.

import os
import numpy as np
from matplotlib.pyplot import imread, imsave
from PIL import Image

THRESHOLD_SHIP_EXPL = 0.99
THRESHOLD_R = 0.92
THRESHOLD_G = 0.98
THRESHOLD_B = 0.98

# os.remove(<file name>)
# image_names = os.listdir('images_orig')
_, folder_names, _ = os.walk('./images/raw').__next__()

for folder_name in folder_names:
    _, _, file_names = os.walk('./images/raw/' + folder_name).__next__()
    for file_name in file_names:
        pic = imread('./images/raw/' + folder_name + '/' + file_name)
        if pic.shape[2] == 3:  # if no alpha layer -> create it
            alpha_ = np.full((pic.shape[0], pic.shape[1]), 1)
            pic = np.dstack((pic, alpha_))

        if file_name[0:4] == 'ship' or file_name[0:4] == 'expl':
            threshold_r = THRESHOLD_SHIP_EXPL
            threshold_g = THRESHOLD_SHIP_EXPL
            threshold_b = THRESHOLD_SHIP_EXPL
        else:
            threshold_r = THRESHOLD_R
            threshold_g = THRESHOLD_G
            threshold_b = THRESHOLD_B

        array_binary_r = np.where(pic[:, :, 0] > threshold_r, 0.0, 1)  # where alpha should be 1, and 0 otherwise
        array_binary_g = np.where(pic[:, :, 1] > threshold_g, 0.0, 1)  # where alpha should be 1, and 0 otherwise
        array_binary_b = np.where(pic[:, :, 2] > threshold_b, 0.0, 1)  # where alpha should be 1, and 0 otherwise
        # prod = array_binary_r * array_binary_g * array_binary_b

        if file_name[0:4] == 'expl':
            prod = array_binary_b
        else:
            prod = array_binary_g * array_binary_b
        pic[:, :, 3] = np.multiply(prod, np.ones_like(pic[:, :, 2]))  # alpha set to 0 in correct places

        imsave('./images/processed/' + folder_name + '/' + file_name, pic)

    print("done folder " + str(folder_name))

