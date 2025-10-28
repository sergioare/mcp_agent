from app.core.ports.embedder import EmbedderInterface

class ModelTrainerCore:
    """Handles training or fine-tuning embeddings models."""

    def __init__(self, embedder: EmbedderInterface):
        self.embedder = embedder

    def train(self, sentences: list[str]) -> None:
        """
        Calls the underlying model training method.
        This can be a PyTorch model, a transformer fine-tune, etc.
        """
        self.embedder.train(sentences)
