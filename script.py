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
from PIL import Image
import pytesseract
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400

    image_file = request.files['image']
    image = Image.open(image_file.stream)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # Run pytesseract OCR for Bangla
    text = pytesseract.image_to_string(image, lang='ben')  # 'ben' = Bengali language code
    return jsonify({'text': text})

if __name__ == '__main__':
    try:
        # img = Image.open(r"C:\Users\tofiq.akbar\PyCharmMiscProject\test2.png")
        # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        # text = pytesseract.image_to_string(r"C:\Users\tofiq.akbar\PyCharmMiscProject\test2.png",lang='ben')
        # print(text)
        app.run(host='0.0.0.0', port=5000)
    except Exception as e:
        print(e)