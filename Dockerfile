# Usa una imagen base oficial de Python
FROM python:3.8-slim

# Instala Tesseract-OCR
RUN apt-get update && apt-get install -y tesseract-ocr tesseract-ocr-spa \
    && apt-get clean 

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de requisitos y los instala
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de la aplicación
COPY . /app

# Expone el puerto en el que Flask se ejecutará
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "app.py"]
