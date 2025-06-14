# app/schemas.py
from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class AnalyzeResponse(BaseModel):
    doc_id: UUID
    result: str  # пока stub
    detail: Optional[str]
