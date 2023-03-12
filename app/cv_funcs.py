import cv2
import numpy as np
import matplotlib.pyplot as plt

import math
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

threshold_values = {}
h = [1]

OUTPUT_SIZE = (564, 400)


def process_img(img):
    # Get the dimensions of the image
    height, width = img.shape[:2]

    # Crop the top 25% of the image
    crop_height = int(height * 0.35)
    img = img[crop_height:height, 0:width]

    print('Dimensions', height, width)

    img = cv2.resize(img, OUTPUT_SIZE)

    img = custom_thresholding(img)

    # Display the cropped image
    # cv2.imshow('Cropped Image', img)
    # cv2.imshow('Cropped Image', img.astype(np.float32))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return img


def custom_thresholding(img):
    red_mask = np.where(img[:, :, 0] > 200, 1, 0)
    blue_mask = np.where(img[:, :, 1] > 200, 1, 0)
    green_mask = np.where(img[:, :, 2] > 200, 1, 0)
    bin_img = np.logical_or.reduce((red_mask, blue_mask, green_mask))
    return bin_img


def transform(img):
    # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    red_mask = np.where(img[:, :, 0] > 200, 255, 0)
    blue_mask = np.where(img[:, :, 1] > 200, 255, 0)
    green_mask = np.where(img[:, :, 2] > 200, 255, 0)

    new_img = np.logical_or.reduce((red_mask, blue_mask, green_mask))
    return new_img


def init_window(img, frame):
    max_window_width = 1080
    max_window_height = 1080
    img_wind = frame
    img_h, img_w = img.shape[:2]
    scale_width = max_window_width / img_w
    scale_height = max_window_height / img_h
    scale = min(scale_width, scale_height)
    # resized window width and height
    window_width = int(img_w * scale)
    window_height = int(img_h * scale)
    # cv2.WINDOW_NORMAL makes the output window resizable
    cv2.namedWindow(img_wind, cv2.WINDOW_NORMAL)
    # resize the window according to the screen resolution
    cv2.resizeWindow(img_wind, window_width, window_height)




def regenerate_img(img, threshold):
    row, col = img.shape
    y = np.zeros((row, col))
    for i in range(0, row):
        for j in range(0, col):
            if img[i, j] >= threshold:
                y[i, j] = 255
            else:
                y[i, j] = 0
    return y


def Hist(img):
    row, col = img.shape
    y = np.zeros(256)
    for i in range(0, row):
        for j in range(0, col):
            y[img[i, j]] += 1
    x = np.arange(0, 256)
    plt.bar(x, y, color='b', width=5, align='center', alpha=0.25)
    plt.show()
    return y


def regenerate_img(img, threshold):
    row, col = img.shape
    y = np.zeros((row, col))
    for i in range(0, row):
        for j in range(0, col):
            if img[i, j] >= threshold:
                y[i, j] = 255
            else:
                y[i, j] = 0
    return y


def countPixel(h):
    cnt = 0
    for i in range(0, len(h)):
        if h[i] > 0:
            cnt += h[i]
    return cnt


def wieght(s, e):
    w = 0
    for i in range(s, e):
        w += h[i]
    return w


def mean(s, e):
    m = 0
    w = wieght(s, e)
    for i in range(s, e):
        m += h[i] * i

    return m / float(w)


def variance(s, e):
    v = 0
    m = mean(s, e)
    w = wieght(s, e)
    for i in range(s, e):
        v += ((i - m) ** 2) * h[i]
    v /= w
    return v


def threshold(h):
    cnt = countPixel(h)
    for i in range(1, len(h)):
        vb = variance(0, i)
        wb = wieght(0, i) / float(cnt)
        mb = mean(0, i)

        vf = variance(i, len(h))
        wf = wieght(i, len(h)) / float(cnt)
        mf = mean(i, len(h))

        V2w = wb * (vb) * (vb) + wf * (vf) * (vf)
        V2b = wb * wf * (mb - mf) ** 2

        fw = open("trace.txt", "a")
        fw.write('T=' + str(i) + "\n")

        fw.write('Wb=' + str(wb) + "\n")
        fw.write('Mb=' + str(mb) + "\n")
        fw.write('Vb=' + str(vb) + "\n")

        fw.write('Wf=' + str(wf) + "\n")
        fw.write('Mf=' + str(mf) + "\n")
        fw.write('Vf=' + str(vf) + "\n")

        fw.write('within class variance=' + str(V2w) + "\n")
        fw.write('between class variance=' + str(V2b) + "\n")
        fw.write("\n")

        if not math.isnan(V2w):
            threshold_values[i] = V2w


def get_optimal_threshold():
    min_V2w = min(threshold_values.values())
    optimal_threshold = [k for k, v in threshold_values.items() if v == min_V2w]
    print('optimal threshold', optimal_threshold[0])
    return optimal_threshold[0]


def clean_img(img):
    h = Hist(img)
    threshold(h)
    op_thres = get_optimal_threshold()

    res = regenerate_img(img, op_thres)
