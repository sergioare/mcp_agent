from app.core.ports.embedder import EmbedderInterface

class EmbedderCore:
    """Generic embedding orchestrator that delegates to the selected adapter."""

    def __init__(self, embedder: EmbedderInterface):
        self.embedder = embedder

    def generate_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        return self.embedder.encode(texts)
