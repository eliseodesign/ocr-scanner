from flask import Blueprint, request, jsonify, send_file
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np
import cv2
import io
from src.response import res
from src.utils import allowed_file
from src.perseptive import correct_perspective

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

        #! Mejora de perspectiva
        image_correct = correct_perspective(open_cv_image)
        if image_correct is None:
            return jsonify(res(None, "No rectangle could be found", False)), 400

        open_cv_image = image_correct

        #! Mejora de calidad
        # Convertir RGB a BGR para OpenCV
        open_cv_image = open_cv_image[:, :, ::-1].copy()

        # Convertir de nuevo de OpenCV Image a PIL Image
        image = Image.fromarray(open_cv_image[:, :, ::-1])

         # Aplicar el realce de bordes para resaltar el texto
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        
        # Mejorar el contraste de la imagen
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)  # Aumentar el contraste


        # Volver imagen a blanco y negro
        image = image.convert('L')

        # Guardar la imagen mejorada en un buffer
        img_io = io.BytesIO()
        image.save(img_io, 'PNG', quality=70)
        img_io.seek(0)

        # Devolver la imagen como una respuesta
        return send_file(img_io, mimetype='image/png')
