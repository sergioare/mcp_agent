# app/adapters/redis_vector_db_adapter.py
import redis
import numpy as np
import json
from typing import List, Dict, Any
from app.core.ports.vector_db import VectorDBInterface
from app.utils.config import settings

class RedisVectorDBAdapter(VectorDBInterface):
    """
    Simple Redis adapter storing each vector as a binary blob or JSON and performing
    linear scan similarity queries. For production, prefer Redis 7.2+ vector search
    (FT.CREATE ... WITH VECTOR) or a dedicated vector DB (Qdrant, Milvus).
    """

    def __init__(self, host: str = None, port: int = None, db: int = None):
        host = host or settings.REDIS_HOST
        port = port or settings.REDIS_PORT
        db = db or settings.REDIS_DB
        # decode_responses=False to get bytes for vector blobs if used
        self.client = redis.Redis(host=host, port=port, db=db, decode_responses=False)
        self.ns_prefix = "vec:"  # key prefix

    def insert(self, id: str, vector: List[float], metadata: Dict[str, Any] = None) -> None:
        key = f"{self.ns_prefix}{id}"
        # store vector as bytes (float32) and metadata as json in a hash
        arr = np.array(vector, dtype=np.float32)
        self.client.hset(key, mapping={
            "vector": arr.tobytes(),
            "metadata": json.dumps(metadata or {})
        })

    def query(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        q = np.array(vector, dtype=np.float32)
        keys = self.client.keys(f"{self.ns_prefix}*")
        results = []
        for k in keys:
            raw = self.client.hget(k, "vector")
            if not raw:
                continue
            vec = np.frombuffer(raw, dtype=np.float32)
            denom = (np.linalg.norm(q) * np.linalg.norm(vec)) + 1e-12
            score = float(np.dot(q, vec) / denom)
            meta_raw = self.client.hget(k, "metadata")
            try:
                meta = json.loads(meta_raw) if meta_raw else {}
            except Exception:
                meta = {}
            key_decoded = k.decode() if isinstance(k, bytes) else str(k)
            id_only = key_decoded.replace(self.ns_prefix, "")
            results.append({"id": id_only, "score": score, "metadata": meta})
        # sort desc by score
        results.sort(key=lambda r: r["score"], reverse=True)
        return results[:top_k]

    def delete(self, id: str) -> None:
        key = f"{self.ns_prefix}{id}"
        self.client.delete(key)

    def persist(self) -> None:
        # Redis persists per its config; no-op placeholder
        return

    def load(self) -> None:
        # No-op: Redis holds data; but you could implement reindexing helper here
        return
