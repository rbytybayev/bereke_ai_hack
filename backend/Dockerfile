FROM python:3.10-slim

# Установим сборочные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    tesseract-ocr \
    tesseract-ocr-rus \
    tesseract-ocr-eng \
    tesseract-ocr-kaz \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    cmake \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск alembic миграций перед стартом API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]