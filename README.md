# Proyecto API OCR con Flask

Este proyecto es una API construida con Flask que proporciona funcionalidades OCR (Reconocimiento Óptico de Caracteres). La API permite enviar imágenes y devuelve el texto extraído de ellas.

## Requisitos

- Python 3.8
- Flask
- numpy==1.19.2
- Pillow
- opencv-python==4.4.0.42
- pytesseract
- python-dotenv

## Instalación

1. Clona este repositorio.

```bash
git clone https://github.com/eliseodesign/ocr-scanner
```

2. Ve al directorio del proyecto.

```bash
cd ocr-scanner
```

3. Crea un entorno virtual e instala las dependencias.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. Carga las variables de entorno.

```bash
load_dotenv()
```

## Uso

Para ejecutar la aplicación, utiliza el siguiente comando:

```bash
python app.py
```

La aplicación se ejecutará en el puerto 5000.

## API

### OCR

El endpoint `/api/ocr` permite realizar OCR en una imagen.

#### POST /api/ocr

- `file`: La imagen a procesar. Debe ser un archivo en formato JPG, JPEG o PNG.

##### Respuesta

- `200 OK`: La operación se realizó correctamente. El cuerpo de la respuesta contiene el texto extraído de la imagen.

```json
{
    "data": "El texto extraído de la imagen",
    "message": "Text extracted successfully",
    "success": true
}
```

- `400 Bad Request`: No se proporcionó una imagen válida. El cuerpo de la respuesta contiene un mensaje de error.

```json
{
    "data": null,
    "message": "No file part :c",
    "success": false
}
```

## Docker

Este proyecto incluye un archivo `Dockerfile` y un `docker-compose.yml` para facilitar la implementación con Docker.

Para construir y ejecutar el contenedor, utiliza el siguiente comando:

```bash
docker-compose up --build
```

La aplicación se ejecutará en el puerto 5000 del contenedor, que se mapeará al puerto 5000 del host.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.