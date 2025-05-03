# teambudgets-front/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

# Instala dependencias
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.enableCORS=false"]
