# app/api.py

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from uuid import uuid4

from .db import get_db
from .models import ContractRaw, DocumentFragment
from .schemas import AnalyzeResponse
from .utils.extract import extract_text
from .utils.semantic import chunk_text, get_embedding

router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(
    files: list[UploadFile] = File(None),
    file: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    """
    Принимает один или несколько PDF-файлов под полями 'files' или 'file',
    объединяет их тексты, сохраняет в contracts_raw и document_fragments,
    возвращает аналитику.
    """
    # 1. Консолидируем загруженные файлы
    uploads = []
    if files:
        uploads.extend(files)
    if file:
        uploads.append(file)
    if not uploads:
        raise HTTPException(status_code=400, detail="Нужно передать хотя бы один файл 'file' или 'files'")

    # 2. Извлечение текста из каждого файла
    tmp_dir = "/tmp/uploads"
    os.makedirs(tmp_dir, exist_ok=True)
    all_texts = []
    for up in uploads:
        filename = f"{uuid4()}.pdf"
        path = os.path.join(tmp_dir, filename)
        with open(path, "wb") as f_out:
            shutil.copyfileobj(up.file, f_out)
        text = extract_text(path)
        if text and text.strip():
            all_texts.append(text)
    if not all_texts:
        raise HTTPException(status_code=400, detail="Не удалось извлечь текст ни из одного документа")

    # 3. Объединяем тексты
    combined_content = "\n\n---\n\n".join(all_texts)

    # 4. Сохраняем raw содержимое
    first_filename = uploads[0].filename if uploads else "unknown.pdf"
    contract = ContractRaw(
        filename=first_filename,
        content=combined_content
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)

    # 5. Чанкование и генерация эмбеддингов
    fragments = chunk_text(combined_content)
    if not fragments:
        raise HTTPException(status_code=500, detail="Не удалось разбить текст на фрагменты")
    embeddings = get_embedding(fragments)
    if not embeddings:
        raise HTTPException(status_code=500, detail="Не удалось сгенерировать эмбеддинги")

    # 6. Сохранение чанков в БД
    for frag_text, vector in zip(fragments, embeddings):
        db.add(DocumentFragment(
            doc_id=contract.doc_id,
            content=frag_text,
            embedding=vector
        ))
    db.commit()

    # 7. Поиск релевантных фрагментов (3 ближайших)
    query_emb = embeddings[0]
    related = (
        db.query(DocumentFragment)
          .order_by(DocumentFragment.embedding.cosine_distance(query_emb))
          .limit(3)
          .all()
    )

    # 8. Формирование ответа (заглушка)
    snippets = [r.content for r in related]
    if snippets:
        detail = f"Найдено {len(snippets)} релевантных фрагмента(ов):\n" + "\n---\n".join(snippets)
    else:
        detail = "Ничего релевантного не найдено"
    result = "Принять"

    return AnalyzeResponse(
        doc_id=contract.doc_id,
        result=result,
        detail=detail
    )
