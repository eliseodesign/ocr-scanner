from flask import Blueprint, request, jsonify, send_file
import cv2
import numpy as np
import io
from PIL import Image

auto_perspective_api = Blueprint('auto_perspective_api', __name__)

@auto_perspective_api.route('/auto_correct_perspective', methods=['POST'])
def auto_correct_perspective():
    file = request.files['file']
    
    if not file:
        return jsonify({"error": "No file provided"}), 400

    # Read the image
    image = Image.open(file.stream)
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)

    # Find contours and sort them by size
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]

    # Loop over the contours to find the best possible rectangle
    for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)

        # Assuming that the contour with 4 points is our document
        if len(approx) == 4:
            pts = np.array([item[0] for item in approx], dtype="float32")
            break
    else:
        return jsonify({"error": "No rectangle could be found"}), 400

    # Compute the perspective transform matrix and apply it
    transformed = four_point_transform(image, pts)

    # Convert back to PIL Image to send via Flask
    im_pil = Image.fromarray(transformed)
    img_io = io.BytesIO()
    im_pil.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

def four_point_transform(image, pts):
    # Obtain a consistent order of the points and unpack them
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    # Compute the width of the new image
    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = max(int(widthA), int(widthB))

    # Compute the height of the new image
    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = max(int(heightA), int(heightB))

    # Set up the destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]
    ], dtype="float32")

    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped


def order_points(pts):
    # Ordena los puntos en la forma: superior izquierdo, superior derecho,
    # inferior derecho e inferior izquierdo
    rect = np.zeros((4, 2), dtype="float32")
    
    # La suma de los puntos proporciona la esquina superior izquierda
    # El punto con la menor suma es la esquina superior izquierda
    # El punto con la mayor suma es la esquina inferior derecha
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    
    # La diferencia entre los puntos proporciona la esquina superior derecha
    # El punto con la menor diferencia es la esquina superior derecha
    # El punto con la mayor diferencia es la esquina inferior izquierda
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    
    # Devuelve los puntos ordenados
    return rect
