from typing import List


def split_into_chunks(
    text: str,
    max_chunk_size: int = 500,
    overlap: int = 50
) -> List[str]:
    """
    Divide un texto largo en fragmentos (chunks) de tamaño máximo `max_chunk_size`.
    Usa un solapamiento entre fragmentos para mantener el contexto.

    Ejemplo:
    - max_chunk_size = 500
    - overlap = 50  → cada chunk comparte 50 caracteres con el anterior
    """
    if not text or not text.strip():
        return []

    text = text.strip().replace("\n", " ")

    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + max_chunk_size, text_length)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start += max_chunk_size - overlap

    return chunks
