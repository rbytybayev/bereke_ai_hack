# app/models.py

from sqlalchemy import Column, Text, TIMESTAMP, func, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import uuid
from pgvector.sqlalchemy import Vector
from .db import Base

class ContractRaw(Base):
    __tablename__ = "contracts_raw"
    doc_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    filename = Column(Text, nullable=False) 
    content = Column(Text, nullable=True)
    upload_date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class DocumentFragment(Base):
    __tablename__ = "document_fragments"
    fragment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    doc_id      = Column(UUID(as_uuid=True), ForeignKey("contracts_raw.doc_id"), nullable=False)
    content     = Column(Text, nullable=False)
    # Эмбеддинг размерности 384
    embedding   = Column(Vector(384), nullable=False)
    
class ContractParsed(Base):
    __tablename__ = "contracts_parsed"
    doc_id = Column(UUID(as_uuid=True), primary_key=True)
    contract_date = Column(Text, nullable=True)
    contract_amount = Column(Text, nullable=True)
    contract_number = Column(Text, nullable=True)
    contract_currency = Column(Text, nullable=True)
