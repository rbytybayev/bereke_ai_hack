# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import router
from .db import Base, engine

app = FastAPI(title="AI Compliance Assistant")
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # или ["*"] для всех
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# создаем таблицы (для dev)
Base.metadata.create_all(bind=engine)

app.include_router(router, prefix="")
