from pydantic import BaseModel, Field
from typing import Optional

class ForeignPartner(BaseModel):
    name: str
    country: Optional[str] = None
    swift: Optional[str] = None
    address: Optional[str] = None

class ContractData(BaseModel):
    contract_number: str
    contract_date: str
    contract_amount: str
    currency: str
    deal_type: str  # экспорт / импорт
    tnved_code: Optional[str] = None
    payment_terms: Optional[str] = None
    foreign_partner: Optional[ForeignPartner] = None
