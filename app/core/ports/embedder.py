from abc import ABC, abstractmethod
from typing import List

class EmbedderInterface(ABC):
    """Interface that defines the contract for text embedding generators."""

    @abstractmethod
    def encode(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for a list of texts."""
        raise NotImplementedError

    @abstractmethod
    def train(self, texts: List[str]) -> None:
        """Optional: train or fine-tune the model."""
        raise NotImplementedError