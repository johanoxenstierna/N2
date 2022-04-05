# TODO: Stray white pixels over areas where some movement is desired. (?)
"""OBS the default """

import os
import numpy as np
from matplotlib.pyplot import imread, imsave
from PIL import Image
from copy import deepcopy
import cv2
from skimage.morphology import medial_axis, skeletonize
from src.trig_functions import *
from sklearn.preprocessing import StandardScaler

THRESHOLD_SHIP_EXPL = 0.99
# THRESHOLD_B = 0.999  # 0.98
# THRESHOLD_G = 0.999  # 0.98
# THRESHOLD_R = 0.9999  # 0.92


def process_alpha(pic_in, file_name):
    """RGB!!! """

    THRESHOLD_R = 0.98
    THRESHOLD_B = 0.92
    THRESHOLD_G = 0.98


    if file_name.split('.')[0] in ['0', '1', '2', '3', '4', '5', '6', '7', '0',]:  # ships (not as strict).
        THRESHOLD_R = 0.5
        THRESHOLD_B = 0.5
        THRESHOLD_G = 0.5


    save_status = 1  # 0: don't save, 1: save right now

    if pic_in.shape[2] == 3:  # if no alpha layer -> create it
        alpha_ = np.full((pic_in.shape[0], pic_in.shape[1]), 1)
        pic_in = np.dstack((pic_in, alpha_))

    pic = pic_in.copy()

    alpha_r = np.where(pic_in[:, :, 2] > THRESHOLD_R, 0.0, 1)  # where alpha should be 1, and 0 otherwise
    alpha_b = np.where(pic_in[:, :, 0] > THRESHOLD_B, 0.0, 1)  # alpha should be 0 wherever things are too white
    alpha_g = np.where(pic_in[:, :, 1] > THRESHOLD_G, 0.0, 1)  # if it's too bright make it 0, 1 otherwise


    if file_name[0:4] == 'expl':  # this may be unmaintainable
        prod = alpha_r  # because expl is really white to start with
    else:
        prod = alpha_g * alpha_b * alpha_r  # this sets more frames to 0.0

    pic[:, :, 3] = np.multiply(prod, np.ones_like(pic_in[:, :, 2]))  # alpha set to 0 in correct places

    # # Since background is white and black is desired, convert (OBS blue layer doesn't work for expls see below)
    for i in range(0, 3):
        white_mask = np.where(pic[:, :, i] > 0.9999999, 0.0, 1.0)
        pic[:, :, i] = pic[:, :, i] * white_mask

    if file_name[0:4] == 'expl':  # needed since the blue layer is totally useless and messes up in the above loop
        pic[:, :, 0] = alpha_r

    return pic, save_status


def load_mask(file_names, mask_name_to_search, mask_full_path):
    flag_mask = False
    mask = None
    if mask_name_to_search in file_names:
        # mask = imread('./images/raw/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name_mask)
        mask = imread('./images/raw/' + mask_full_path)
        flag_mask = True
    else:
        print("image does not have mask: " + file_name)
        flag_mask = False
    # try:
    #     mask = imread('./images/raw/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name_mask)
    #     flag_mask = True
    # except:
    #     print("image does not have mask: " + file_name)
    #     flag_mask = False
        # imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)
        # continue
    return mask, flag_mask


