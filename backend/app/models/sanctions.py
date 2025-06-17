from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Sanction(Base):
    __tablename__ = "sanctions"

    id = Column(Integer, primary_key=True, index=True)
    source = Column(String, nullable=False)  # OFAC, EU, UK
    name = Column(Text, nullable=False)
    original_name = Column(Text)
    comment = Column(Text)
    start_date = Column(String)
    end_date = Column(String)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
