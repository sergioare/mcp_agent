from typing import List, Dict, Any
from app.adapters.embedder.torch_embedder import TorchSkipGramEmbedderAdapter
from app.adapters.vector_db.redis_db import RedisVectorDBAdapter
from app.utils.file_loader import extract_text_from_file
from app.utils.chunk_splitter import split_into_chunks


class EmbeddingService:
    """
    Servicio encargado de:
    - Generar embeddings a partir de texto usando el modelo SkipGram.
    - Guardar embeddings en la base vectorial (Redis).
    - Consultar similitudes de embeddings.
    - Procesar archivos (PDF, DOCX, TXT, etc.) para generar embeddings desde su contenido.
    """

    def __init__(
        self,
        embedder: TorchSkipGramEmbedderAdapter | None = None,
        vector_db: RedisVectorDBAdapter | None = None
    ):
        self.embedder = embedder or TorchSkipGramEmbedderAdapter()
        self.vector_db = vector_db or RedisVectorDBAdapter()

    # -------------------------------------------------------------------------
    # 🔹 Embeddings desde texto directamente
    # -------------------------------------------------------------------------
    def embed_and_store(
        self, doc_id: str, chunks: List[str], metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Genera embeddings para cada chunk y los guarda en Redis con metadata.
        Devuelve una lista con los IDs insertados y los metadatos.
        """
        vectors = self.embedder.encode(chunks)
        responses = []
        for i, vec in enumerate(vectors):
            chunk_id = f"{doc_id}_chunk_{i}"
            meta = (metadata or {}).copy()
            meta.update({"doc_id": doc_id, "chunk_index": i})
            self.vector_db.insert(chunk_id, vec, meta)
            responses.append({"chunk_id": chunk_id, "metadata": meta})
        return responses

    # -------------------------------------------------------------------------
    # 🔹 Búsqueda por similitud
    # -------------------------------------------------------------------------
    def query_similar_chunks(
        self, query_text: str, top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Busca los chunks más similares al texto de consulta.
        """
        vector = self.embedder.encode([query_text])[0]
        results = self.vector_db.query(vector, top_k=top_k)
        return results

    # -------------------------------------------------------------------------
    # 🔹 Procesar archivo completo y generar embeddings desde su contenido
    # -------------------------------------------------------------------------
    def process_and_embed_file(
        self, file_path: str, doc_id: str, metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """
        1. Extrae texto desde el archivo (PDF, DOCX, TXT, etc.).
        2. Divide el texto en chunks manejables.
        3. Genera embeddings para cada chunk.
        4. Los almacena en la base vectorial (Redis).
        """
        
        text = extract_text_from_file(file_path)

        chunks = split_into_chunks(text)

        # Validación básica
        if not chunks:
            raise ValueError(f"No se generaron chunks válidos desde el archivo: {file_path}")

        # 🔸 (3) Generar y almacenar embeddings
        return self.embed_and_store(doc_id, chunks, metadata)
