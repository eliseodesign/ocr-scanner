from flask import Flask, request, render_template
from PIL import Image
import pytesseract
import io

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file:
            image = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(image, lang='eng')
            return render_template('show_text.html', extracted_text=text)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
