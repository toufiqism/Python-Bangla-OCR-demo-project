# # This is a sample Python script.
#
# # Press Shift+F10 to execute it or replace it with your code.
# # Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
# import pytesseract
# from PIL import Image
# from pathlib import Path
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print(pytesseract.image_to_string(Image.open(Path(r"C:\Users\tofiq.akbar\PyCharmMiscProject\test.png"))))
#
#
#
#
#
#
#
from PIL import Image,ImageOps, ImageFilter
import pytesseract
import cv2
import numpy as np
import io
from flask import Flask, request, jsonify


app = Flask(__name__)



@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    # Read image from request
    image_file = request.files['image']
    image_bytes = image_file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # --- Preprocessing Steps ---

    # 1. Convert to grayscale
    image = image.convert('L')

    # 2. Resize (scaling up small text improves OCR accuracy)
    base_width = 1800
    w_percent = (base_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    image = image.resize((base_width, h_size), Image.LANCZOS)

    # 3. Optional: Enhance contrast and remove noise
    image = ImageOps.autocontrast(image)
    image = image.filter(ImageFilter.MedianFilter(size=3))

    # --- OCR Processing ---
    try:
        text = pytesseract.image_to_string(image, lang='ben',config='--dpi 300')
        return jsonify({'text': text.strip()})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# @app.route('/extract_text', methods=['POST'])
# def extract_text():
#     image_bytes = request.files['image'].read()
#     image = preprocess_opencv(image_bytes)
#     text = pytesseract.image_to_string(image, lang='ben')
#     return jsonify({'text': text.strip()})


def preprocess_opencv(image_bytes):
    npimg = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Resize to width 1800 px
    scale = 1800 / gray.shape[1]
    gray = cv2.resize(gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_LANCZOS4)

    # Adaptive thresholding
    processed = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    # Convert back to PIL for pytesseract
    pil_image = Image.fromarray(processed)
    return pil_image

if __name__ == '__main__':
    try:
        # img = Image.open(r"C:\Users\tofiq.akbar\PyCharmMiscProject\test2.png")
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # text = pytesseract.image_to_string(r"C:\Users\tofiq.akbar\PyCharmMiscProject\test2.png",lang='ben')
        # print(text)
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(e)