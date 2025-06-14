import pickle
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import ContractRaw, ContractParsed
from sqlalchemy.dialects.postgresql import insert

# Загрузка моделей
with open("models/emb_model.pkl", "rb") as f:
    embedder = pickle.load(f)

with open("models/clf.pkl", "rb") as f:
    clf = pickle.load(f)

def extract_fields(text: str):
    chunks = [line.strip() for line in text.splitlines() if line.strip()]
    extracted = {}

    for chunk in chunks:
        embedding = embedder.encode([chunk])
        label = clf.predict(embedding)[0]

        if label in ["contract_date", "contract_amount", "contract_number", "contract_currency"] and label not in extracted:
            extracted[label] = chunk

    return extracted

def main():
    db: Session = SessionLocal()
    try:
        docs = db.query(ContractRaw).all()
        for doc in docs:
            result = extract_fields(doc.content or "")
            stmt = insert(ContractParsed).values(
                doc_id=doc.doc_id,
                contract_date=result.get("contract_date"),
                contract_amount=result.get("contract_amount"),
                contract_number=result.get("contract_number"),
                contract_currency=result.get("contract_currency"),
            ).on_conflict_do_update(
                index_elements=['doc_id'],
                set_={
                    "contract_date": result.get("contract_date"),
                    "contract_amount": result.get("contract_amount"),
                    "contract_number": result.get("contract_number"),
                    "contract_currency": result.get("contract_currency"),
                }
            )
            db.execute(stmt)
        db.commit()
        print("✅ Обработка завершена.")
    finally:
        db.close()

if __name__ == "__main__":
    main()
