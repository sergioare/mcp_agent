from app.utils.file_loader import load_text_from_file
from app.utils.text_splitter import split_text_into_chunks

class DocumentProcessor:
    """Handles document cleaning, extraction, and chunking."""

    def __init__(self):
        pass

    def process(self, file_path: str) -> list[str]:
        """
        Load, clean, and split a document into chunks for embedding.
        """
        text = load_text_from_file(file_path)
        chunks = split_text_into_chunks(text)
        return chunks
