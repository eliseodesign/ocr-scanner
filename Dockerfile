# Usa una imagen base oficial de Python
FROM python:3.8-slim

# Instala Tesseract-OCR y dependencias necesarias para OpenCV
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-spa \
    libgl1-mesa-dev \     
    libglib2.0-0          

# Limpia los archivos de paquetes innecesarios para reducir el tamaño del contenedor
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

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
