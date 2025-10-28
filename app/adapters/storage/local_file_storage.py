import os
import uuid
from typing import List
from app.core.ports.file_storage import FileStorageInterface

class LocalFileStorageAdapter(FileStorageInterface):
    """
    Simple local file storage adapter.
    - Saves raw text into data/docs/<doc_id>.txt
    - Saves chunks into data/docs/<doc_id>.chunks (one chunk per line)
    """

    def __init__(self, base_path: str = "data/docs"):
        self.base_path = base_path
        os.makedirs(self.base_path, exist_ok=True)

    def save(self, chunks: List[str]) -> str:
        """
        Save list of chunks and return generated doc_id.
        """
        doc_id = str(uuid.uuid4())
        raw_path = os.path.join(self.base_path, f"{doc_id}.txt")
        chunks_path = os.path.join(self.base_path, f"{doc_id}.chunks")
        # Save raw concatenated
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write("\n".join(chunks))
        # Save chunks separately (fallback)
        with open(chunks_path, "w", encoding="utf-8") as f:
            f.write("\n---CHUNK---\n".join(chunks))
        return doc_id

    def load(self, doc_id: str) -> List[str]:
        """
        Return list of chunks for a given doc_id.
        Prefer the .chunks file; fall back to .txt split by newline.
        """
        chunks_path = os.path.join(self.base_path, f"{doc_id}.chunks")
        raw_path = os.path.join(self.base_path, f"{doc_id}.txt")
        if os.path.exists(chunks_path):
            with open(chunks_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content.split("\n---CHUNK---\n")
        if os.path.exists(raw_path):
            with open(raw_path, "r", encoding="utf-8") as f:
                text = f.read()
            # fallback splitter: simple newline split
            return [p for p in text.split("\n") if p.strip()]
        return []

    def delete(self, doc_id: str) -> None:
        """
        Delete stored files for a document.
        """
        for ext in (".chunks", ".txt"):
            path = os.path.join(self.base_path, f"{doc_id}{ext}")
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception:
                pass
