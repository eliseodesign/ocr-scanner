from flask import Blueprint, request, jsonify, send_file
from PIL import Image, ImageEnhance
import numpy as np
import cv2
import io
from src.response import res
from src.utils import allowed_file


enhance_api = Blueprint('enhance_api', __name__)

@enhance_api.route('/enhance', methods=['POST'])
def enhance_funct():
    # Chequear si el archivo fue enviado y si el request es válido
    if 'file' not in request.files:
        return jsonify(res(None, "No file part :c", False)), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify(res(None, "No selected file", False)), 400
    if not allowed_file(file.filename):
        return jsonify(res(None, "File extension not allowed", False)), 400
    if file:
        # Leer la imagen desde el archivo subido
        image_stream = io.BytesIO(file.read())
        image_stream.seek(0)
        image = Image.open(image_stream)
        
        # Convertir PIL Image a OpenCV Image
        open_cv_image = np.array(image)
        # Convertir RGB a BGR para OpenCV
        open_cv_image = open_cv_image[:, :, ::-1].copy()
        
        # Aplicar un desenfoque Gaussiano para suavizar la imagen
        open_cv_image = cv2.GaussianBlur(open_cv_image, (5, 5), 0)
        
        # Convertir de nuevo de OpenCV Image a PIL Image
        image = Image.fromarray(open_cv_image[:, :, ::-1])
        
        # Mejorar el contraste de la imagen
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)  # Aumentar el contraste

        # Volver imagen a blanco y negro
        image = image.convert('L')
        
        # Guardar la imagen mejorada en un buffer
        img_io = io.BytesIO()
        image.save(img_io, 'JPEG', quality=70)
        img_io.seek(0)
        
        # Devolver la imagen como una respuesta
        return send_file(img_io, mimetype='image/jpeg')