# Usar una imagen base de Python
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . /app

# Instalar las dependencias necesarias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install uvicorn  # Instalar uvicorn si no está en requirements.txt

# Exponer el puerto donde Uvicorn escuchará
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
