from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorDBInterface(ABC):
    """Interface that defines the contract for any vector database (e.g., Redis, FAISS, Pinecone)."""

    @abstractmethod
    def insert(self, id: str, vector: List[float], metadata: Dict[str, Any]) -> None:
        """Insert a new vector with its metadata into the database."""
        raise NotImplementedError

    @abstractmethod
    def query(self, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Query the top_k most similar vectors."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: str) -> None:
        """Remove a vector by its ID."""
        raise NotImplementedError

    @abstractmethod
    def persist(self) -> None:
        """Persist the index to disk or remote storage."""
        raise NotImplementedError

    @abstractmethod
    def load(self) -> None:
        """Load a persisted index into memory."""
        raise NotImplementedError
