from typing import List
from app.adapters.storage.local_file_storage import LocalFileStorageAdapter
from app.utils.chunk_splitter import split_into_chunks

class StorageService:
    """
    Encapsula la lógica de almacenamiento de archivos (documentos y chunks).
    No depende directamente del sistema de archivos — solo del adapter.
    """

    def __init__(self, adapter: LocalFileStorageAdapter | None = None):
        self.adapter = adapter or LocalFileStorageAdapter()

    def save_raw(self, filename: str, content: str) -> str:
        """
        Recibe contenido crudo, lo divide en chunks y lo guarda.
        Retorna el doc_id generado.
        """
        chunks = split_into_chunks(content)
        if not chunks:
            raise ValueError(f"No se pudieron generar chunks del archivo: {filename}")
        return self.adapter.save(chunks)

    def get_chunks(self, doc_id: str) -> List[str]:
        """
        Obtiene los chunks de un documento por su ID.
        Alias de load_document para compatibilidad con routes.
        """
        return self.adapter.load(doc_id)

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