def process_mask(pic, file_name, file_name_split, NUM_GEN_CONTOURS):
    """
    file_name (for debugging)
    OBS as soon as it hits inner contour procedure stops
    """
    mid_point_rc = [pic.shape[0] / 2, pic.shape[1] / 2]  # TODO use marked point on mask instead

    img_grey = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
    thresh = 0.01

    ret, thresh_pic = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY_INV)
    thresh_pic = thresh_pic.astype(np.uint8)
    a = np.where(thresh_pic == 255)
    b = np.where(thresh_pic == 0)
    thresh_pic[a] = 0
    thresh_pic[b] = 255
    contours, hierarchy = cv2.findContours(thresh_pic, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_TC89_L1)

    # NUM_CONTOURS_BEG = 1  # always
    contour_lens = [len(x) for x in contours]
    contour_i_inner = np.argmin(contour_lens)
    contour_i_outer = np.argmax(contour_lens)
    if len(contours[contour_i_outer]) < len(contours[contour_i_inner]):
        raise Exception("bad contour thing:  file_name: " + str(file_name))
    contours = [contours[contour_i_outer]]
    contour_i_outer = 0

    d = 0
    # NUM_GEN_CONTOURS = 1
    NUM_TOTAL_CONTOURS = NUM_GEN_CONTOURS + 1

    for _ in range(NUM_GEN_CONTOURS):  # LOOP THROUGH OUTER CONTOURS ONLY
        d += 0.2  # distance between contours (more d, more aggressive alpha removal)
        contour_new = []
        # perc_dist_to_mid_cont += 0.02
        for i in range(1, len(contours[contour_i_outer]) - 1):

            point_prev = contours[contour_i_outer][i - 1][0]
            point_this = contours[contour_i_outer][i][0]
            point_next = contours[contour_i_outer][i + 1][0]

            # point_prev = [5, 10]
            # point_this = [9, 8]
            # point_next = [11, 4]

            # point_prev = [4, 1]
            # point_this = [7, 2]
            # point_next = [8, 4]

            # point_prev = [8, 3]
            # point_this = [4, 2]
            # point_next = [3, 9]

            # point_prev = [9, 2]
            # point_this = [6, 4]
            # point_next = [3, 2]

            # point_prev = [7, 6]
            # point_this = [9, 4]
            # point_next = [4, 3]

            # point_prev = [3, 6]
            # point_this = [4, 4]
            # point_next = [3, 2]

            dx = point_prev[0] - point_next[0]
            dy = -(point_prev[1] - point_next[1])
            if dx == 0 or dy == 0:
                if dx == 0:
                    point_new0 = [point_this[0] + d, point_this[1]]
                    point_new1 = [point_this[0] - d, point_this[1]]
                if dy == 0:
                    point_new0 = [point_this[0], point_this[1] - d]
                    point_new1 = [point_this[0], point_this[1] + d]
            else:
                grad_orthogonal = - 1 / (dy / dx)  # normal gradient is dy/dx
                x_new = d * (1 / np.sqrt(1 + (np.tan(grad_orthogonal)**2)))
                y_new = d * (np.tan(grad_orthogonal) / np.sqrt(1 + (np.tan(grad_orthogonal)**2)))
                assert(np.sqrt(x_new**2 + y_new**2) - d < 0.001)
                point_new0 = [point_this[0] + x_new, point_this[1] - y_new]
                point_new1 = [point_this[0] - x_new, point_this[1] + y_new]

            dist_origin_0 = np.sqrt((point_new0[0] - mid_point_rc[0])**2 + (point_new0[1] - mid_point_rc[1])**2)
            dist_origin_1 = np.sqrt((point_new1[0] - mid_point_rc[0])**2 + (point_new1[1] - mid_point_rc[1])**2)
            if dist_origin_0 < dist_origin_1:
                point_new = point_new0
            else:
                point_new = point_new1

            # dist_origin_this_perc = [dist_origin_this[0] * perc_dist_to_mid_cont, dist_origin_this[1] * perc_dist_to_mid_cont]
            # point_new = [int(point_this[0] - dist_origin_this_perc[0]), int(point_this[1] - dist_origin_this_perc[1])]

            # if abs(point_new[0] - point_this[0]) > 140 or abs(point_new[1] - point_this[1]) > 140:
            #     raise Exception("distance between new point and this point seems large")

            contour_new.append([point_new])

        contours.append(np.asarray(contour_new, dtype=np.int32))

    # X = np.arange(0, NUM_TOTAL_CONTOURS)
    # alpha = np.ones(X.shape)  # no sigmoid
    # alpha = np.linspace(0.3, 1, num=NUM_TOTAL_CONTOURS)
    # alpha = np.asarray([sigmoid(x, grad_magn_inv=NUM_TOTAL_CONTOURS//6, x_shift=NUM_TOTAL_CONTOURS//3.6, y_magn=1, y_shift=0.0) for x in X])
    mask_outputs = []

    '''
    This creates several masks and each mask moves closer to the centroid of the pic
    '''
    for i in range(NUM_TOTAL_CONTOURS):
        mask_output0 = np.zeros(pic[:, :, 3].shape)
        cont = contours[i]
        for row in range(mask_output0.shape[0]):
            for col in range(mask_output0.shape[1]):
                dist = cv2.pointPolygonTest(cont, (col, row), True)  # neg dist=outside, pos=inside
                if dist < 0:
                    dist = 0
                # else:
                #     dist += 10
                mask_output0[row, col] = dist
        mask_outputs.append(mask_output0)

    # mask_output0 = min_max_normalization(mask_output0, [0.0, 1.0])

    mask_output = sum(mask_outputs)
    min_max_range = [0.2, 1.0]
    if file_name_split[1] == 'a':
        min_max_range = [0.1, 1.0]
    mask_output = min_max_normalization(mask_output, min_max_range)
    mask_output = cv2.GaussianBlur(mask_output, (7, 7), sigmaX=5, sigmaY=5)
    pic[:, :, 3] = pic[:, :, 3] * mask_output  # the multiplication makes sure that anything that should be zero is

    # # # # # # DRAW CONTOUR (debugger) ===================
    # image_copy = pic.copy()
    # cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1,
    #              lineType=cv2.LINE_AA)
    # # cv2.drawContours(image=image_copy, contours=contours, contourIdx=3, color=(0, 255, 255), thickness=2,
    # #                  lineType=cv2.LINE_AA)
    # cv2.imshow('None approximation', image_copy)  # use with debugger
    # # cv2.imshow('None approximation', mask_inner)  # use with debugger

    adf = 5


