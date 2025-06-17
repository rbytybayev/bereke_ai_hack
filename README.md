# 💼 AI-Платформа валютного контроля и санкционных проверок

Автоматизированное FastAPI + React-приложение для анализа PDF-договоров с проверкой на соответствие валютному законодательству РК и санкционным спискам (OFAC, EU). Поддерживает LLM-инференс, OCR, предобработку изображений и JWT-авторизацию.

---

## 📦 Состав проекта

- **Backend**: FastAPI + PostgreSQL + LLaMA.cpp
- **Frontend**: React + Vite + TailwindCSS + shadcn/ui
- **База данных**: PostgreSQL + pgvector
- **Контейнеризация**: Docker + Docker Compose
- **Интеграции**: OFAC, EU API, LLM-инференс, PDF OCR

---

## 🚀 Запуск проекта

```bash
git clone https://your-repo-url.git
cd your-repo

# 1. Настроить .env
cp backend/.env.example backend/.env
# Укажи DATABASE_URL и SECRET_KEY

# 2. Собрать и запустить проект
docker-compose up --build

# 3. (опционально) Применить миграции вручную
docker compose exec backend alembic upgrade head
