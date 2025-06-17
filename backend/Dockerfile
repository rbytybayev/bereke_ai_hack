FROM python:3.10-slim

# Установим сборочные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запуск alembic миграций перед стартом API
COPY start.sh /start.sh
RUN chmod +x /start.sh
CMD ["/start.sh"]
