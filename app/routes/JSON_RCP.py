from fastapi import APIRouter, Request
from app.services.embedding_service import EmbeddingService
from app.services.storage_service import StorageService
from app.services.training_service import TrainingService
import uuid
from typing import Dict, Any

EMBED_SVC = EmbeddingService()
STORAGE_SVC = StorageService()
TRAIN_SVC = TrainingService()

router = APIRouter(prefix="/mcp")

@router.post("/mcp")
async def mcp_http_entry(request: Request) -> Dict[str, Any]:
    """
    Accepts JSON-RPC 2.0 POSTs and routes to configured services.
    Expected jsonrpc request:
    { "jsonrpc":"2.0", "method":"<method>", "params":{...}, "id":"<id>" }
    Supported methods:
      - upload_document: params { "filename": str, "content": str }
      - generate_embeddings: params { "doc_id": str, "reindex": bool? }
      - search_embeddings: params { "query": str, "top_k": int? }
      - train_model: params { "doc_ids": [str], "epochs": int? }
    """
    payload = await request.json()
    method = payload.get("method")
    params = payload.get("params", {})
    req_id = payload.get("id", str(uuid.uuid4()))

    try:
        if method == "upload_document":
            filename = params.get("filename")
            content = params.get("content")
            if not filename or content is None:
                return {"jsonrpc":"2.0", "error": {"code":400, "message":"Missing filename or content"}, "id": req_id}
            doc_id = STORAGE_SVC.save_raw(filename, content)
            return {"jsonrpc":"2.0", "result": {"doc_id": doc_id}, "id": req_id}

        if method == "generate_embeddings":
            doc_id = params.get("doc_id")
            if not doc_id:
                return {"jsonrpc":"2.0", "error": {"code":400, "message":"Missing doc_id"}, "id": req_id}
            chunks = STORAGE_SVC.get_chunks(doc_id)
            out = EMBED_SVC.process_and_store(doc_id, chunks)
            return {"jsonrpc":"2.0", "result": out, "id": req_id}

        if method == "search_embeddings":
            query = params.get("query", "")
            top_k = int(params.get("top_k", 5))
            if not query:
                return {"jsonrpc":"2.0", "error": {"code":400, "message":"Missing query"}, "id": req_id}
            res = EMBED_SVC.semantic_search(query, top_k=top_k)
            return {"jsonrpc":"2.0", "result": {"results": res}, "id": req_id}

        if method == "train_model":
            doc_ids = params.get("doc_ids", [])
            epochs = int(params.get("epochs", 10))
            TRAIN_SVC.train_on_documents(doc_ids, epochs)
            return {"jsonrpc":"2.0", "result": {"status":"training_started"}, "id": req_id}

        return {"jsonrpc":"2.0", "error": {"code":404, "message":"Unknown method"}, "id": req_id}
    except Exception as e:
        return {"jsonrpc":"2.0", "error": {"code":500, "message": str(e)}, "id": req_id}
