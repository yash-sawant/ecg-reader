from pdf2image import convert_from_path,convert_from_bytes
import cv2
import numpy as np

POPPLER_PATH = r'C:\Users\yashs\Workspace\Softwares\poppler-0.68.0_x86\poppler-0.68.0\bin'


def get_image_from_pdf(path):
    dpi = 300
    image = convert_from_path(path, dpi=dpi, first_page=1, last_page=1, poppler_path=POPPLER_PATH)[0]
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return img


def get_image_from_pdf_bytes(bytes):
    dpi = 300
    image = convert_from_bytes(bytes.read(), dpi=dpi, first_page=1, last_page=1, poppler_path=POPPLER_PATH)[0]
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    return img
