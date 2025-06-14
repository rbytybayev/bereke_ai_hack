# app/utils/semantic.py
from typing import List
from sentence_transformers import SentenceTransformer

# Загружаем модель (разово при старте)
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    words = text.split()
    chunks, i = [], 0
    while i < len(words):
        chunk = words[i : i + chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
    return chunks

def get_embedding(texts: List[str]) -> List[List[float]]:
    # возвращает список эмбеддингов
    return embed_model.encode(texts, show_progress_bar=False).tolist()
