from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.file_ops import save_upload_file
from app.services.image_preprocess import preprocess_pdf
from app.services.pdf_parser import extract_text_from_pdf
from app.core.lang_detect import detect_language
from app.services.signature_detector import detect_signature_presence
from app.services.extractor import extract_contract_parameters
from app.services.verdict import generate_summary_and_verdict
from app.models.schema import ContractData
from app.services.checker import run_checks
from app.services.sanctions_loader import refresh_all_sanctions
from app.core.auth import get_current_user, authenticate_user, get_password_hash, create_access_token
from app.models.user_document import User, Document, StatusEnum
from app.db.session import get_async_session 
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
import uuid
import os

router = APIRouter()

UPLOAD_DIR = "uploaded_docs"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/documents/my")
async def get_my_documents(current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Document).where(Document.uploaded_by == current_user.id))
    docs = result.scalars().all()
    return [
        {
            "file_id": d.file_id,
            "filename": d.filename,
            "upload_time": d.upload_time,
            "status": d.status,
            "status_comment": d.status_comment,
            "updated_by": d.updated_by,
        }
        for d in docs
    ]

@router.post("/auth/register")
async def register(
    username: str = Form(...),
    password: str = Form(...),
    session: AsyncSession = Depends(get_async_session)
    ):
    result = await session.execute(select(User).where(User.username == username))
    if result.scalar():
        raise HTTPException(status_code=400, detail="Username already registered")

    user = User(username=username, hashed_password=get_password_hash(password))
    session.add(user)
    await session.commit()
    return {"status": "registered"}

@router.post("/auth/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_async_session)):
    user = await authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...), current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_id = str(uuid.uuid4())
    filepath = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    await save_upload_file(file, filepath)

    try:
        images = preprocess_pdf(filepath)
        extracted_text = extract_text_from_pdf(images)
        language = detect_language(extracted_text)
        has_signature = detect_signature_presence(images)
        contract_dict = extract_contract_parameters(extracted_text)
        contract_data = ContractData(**contract_dict)
        checks = await run_checks(contract_data)
        verdict = generate_summary_and_verdict(checks)

        doc = Document(
            filename=file.filename,
            file_id=file_id,
            uploaded_by=current_user.id,
            status=StatusEnum.REJECTED if verdict['decision'] == "Отказать" else StatusEnum.ACCEPTED
        )
        session.add(doc)
        await session.commit()

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

    return JSONResponse({
        "file_id": file_id,
        "language": language,
        "has_signature": has_signature,
        "contract_data": contract_data.dict(),
        "checks": checks,
        "verdict": verdict
    })


@router.post("/refresh_sanctions")
async def refresh_sanctions(session=Depends(get_async_session)):
    await refresh_all_sanctions(session)
    return {"status": "updated"}


class StatusUpdateRequest(BaseModel):
    file_id: str
    new_status: StatusEnum
    comment: str

@router.post("/update_status")
async def update_status(data: StatusUpdateRequest, current_user: User = Depends(get_current_user), session: AsyncSession = Depends(get_async_session)):
    result = await session.execute(select(Document).where(Document.file_id == data.file_id))
    doc = result.scalar()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    doc.status = data.new_status
    doc.status_comment = data.comment
    doc.updated_by = current_user.id
    await session.commit()

    return {"status": doc.status, "comment": doc.status_comment, "updated_by": current_user.username}