# os.remove(<file name>)
# image_names = os.listdir('images_orig')
_, folder_names_outer, _ = os.walk('./images/raw').__next__()

for folder_name_outer in folder_names_outer:

    if folder_name_outer == 'waves':
        adf = 5

    _, folder_names_inner, file_names_inner = os.walk('./images/raw/' + folder_name_outer).__next__()

    file_names = file_names_inner
    if len(folder_names_inner) > 0:  # SHIPS (they are nested) overwrites file names SAILS
        for folder_name_inner in folder_names_inner:
            _, _, file_names = os.walk('./images/raw/' + folder_name_outer + '/' + folder_name_inner).__next__()

            if folder_name_inner == '7':
                adf = 5

            for file_name in file_names:

                file_name_split = file_name.split('_')

                if len(file_name_split) > 3:
                    continue
                if file_name == '7_s_1.png':
                    aa = 5
                pic_in = imread('./images/raw/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name)
                pic, save_status = process_alpha(pic_in, file_name)

                # if file_name == '7_s_1.png':   # TEMP
                if len(file_name_split) > 2:  # the alpha masking is only applied for smokes and sails and waves
                    if file_name_split[1] == 's':   # TEMP
                        process_mask(pic, file_name, file_name_split, NUM_GEN_CONTOURS=5)
                    elif file_name_split[1] == 'a':
                        process_mask(pic, file_name, file_name_split, NUM_GEN_CONTOURS=1)
                imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)

    else:  # WAVES, EXPLS, SPLS (not nested)
        for file_name in file_names_inner:

            file_name_split = file_name.split('_')
            if file_name == 'w_0_369_272.png':
                adf = 5
            # if 'm.png' in file_name_split:
            #     continue  # masks are loaded separately below
            pic_in = imread('./images/raw/' + folder_name_outer + '/' + file_name)
            pic, save_status = process_alpha(pic_in, file_name)
            # if len(file_name_split) < 3:
            #     continue
            # mask_name_to_search = file_name_split[0] + '_' + file_name_split[1] + '_' + file_name_split[2][
            #     0] + '_m.png'
            # # mask, flag_mask = check_if_mask_exists(
            # #     file_name_split[0] + '_' + file_name_split[1] + '_' + file_name_split[2][
            # #         0] + '_m.png')
            # mask_full_path = folder_name_outer + '/' + mask_name_to_search
            # mask, flag_mask = load_mask(file_names_inner, mask_name_to_search, mask_full_path)
            #
            # if flag_mask == False:
            imsave('./images/processed/' + folder_name_outer + '/' + file_name, pic)
            # else:
            #     raise Exception("Maybe won't use this")
            #     process_mask(pic, mask)
            #     imsave('./images/processed/' + folder_name_outer + '/' + file_name, pic)

    print("done folder " + str(folder_name_outer))


