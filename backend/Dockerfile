# backend/Dockerfile

# Базовый образ с Python 3.11
FROM python:3.11-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Установка системных библиотек:
# - libpq-dev для psycopg2
# - poppler-utils для pdfplumber
# - tesseract-ocr для OCR (pytesseract)
# - gcc для сборки зависимостей, если потребуется
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      gcc \
      libpq-dev \
      poppler-utils \
      tesseract-ocr \
      tesseract-ocr-eng \
      tesseract-ocr-rus \
      tesseract-ocr-kaz \
	  libxml2-dev \
      libxslt1-dev && \ 
    rm -rf /var/lib/apt/lists/*

# Копируем и устанавливаем Python-зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ./app ./app

# По желанию: копируем .env, если вы планируете его монтировать внутрь контейнера
# COPY .env .env

# Открываем порт FastAPI
EXPOSE 8000

# Запуск Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
