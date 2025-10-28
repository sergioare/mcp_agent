from typing import Union
from pathlib import Path

from PyPDF2 import PdfReader
from docx import Document


def extract_text_from_file(file_path: Union[str, Path]) -> str:
    """
    Extrae texto de un archivo .txt, .pdf o .docx y devuelve un string con el contenido limpio.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f"El archivo no existe: {file_path}")

    ext = file_path.suffix.lower()
    if ext == ".txt":
        return _read_txt(file_path)
    elif ext == ".pdf":
        return _read_pdf(file_path)
    elif ext == ".docx":
        return _read_docx(file_path)
    else:
        raise ValueError(f"Tipo de archivo no soportado: {ext}")


# ---------------------------------------------------------------
# Lectores individuales por tipo
# ---------------------------------------------------------------

def _read_txt(path: Path) -> str:
    """Lee un archivo de texto plano."""
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read().strip()


def _read_pdf(path: Path) -> str:
    """Lee texto de un archivo PDF usando PyPDF2."""
    text = ""
    with open(path, "rb") as f:
        reader = PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()


def _read_docx(path: Path) -> str:
    """Lee texto de un archivo Word (.docx)."""
    doc = Document(path)
    text = "\n".join(p.text for p in doc.paragraphs)
    return text.strip()
