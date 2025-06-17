#!/bin/bash

echo "🧹 Полная очистка Docker окружения..."
docker-compose down -v --remove-orphans
docker container prune -f
docker image prune -a -f
docker volume prune -f
docker network prune -f
docker system prune -a -f

echo "📦 Установка зависимостей и сборка backend..."
docker-compose build backend

echo "🚀 Запускаем весь проект..."
docker-compose up
