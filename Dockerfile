# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Configura el directorio de trabajo en el contenedor
WORKDIR /app

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    && apt-get clean

# Copia el archivo de requerimientos
COPY requirements.txt .

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el contenido del proyecto
COPY . .

# Expone el puerto en el que la aplicación correrá
EXPOSE 8000

# Ejecuta la aplicación
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]