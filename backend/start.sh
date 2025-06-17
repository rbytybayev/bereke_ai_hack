#!/bin/bash
echo "⏳ Ждём PostgreSQL..."
while ! nc -z db 5432; do
  sleep 1
done
echo "✅ БД доступна. Выполняем миграции..."
alembic upgrade head

echo "🚀 Запускаем FastAPI..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
