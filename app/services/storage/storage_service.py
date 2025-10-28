from typing import List
from app.adapters.storage.local_file_storage import LocalFileStorageAdapter

class StorageService:
    """
    Encapsula la lógica de almacenamiento de archivos (documentos y chunks).
    No depende directamente del sistema de archivos — solo del adapter.
    """

    def __init__(self, adapter: LocalFileStorageAdapter | None = None):
        self.adapter = adapter or LocalFileStorageAdapter()

    def save_document(self, chunks: List[str]) -> str:
        """
        Guarda un documento dividido en chunks y retorna su ID único.
        """
        return self.adapter.save(chunks)

    def load_document(self, doc_id: str) -> List[str]:
        """
        Carga un documento (lista de chunks) desde su ID.
        """
        return self.adapter.load(doc_id)

    def delete_document(self, doc_id: str) -> None:
        """
        Elimina archivos asociados a un documento.
        """
        self.adapter.delete(doc_id)
