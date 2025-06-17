from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class StatusEnum(str, enum.Enum):
    ACCEPTED = "Принят"
    REJECTED = "Отказано"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Document(Base):
    __tablename__ = "documents"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_id = Column(String, nullable=False, unique=True)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    upload_time = Column(DateTime(timezone=True), server_default=func.now())

    status = Column(Enum(StatusEnum), default=StatusEnum.REJECTED)
    status_comment = Column(Text)
    updated_by = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    uploader = relationship("User", foreign_keys=[uploaded_by])
    updater = relationship("User", foreign_keys=[updated_by])
