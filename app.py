from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
import pytesseract
import io
from src.response import res

app = Flask(__name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    """ Check if the file has one of the allowed extensions """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/api/ocr', methods=['POST'])
def ocr_api():
    if 'file' not in request.files:
        return jsonify(res(None, "No file part :c", False)), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(res(None, "No selected file", False)), 400
    if not allowed_file(file.filename):
        return jsonify(res(None, "File extension not allowed", False)), 400
    
    try:
        with Image.open(io.BytesIO(file.read())) as image:
            custom_oem_psm_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, lang='spa', config=custom_oem_psm_config)
    except UnidentifiedImageError:
        return jsonify(res(None, "Invalid image file", False)), 400
    
    return jsonify(res(text, "Text extracted successfully", True))

if __name__ == '__main__':
    app.run(debug=True)  # For local development
