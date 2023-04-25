import os.path

from keras.models import load_model
import cv2
import numpy as np


MODEL_FOLDER = 'model/model_II_v1/'
model = load_model(MODEL_FOLDER)

classes = {
    1: 'FA',
    0: 'normal'
}

img_size = 640, 320


def predict(img):
    rs_img = cv2.resize(img, img_size)

    model_input = rs_img.reshape((1, *rs_img.shape))

    pred = model.predict(model_input)
    result = classes[int(np.round(pred).flatten().tolist()[0])]

    return result


if __name__ == '__main__':
    img = cv2.imread('../test_images/test_II.jpg')

    res = predict(img)

    print(res)
