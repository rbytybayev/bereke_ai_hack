import os
import subprocess

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from dotenv import load_dotenv
from app.api.routes import router as api_router
from app.db.session import Base
from app.db import async_engine 

# === Загрузка переменных из .env ===
load_dotenv()
USE_MIGRATIONS = os.getenv("USE_MIGRATIONS", "False").lower() == "true"

app = FastAPI(title="Currency Compliance Validator")

# === CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Роутинг ===
app.include_router(api_router, prefix="/api")

# === Инициализация БД ===
@app.on_event("startup")
async def setup_db():
    print(f"🔁 USE_MIGRATIONS = {USE_MIGRATIONS}")

    if USE_MIGRATIONS:
        print("📦 Применяем Alembic миграции...")
        subprocess.run(["alembic", "upgrade", "head"])
    else:
        print("🛠️ Создаём таблицы напрямую (SQLAlchemy Base)...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
