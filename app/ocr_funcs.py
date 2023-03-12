from PIL import Image
import pytesseract
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\yashs\\Workspace\\Softwares\\Tesseract-OCR\\tesseract'
# Example tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'

img_pah = './static/EK_000001.jpg'

# # Simple image to string
# print(pytesseract.image_to_string(Image.open(img_pah)))
#
# # Get bounding box estimates
# print(pytesseract.image_to_boxes(Image.open(img_pah)))
#
# # Get verbose data including boxes, confidences, line and page numbers
# print(pytesseract.image_to_data(Image.open(img_pah)))

image = cv2.imread(img_pah)

# swap color channel ordering from BGR (OpenCV’s default) to RGB (compatible with Tesseract and pytesseract).
# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
results = pytesseract.image_to_data(rgb, output_type=Output.DICT, lang='eng')  # ,config=custom_config)
boxresults = pytesseract.image_to_boxes(rgb, output_type=Output.DICT, lang='eng')  # ,config=custom_config)
print(results)
print(boxresults)

for i in range(0, len(results["text"])):
    # extract the bounding box coordinates of the text region from the current result
    tmp_tl_x = results["left"][i]
    tmp_tl_y = results["top"][i]
    tmp_br_x = tmp_tl_x + results["width"][i]
    tmp_br_y = tmp_tl_y + results["height"][i]
    tmp_level = results["level"][i]
    conf = results["conf"][i]
    text = results["text"][i]

    if (tmp_level == 5):
        cv2.putText(image, text, (tmp_tl_x, tmp_tl_y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.rectangle(image, (tmp_tl_x, tmp_tl_y), (tmp_br_x, tmp_br_y), (0, 0, 255), 1)

for j in range(0, len(boxresults["left"])):
    left = boxresults["left"][j]
    bottom = boxresults["bottom"][j]
    right = boxresults["right"][j]
    top = boxresults["top"][j]
    cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 1)

# cv2.imshow("image", image)
# cv2.waitKey(0)
