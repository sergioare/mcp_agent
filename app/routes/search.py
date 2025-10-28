from fastapi import APIRouter, Query
from app.services.embedding.embedding_service import EmbeddingService

router = APIRouter(prefix="/search", tags=["search"])

embed_service = EmbeddingService()

@router.get("/")
async def search_embeddings(query: str = Query(...), top_k: int = Query(5)):
    """
    Performs a semantic search over stored embeddings.
    Returns the most similar text chunks.
    """
    results = embed_service.semantic_search(query, top_k=top_k)
    return {"query": query, "top_k": top_k, "results": results}
