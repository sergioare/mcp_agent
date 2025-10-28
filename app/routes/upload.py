# app/routes/upload.py
from fastapi import APIRouter, UploadFile, File, Form
from app.services.storage.storage_service import StorageService

router = APIRouter(prefix="/upload", tags=["upload"])
storage_service = StorageService()

@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    """
    Receives a file (PDF, TXT, DOCX) and stores it in the system.
    Returns a document ID for later embedding or search.
    """
    content = await file.read()
    doc_id = storage_service.save_raw(file.filename, content.decode("utf-8", errors="ignore"))
    return {"doc_id": doc_id, "filename": file.filename}

@router.post("/text")
async def upload_text(filename: str = Form(...), content: str = Form(...)):
    """
    Alternative endpoint for direct text upload (no file object).
    """
    doc_id = storage_service.save_raw(filename, content)
    return {"doc_id": doc_id, "filename": filename}
