from PIL import Image
# import pytesseract
# from pytesseract import Output
import cv2
import os
import numpy as np
os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"
from easyocr import Reader
from cv_funcs import easy_ocr_thresholding
import re
from collections import OrderedDict

reader = Reader(['en'])
crop_kb = {'h': {'h1': ('I', 'aVR', 'V1', 'V6'),
                 'h2': ('II', 'aVL', 'V2', 'V5'),
                 'h3': ('III', 'aVF', 'V3', 'V5'),
                 'h4': 'II'},
           'v': {'v1': ('I', 'II', 'III', 'II'),
                 'v2': ('aVR', 'aVL', 'aVF'),
                 'v3': ('V1', 'V2', 'V3'),
                 'v4': 'V5'}}


def prep_text(s):
    s = s.lower().strip()
    regex = r"[^\w\s]"
    s = re.sub(regex, "", s)
    return s


def crop_img(img, bbox):
    #     print(bbox)
    crop_img = img[bbox[0][1]:bbox[1][1], bbox[0][0]:bbox[1][0]]
    return crop_img


def get_empty_coord():
    crop_coord = OrderedDict({
        'h': {
            'h1': None,
            'h2': None,
            'h3': None,
            'h4': None
        },
        'v': {
            'v1': None,
            'v2': None,
            'v3': None,
            'v4': None
        }})
    return crop_coord


def get_crops(img):
    image = easy_ocr_thresholding(img.copy())

    results = reader.readtext(image)

    crop_coord = get_empty_coord()

    # Horizontal
    for k, pattern in crop_kb['h'].items():
        for res in results:
            for pat in map(prep_text, pattern):
                if prep_text(res[1]) == pat:
                    if crop_coord['h'][k]:
                        if res[2] > crop_coord['h'][k][1]:
                            crop_coord['h'][k] = (np.array(res[0]).mean(axis=0).round().astype(int)[1], res[2])
                    else:
                        crop_coord['h'][k] = (np.array(res[0]).mean(axis=0).round().astype(int)[1], res[2])
    # Vertical
    for k, pattern in crop_kb['v'].items():
        for res in results:
            for pat in map(prep_text, pattern):
                if prep_text(res[1]) == pat:
                    if crop_coord['v'][k]:
                        if res[2] > crop_coord['v'][k][1]:
                            crop_coord['v'][k] = (np.array(res[0]).mean(axis=0).round().astype(int)[0], res[2])
                    else:
                        crop_coord['v'][k] = (np.array(res[0]).mean(axis=0).round().astype(int)[0], res[2])

    for k, hdict in crop_coord['h'].items():
        if crop_coord['h'][k]:
            crop_coord['h'][k] = crop_coord['h'][k][0]
    for k, pattern in crop_coord['v'].items():
        if crop_coord['v'][k]:
            crop_coord['v'][k] = crop_coord['v'][k][0]

    cc = crop_coord
    vertical_def = None
    horizontal_def = None
    h_buf, v_buf = None, None

    for k, v in cc['h'].items():
        if v:
            if h_buf:
                horizontal_def = v - h_buf
                break
            else:
                h_buf = v
    h_buf = None
    if horizontal_def:
        for k, v in cc['h'].items():
            if not v and h_buf:
                cc['h'][k] = h_buf + horizontal_def
            else:
                h_buf = v

    for k, v in cc['v'].items():
        if v:
            if v_buf:
                vertical_def = v - v_buf
                break
            else:
                v_buf = v
    v_buf = None
    if vertical_def:
        for k, v in cc['v'].items():
            if not v and v_buf:
                cc['v'][k] = v_buf + vertical_def
            else:
                v_buf = v

    cc = {}
    for k, v in crop_coord['h'].items():
        cc[k] = v
    for k, v in crop_coord['v'].items():
        cc[k] = v

    # tl, tr, br, bl
    crop_ref = {
        'I': [[cc['v1'], cc['h1']], [cc['v2'], cc['h2']]],
        'aVR': [[cc['v2'], cc['h1']], [cc['v3'], cc['h2']]],
        'V1': [[cc['v3'], cc['h1']], [cc['v4'], cc['h2']]],
        'V4': [[cc['v4'], cc['h1']], ['end', cc['h2']]],
        'II': [[cc['v1'], cc['h2']], [cc['v2'], cc['h3']]],
        'aVL': [[cc['v2'], cc['h2']], [cc['v3'], cc['h3']]],
        'V2': [[cc['v3'], cc['h2']], [cc['v4'], cc['h3']]],
        'V5': [[cc['v4'], cc['h2']], ['end', cc['h3']]],
        'III': [[cc['v1'], cc['h3']], [cc['v2'], cc['h4']]],
        'aVF': [[cc['v2'], cc['h3']], [cc['v3'], cc['h4']]],
        'V3': [[cc['v3'], cc['h3']], [cc['v4'], cc['h4']]],
        'V6': [[cc['v4'], cc['h4']], ['end', cc['h4']]],
        'II_2': [[cc['v1'], cc['h4']], ['end', 'end']]
    }
    H, W = img.shape[:2]
    #print(img.shape)
    images_list = []

    for k, v in crop_ref.items():
        tl, br = v
        if tl[0] == 'end':
            tl[0] = W
        if br[0] == 'end':
            br[0] = W
        if tl[1] == 'end':
            tl[1] = H
        if br[1] == 'end':
            br[1] = H
        #print(k)
        #print(tl,br)
        images_list.append((k, crop_img(img, [tl,br])))

    return images_list

    #     tl, br = v
    #     if tl[0] == 'end':
    #         tl[0] = W
    #     if br[0] == 'end':
    #         br[0] = W
    #     if tl[1] == 'end':
    #         tl[1] = H
    #     if br[1] == 'end':
    #         br[1] = H
    #
    #     cv2.rectangle(img, tl, br, (0, 255, 0), 2)

    # return img




# pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\yashs\\Workspace\\Softwares\\Tesseract-OCR\\tesseract'
# # Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
#
# img_pah = './static/EK_000001.jpg'
#
# # Simple image to string
# print(pytesseract.image_to_string(Image.open(img_pah)))
# #
# # # Get bounding box estimates
# # print(pytesseract.image_to_boxes(Image.open(img_pah)))
# #
# # # Get verbose data including boxes, confidences, line and page numbers
# # print(pytesseract.image_to_data(Image.open(img_pah)))
#
# image = cv2.imread(img_pah)
#
# # swap color channel ordering from BGR (OpenCV’s default) to RGB (compatible with Tesseract and pytesseract).
# # By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# # we need to convert from BGR to RGB format/mode:
# rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
# results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='eng')  # ,config=custom_config)
# boxresults = pytesseract.image_to_boxes(rgb, output_type=Output.DICT, lang='eng')  # ,config=custom_config)
# print(results)
# print(boxresults)
#
# for i in range(0, len(results["text"])):
#     # extract the bounding box coordinates of the text region from the current result
#     tmp_tl_x = results["left"][i]
#     tmp_tl_y = results["top"][i]
#     tmp_br_x = tmp_tl_x + results["width"][i]
#     tmp_br_y = tmp_tl_y + results["height"][i]
#     tmp_level = results["level"][i]
#     conf = results["conf"][i]
#     text = results["text"][i]
#
#     if (tmp_level == 5):
#         cv2.putText(image, text, (tmp_tl_x, tmp_tl_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
#         cv2.rectangle(image, (tmp_tl_x, tmp_tl_y), (tmp_br_x, tmp_br_y), (0, 0, 255), 1)
#
# for j in range(0, len(boxresults["left"])):
#     left = boxresults["left"][j]
#     bottom = boxresults["bottom"][j]
#     right = boxresults["right"][j]
#     top = boxresults["top"][j]
#     cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 1)
#
# # cv2.imshow("image", image)
# # cv2.waitKey(0)
#
#
# crop_kb = {'h': {'h1': ('I', 'aVR', 'V1', 'V6'),
#                  'h2': ('II', 'aVL', 'V2', 'V5'),
#                  'h3': ('III', 'aVF', 'V3', 'V5'),
#                  'h4': 'II'},
#            'v': {'v1': ('I', 'II', 'III', 'II'),
#                  'v2': ('aVR', 'aVL', 'aVF'),
#                  'v3': ('V1', 'V2', 'V3'),
#                  'v4': 'V5'}}
# crop_kb
