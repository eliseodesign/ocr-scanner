from flask import Flask
from api.ocr import ocr_api
from api.enhance import enhance_api
from api.auto_correct_perspective import auto_perspective_api
import os
from dotenv import load_dotenv

load_dotenv()


app = Flask(__name__)

app.register_blueprint(auto_perspective_api, url_prefix='/api')
app.register_blueprint(ocr_api, url_prefix='/api')
app.register_blueprint(enhance_api, url_prefix='/api')

PRODUCTION = os.getenv('PRODUCTION', True)

if __name__ == '__main__':
    app.run(debug=not PRODUCTION, host='0.0.0.0', port=5000)
