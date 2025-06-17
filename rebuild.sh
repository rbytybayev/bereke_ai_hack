#!/bin/bash

echo "🛑 Останавливаем и очищаем контейнеры..."
docker-compose down -v

echo "⚙️  Собираем backend..."
docker-compose build backend

echo "🚀 Запускаем проект..."
docker-compose up
