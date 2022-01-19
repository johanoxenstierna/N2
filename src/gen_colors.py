
import cv2
import matplotlib
import numpy as np
import time

def gen_colors(pic):
    """
    pic is temp.
    This will prob be specific for each layer
    Either returns a mvn function to be applied in the animation loop
    or 2D tensor through time (expensive)
    """

    # LATER ===
    # hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)  # MIGHT BE RGB

    # hsv = matplotlib.colors.rgb_to_hsv(pic[:, :, 0:3])  # MIGHT BE RGB
    # h, s, v = cv2.split(hsv)  # s=0 means grayscale, v=1 white, v=0 dark.
    # pic[:, :, 0:3] = matplotlib.colors.hsv_to_rgb(hsv)

    # constants
    num_cycles_x = 5
    num_cycles_y = 4

    # variables
    y_shear = 0.2  # -1 < y_shear < 1  # neg means to left, pos means to right
    # x_shear = 0.001   # -1 < x_shear < 1  # neg means to left, pos means to right

    x_ver = np.linspace(np.zeros((pic.shape[1])), np.full((pic.shape[1]), fill_value=num_cycles_x * (2 * np.pi)),
                        num=pic.shape[0], axis=0)
    x_hor = np.linspace(np.zeros((pic.shape[0])), np.full((pic.shape[0]), fill_value=num_cycles_y * (2 * np.pi)),
                        num=pic.shape[1], axis=1)

    # x_hor = x_hor + 0.5 * np.pi
    # y_ver = (np.sin(x_ver) + 1) / 2
    y_ver = np.zeros((pic.shape[0], pic.shape[1]))
    y_hor = np.zeros((pic.shape[0], pic.shape[1]))
    for i in range(pic.shape[0]):
        y_ver[i, :] = (np.sin(x_hor[i, :] + i*y_shear) + 1) / 2
        y_hor[i, :] = (np.sin(x_hor[i, :] + i*y_shear) + 1) / 2

    # y = y_ver #* y_hor
    # pic[:, :, 0] = pic[:, :, 0] * y
    # pic[:, :, 1] = pic[:, :, 1] * y
    # pic[:, :, 2] = pic[:, :, 2] * y

    fg = 5

    # v += value
    # final_hsv = cv2.merge((h, s, v))
    # img2 = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    # img[:, :, 0:3] = img2
    #
    # # think this is just the operation to sort out alpha
    # idx0 = np.argwhere(img[:, :, 0:3] < 0.0)
    # idx1 = np.argwhere(img[:, :, 0:3] > 1.0)
    #
    # for row, col, ch in idx0:
    #     img[row, col, ch] = 0.0
    #
    # for row, col, ch in idx1:
    #     img[row, col, ch] = 1.0

    return pic