#!/bin/bash

echo "🧹 Полная очистка Docker окружения..."
docker-compose down -v --remove-orphans
docker container prune -f
docker image prune -a -f
docker volume prune -f
docker network prune -f
docker system prune -a -f

echo "⚙️  Пересборка всех сервисов..."
docker-compose build --no-cache

echo "🚀 Запускаем проект..."
docker-compose up -d
echo "📦 Применяем миграции Alembic..."
echo "✅ Готово!"