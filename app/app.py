import base64
import json
import numpy as np
import cv2
import os

from flask import Flask, flash, redirect, request, Response, render_template, session
import io
from werkzeug.utils import secure_filename

from ocr_funcs import get_crops
from cv_funcs import transform
from PIL import Image
from pdf_funcs import get_image_from_pdf_bytes
from cv_funcs import custom_thresholding


# Initialize the Flask application
app = Flask(__name__)

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/upload_image', methods=["POST"])
def uploadFile():
    file_path = ''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        data = io.BytesIO()
        file.save(data)
        data.seek(0)
        img = Image.open(data)
        npimg = np.array(img)
        npimg = transform(npimg)
        img = Image.fromarray(npimg)

        img.save(file_path)
        return render_template('show_image.html', images=[('', file_path)])


@app.route('/upload_pdf', methods=["POST"])
def upload_pdf():
    file_path = ''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output_prefix = os.path.splitext(filename)[0] + '.jpg'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_prefix)
        data = io.BytesIO()
        file.save(data)
        data.seek(0)

        img = get_image_from_pdf_bytes(data)

        height, width = img.shape[:2]
        crop_height = int(height * 0.2)
        img = img[crop_height:height, 0:width]

        img = custom_thresholding(img)

        img = Image.fromarray(img)

        img.save(file_path)
        return render_template('show_image.html', images=[('', file_path)])


@app.route('/ocr_pdf', methods=["POST"])
def upload_pdf_ocr():
    file_path = ''
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output_prefix = os.path.splitext(filename)[0] + '.jpg'
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_prefix)
        data = io.BytesIO()
        file.save(data)
        data.seek(0)

        img = get_image_from_pdf_bytes(data)

        img_list = get_crops(img)
        img_paths = []
        for name, c_img in img_list:
            print(name)
            print(c_img.shape)
            if 0 in c_img.shape:
                continue
            # c_img = Image.fromarray(c_img)
            i_path = os.path.splitext(file_path)[0] + name + '.jpg'

            cv2.imwrite(i_path,c_img)
            img_paths.append((name, i_path))

        return render_template('show_image.html', images=img_paths)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
