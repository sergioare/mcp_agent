# app/routes/embed.py
from fastapi import APIRouter, HTTPException
from app.services.embedding.embedding_service import EmbeddingService
from app.services.storage.storage_service import StorageService

router = APIRouter(prefix="/embed", tags=["embedding"])

embed_service = EmbeddingService()
storage_service = StorageService()

@router.post("/{doc_id}")
async def generate_embeddings(doc_id: str):
    """
    Generates embeddings for a given document ID and stores them in Redis.
    """
    chunks = storage_service.get_chunks(doc_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="Document not found or empty")

    result = embed_service.embed_and_store(doc_id, chunks)
    return {"status": "ok", "processed_chunks": len(chunks), "result": result}