# BACKUP from script
# if len(file_name_split) < 2:
                #     imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)
                #     continue

                # mask_name_to_search = file_name_split[0] + '_' + file_name_split[1] + '_' + file_name_split[2][
                #         0] + '_m.png'
                # mask_full_path = folder_name_outer + '/' + folder_name_inner + '/' + mask_name_to_search
                # mask, flag_mask = load_mask(file_names, mask_name_to_search, mask_full_path)

                # if flag_mask == False:
                #     imsave('./images/processed/' + folder_name_outer + '/' + folder_name_inner + '/' + file_name, pic)
                # else:
# def BACKUP_process_mask(pic, mask, file_name):  # March 14
#     """
#     file_name (for debugging)
#     OBS as soon as it hits inner contour procedure stops
#     """
#     mid_point_rc = [pic.shape[0] / 2, pic.shape[1] / 2]  # TODO use marked point on mask instead
#
#     # img_grey_mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
#     img_grey = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
#     # set a thresh
#     thresh = 0.01
#     # get threshold image
#
#     # ret, thresh_mask = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY_INV)
#     ret, thresh_pic = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY_INV)
#     thresh_pic = thresh_pic.astype(np.uint8)
#     a = np.where(thresh_pic == 255)
#     b = np.where(thresh_pic == 0)
#     thresh_pic[a] = 0
#     thresh_pic[b] = 255
#
#     # # thresh_img = np.float32(thresh_img)
#     # # find contours
#     # # contours, hierarchy = cv2.findContours(thresh_img, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
#     #
#     # # # skeleton = medial_axis(thresh_img).astype(np.uint8)
#     skeleton = skeletonize(thresh_pic.astype(bool))
#     skeleton_mask = skeleton.astype(np.uint8)
#     contours, hierarchy = cv2.findContours(thresh_pic, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_TC89_L1)
#
#     # NUM_CONTOURS_BEG = 1  # always
#     contour_lens = [len(x) for x in contours]
#     contour_i_inner = np.argmin(contour_lens)
#     contour_i_outer = np.argmax(contour_lens)
#     if len(contours[contour_i_outer]) < len(contours[contour_i_inner]):
#         raise Exception("bad contour thing:  file_name: " + str(file_name))
#     contours = [contours[contour_i_outer]]
#     contour_i_outer = 0
#     # mask2, _ = process_alpha(mask, file_name)
#
#     mask_temp = np.zeros(pic.shape)
#     # hull_inner = cv2.convexHull(contours[contour_i_inner])
#     # mask_inner = cv2.fillPoly(mask_temp.copy(), pts=[hull_inner], color=(0, 0, 0, 1.0))
#     # mask_inner = mask_inner * pic
#
#     d = 0  # pixels
#     perc_dist_to_mid_cont = 0.0
#     NUM_GEN_CONTOURS = 1
#     NUM_TOTAL_CONTOURS = NUM_GEN_CONTOURS + 1
#
#     for _ in range(NUM_GEN_CONTOURS):  # LOOP THROUGH OUTER CONTOURS ONLY
#         d += 10
#         contour_new = []
#         perc_dist_to_mid_cont += 0.02
#         for i in range(1, len(contours[contour_i_outer]) - 1):
#
#             point_prev = contours[contour_i_outer][i - 1][0]
#             point_this = contours[contour_i_outer][i][0]
#             point_next = contours[contour_i_outer][i + 1][0]
#
#             # point_prev = [5, 10]
#             # point_this = [9, 8]
#             # point_next = [11, 4]
#
#             # point_prev = [4, 1]
#             # point_this = [7, 2]
#             # point_next = [8, 4]
#
#             # point_prev = [8, 3]
#             # point_this = [4, 2]
#             # point_next = [3, 9]
#
#             # point_prev = [9, 2]
#             # point_this = [6, 4]
#             # point_next = [3, 2]
#
#             # point_prev = [7, 6]
#             # point_this = [9, 4]
#             # point_next = [4, 3]
#
#             # point_prev = [3, 6]
#             # point_this = [4, 4]
#             # point_next = [3, 2]
#
#             dx = point_prev[0] - point_next[0]
#             dy = -(point_prev[1] - point_next[1])
#             if dx == 0 or dy == 0:
#                 if dx == 0:
#                     point_new0 = [point_this[0] + d, point_this[1]]
#                     point_new1 = [point_this[0] - d, point_this[1]]
#                 if dy == 0:
#                     point_new0 = [point_this[0], point_this[1] - d]
#                     point_new1 = [point_this[0], point_this[1] + d]
#             else:
#                 grad_orthogonal = - 1 / (dy / dx)  # normal gradient is dy/dx
#                 x_new = d * (1 / np.sqrt(1 + (np.tan(grad_orthogonal)**2)))
#                 y_new = d * (np.tan(grad_orthogonal) / np.sqrt(1 + (np.tan(grad_orthogonal)**2)))
#                 assert(np.sqrt(x_new**2 + y_new**2) - d < 0.001)
#                 point_new0 = [point_this[0] + x_new, point_this[1] - y_new]
#                 point_new1 = [point_this[0] - x_new, point_this[1] + y_new]
#
#             dist_origin_0 = np.sqrt((point_new0[0] - mid_point_rc[0])**2 + (point_new0[1] - mid_point_rc[1])**2)
#             dist_origin_1 = np.sqrt((point_new1[0] - mid_point_rc[0])**2 + (point_new1[1] - mid_point_rc[1])**2)
#             if dist_origin_0 < dist_origin_1:
#                 point_new = point_new0
#             else:
#                 point_new = point_new1
#
#             # dist_origin_this_perc = [dist_origin_this[0] * perc_dist_to_mid_cont, dist_origin_this[1] * perc_dist_to_mid_cont]
#             # point_new = [int(point_this[0] - dist_origin_this_perc[0]), int(point_this[1] - dist_origin_this_perc[1])]
#
#             # if abs(point_new[0] - point_this[0]) > 140 or abs(point_new[1] - point_this[1]) > 140:
#             #     raise Exception("distance between new point and this point seems large")
#
#             contour_new.append([point_new])
#
#         contours.append(np.asarray(contour_new, dtype=np.int32))
#
#
#     # X = np.arange(0, NUM_TOTAL_CONTOURS)
#     # alpha = np.ones(X.shape)  # no sigmoid
#     # alpha = np.linspace(0.3, 1, num=NUM_TOTAL_CONTOURS)
#     # alpha = np.asarray([sigmoid(x, grad_magn_inv=NUM_TOTAL_CONTOURS//6, x_shift=NUM_TOTAL_CONTOURS//3.6, y_magn=1, y_shift=0.0) for x in X])
#
#     mask_output0 = np.zeros(pic[:, :, 3].shape)
#     cont = contours[0]
#     for row in range(mask_output0.shape[0]):
#         for col in range(mask_output0.shape[1]):
#             dist = cv2.pointPolygonTest(cont, (col, row), True)  # neg dist=outside, pos=inside
#             if dist < 0:
#                 dist = 0
#             else:
#                 dist += 100
#             mask_output0[row, col] = dist
#
#     mask_output0 = min_max_normalization(mask_output0, [0.0, 0.3])
#
#     # mask_output1 = np.zeros(pic[:, :, 3].shape)
#     # cont = contours[1]
#     # for row in range(mask_output1.shape[0]):
#     #     for col in range(mask_output1.shape[1]):
#     #         dist = cv2.pointPolygonTest(cont, (col, row), True)  # neg dist=outside, pos=inside
#     #         if dist < 0:
#     #             dist = 0
#     #         else:
#     #             dist = dist + 100
#     #         mask_output1[row, col] = dist
#     #
#     # mask_output1 = min_max_normalization(mask_output1, [0.0, 60.8])
#     #
#     # mask_output = mask_output0 + mask_output1
#     mask_output = min_max_normalization(mask_output0, [0, 1.0])
#
#     aa = 5
#     # for i in range(0, 1 + NUM_GEN_CONTOURS):  # 2 because no action taken for i == contour_i_inner
#     #     # if i == contour_i_inner:
#     #     #     continue
#     #     hull_outer = cv2.convexHull(contours[i])
#     #     mask_outer = cv2.fillPoly(mask_output.copy(), pts=[hull_outer], color=(0, 0, 0, alpha[i]))
#     #
#     #     aa = cv2.pointPolygonTest(contours[i], (28, 2), True)
#     #     gf = 5
#     #     #
#     #
#     #     # aa = mask_outer[:, :, 3] * pic[:, :, 3]
#     #     # mask_outer[:, :, 3] = aa
#     #     mask_output[:, :, 3] = mask_outer[:, :, 3]
#     #     aa = 5
#
#     # inner_visibility = np.where(mask_inner[:, :, 3] > 0.01)
#     # mask_output[inner_visibility] = 1.0
#
#     # pic[:, :, 3] = mask_output[:, :, 3]
#     pic[:, :, 3] = mask_output
#
#     # # # # # DRAW CONTOUR (debugger) ===================
#     # image_copy = pic.copy()
#     # cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1,
#     #              lineType=cv2.LINE_AA)
#     # # cv2.drawContours(image=image_copy, contours=contours, contourIdx=3, color=(0, 255, 255), thickness=2,
#     # #                  lineType=cv2.LINE_AA)
#     # cv2.imshow('None approximation', image_copy)  # use with debugger
#     # # cv2.imshow('None approximation', mask_inner)  # use with debugger
#
#     adf = 5




