from app.core.ports.vector_db import VectorDBInterface

class IndexerCore:
    """Handles vector insertion, search, and deletion in the configured vector DB."""

    def __init__(self, vector_db: VectorDBInterface):
        self.vector_db = vector_db

    def index_vectors(self, doc_id: str, vectors: list[list[float]], metadata_list: list[dict]):
        """Insert vectors into the database."""
        for vec, meta in zip(vectors, metadata_list):
            self.vector_db.insert(id=f"{doc_id}_{meta.get('chunk_id')}", vector=vec, metadata=meta)

    def search_vectors(self, query_vector: list[float], top_k: int = 5):
        """Query similar vectors."""
        return self.vector_db.query(query_vector, top_k=top_k)

    def delete_document(self, doc_id: str):
        """Delete all vectors associated with a document."""
        self.vector_db.delete(doc_id)
