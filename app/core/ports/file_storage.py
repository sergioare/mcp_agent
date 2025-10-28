from abc import ABC, abstractmethod
from typing import List

class FileStorageInterface(ABC):
    """Interface for document or chunk storage management."""

    @abstractmethod
    def save(self, chunks: List[str]) -> str:
        """Save text chunks and return a document ID."""
        raise NotImplementedError

    @abstractmethod
    def load(self, doc_id: str) -> List[str]:
        """Retrieve chunks from a stored document by ID."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, doc_id: str) -> None:
        """Delete a document from storage."""
        raise NotImplementedError