# def old_process_mask(pic, mask):
#     mid_point_rc = [pic.shape[0] / 2, pic.shape[1] / 2]  # TODO use marked point on mask instead
#
#     # min and max needed ===========
#     dist_min = 9999
#     dist_max = 0
#     for i in range(pic.shape[0]):
#         for j in range(pic.shape[1]):
#             try:
#                 if mask[i, j, 0] < 0.001 and pic[
#                     i, j, 3] > 0.999:  # the mask area is black and alpha is 1.
#
#                     # HERE NEED TO PROVIDE NUMBER OF PIXELS WITH WHICH TO DO 0-1
#                     dist_y = i - mid_point_rc[0]
#                     dist_x = j - mid_point_rc[1]
#                     dist = np.sqrt(dist_y ** 2 + dist_x ** 2)
#                     if dist < dist_min:
#                         dist_min = dist
#                     elif dist >= dist_max:
#                         dist_max = dist
#             except:
#                 adf = 5
#
#                 # adsf = 5
#
#     dist_min = min(dist_max, dist_min + 0.0 * dist_min)  # so that the 1's will stretch further
#     alpha_spread_xs = np.arange(dist_min, dist_max + 1, 1, dtype=int)
#     alpha_spread_ys = np.linspace(1, 0, len(alpha_spread_xs))  # alpha largest for smallest dists
#
#     for i in range(pic.shape[0]):
#         for j in range(pic.shape[1]):
#             if mask[i, j, 0] < 0.001 and pic[i, j, 3] > 0.999:  # the mask area is black and alpha is 1.
#                 dist_y = i - mid_point_rc[0]
#                 dist_x = j - mid_point_rc[1]
#                 dist = int(np.sqrt(dist_y ** 2 + dist_x ** 2))
#                 if dist < dist_min:
#                     pic[i, j, 3] = 1.0
#                 else:
#                     alpha_spread_x_i = np.where(alpha_spread_xs == dist)[0][0]
#                     alpha_spread_y = alpha_spread_ys[alpha_spread_x_i]
#                     pic[i, j, 3] = alpha_spread_y

