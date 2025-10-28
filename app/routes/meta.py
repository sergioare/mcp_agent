# app/routes/meta.py
from fastapi import APIRouter

router = APIRouter(prefix="/meta", tags=["meta"])

META = {
    "name": "Landing Agent MCP",
    "version": "1.0.0",
    "description": "Agent responsible for handling document ingestion, embedding, and semantic search.",
    "capabilities": {
        "upload": True,
        "embedding": True,
        "search": True,
        "training": True
    },
    "interfaces": ["REST", "JSON-RPC"]
}

@router.get("/")
async def get_meta():
    """
    Returns basic metadata about the MCP Agent, used by orchestrators
    to understand what this server can do.
    """
    return META
