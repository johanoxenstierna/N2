# TODO: Stray white pixels over areas where some movement is desired. (?)
"""OBS the default """

import os
import numpy as np
from matplotlib.pyplot import imread, imsave
from PIL import Image
from copy import deepcopy

THRESHOLD_SHIP_EXPL = 0.99
THRESHOLD_R = 0.92
THRESHOLD_G = 0.98
THRESHOLD_B = 0.98

# os.remove(<file name>)
# image_names = os.listdir('images_orig')
_, folder_names_outer, _ = os.walk('./images/raw').__next__()

for folder_name_outer in folder_names_outer:
    _, folder_names_inner, _ = os.walk('./images/raw/' + folder_name_outer).__next__()
    for folder_name_inner in folder_names_inner:
        _, _, file_names = os.walk('./images/raw/' + folder_name_outer + '/' + folder_name_inner).__next__()
        for file_name in file_names:

            file_name_split = file_name.split('_')
            if 'm.png' in file_name_split:
                continue  # masks are loaded separately below
            pic_in = imread('./images/raw/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name)

            if pic_in.shape[2] == 3:  # if no alpha layer -> create it
                alpha_ = np.full((pic_in.shape[0], pic_in.shape[1]), 1)
                pic_in = np.dstack((pic_in, alpha_))

            pic = pic_in.copy()

            threshold_r = THRESHOLD_R
            threshold_g = THRESHOLD_G
            threshold_b = THRESHOLD_B

            alpha_r = np.where(pic_in[:, :, 0] > threshold_r, 0.0, 1)  # where alpha should be 1, and 0 otherwise
            alpha_g = np.where(pic_in[:, :, 1] > threshold_g, 0.0, 1)  # if it's too bright make it 0, 1 otherwise
            alpha_b = np.where(pic_in[:, :, 2] > threshold_b, 0.0, 1)  # where alpha should be 1, and 0 otherwise
            # prod = array_binary_r * array_binary_g * array_binary_b

            if file_name[0:4] == 'expl':
                prod = alpha_b
            else:
                prod = alpha_g * alpha_b

            pic[:, :, 3] = np.multiply(prod, np.ones_like(pic_in[:, :, 2]))  # alpha set to 0 in correct places

            # Since background is white and black is desired, convert
            for i in range(3):
                white_mask = np.where(pic[:, :, i] > 0.9999, 0.0, 1.0)
                pic[:, :, i] = pic[:, :, i] * white_mask

            # IF THE IMAGE HAS AN ALPHA MASK GEN SCALE FOR ALPHA AT BORDER ======================================
            mask = None
            try:
                file_name_mask = file_name_split[0] + '_' + file_name_split[1] + '_' + file_name_split[2][0] + '_m.png'
                mask = imread('./images/raw/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name_mask)
            except:
                print("image does not have mask: " + file_name)
                imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)
                # file_name_mask = None
                continue

            mid_point_rc = [pic.shape[0] / 2, pic.shape[1] / 2]  # maybe use mask here

            # min and max needed ===========
            dist_min = 9999
            dist_max = 0
            for i in range(pic.shape[0]):
                for j in range(pic.shape[1]):
                    try:
                        if mask[i, j, 0] < 0.001 and pic[i, j, 3] > 0.999: # the mask area is black and alpha is 1.

                            # HERE NEED TO PROVIDE NUMBER OF PIXELS WITH WHICH TO DO 0-1
                            dist_y = i - mid_point_rc[0]
                            dist_x = j - mid_point_rc[1]
                            dist = np.sqrt(dist_y**2 + dist_x**2)
                            if dist < dist_min:
                                dist_min = dist
                            elif dist >= dist_max:
                                dist_max = dist
                    except:
                        adf = 5

                        # adsf = 5

            dist_min = min(dist_max, dist_min + 0.0 * dist_min)  # so that the 1's will stretch further
            alpha_spread_xs = np.arange(dist_min, dist_max + 1, 1, dtype=int)
            alpha_spread_ys = np.linspace(1, 0, len(alpha_spread_xs))  # alpha largest for smallest dists

            for i in range(pic.shape[0]):
                for j in range(pic.shape[1]):
                    if mask[i, j, 0] < 0.001 and pic[i, j, 3] > 0.999:  # the mask area is black and alpha is 1.
                        dist_y = i - mid_point_rc[0]
                        dist_x = j - mid_point_rc[1]
                        dist = int(np.sqrt(dist_y ** 2 + dist_x ** 2))
                        if dist < dist_min:
                            pic[i, j, 3] = 1.0
                        else:
                            alpha_spread_x_i = np.where(alpha_spread_xs == dist)[0][0]
                            alpha_spread_y = alpha_spread_ys[alpha_spread_x_i]
                            pic[i, j, 3] = alpha_spread_y

            imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)

    print("done folder " + str(folder_name_outer))

