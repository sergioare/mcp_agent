import regex as re  
import unicodedata

def clean_text(text: str) -> str:
    """
    Limpia texto eliminando caracteres no válidos pero preservando:
    - Letras con acentos, ñ, ü, diéresis, etc.
    - Números y puntuación básica.
    - Espacios normales.

    Ejemplo:
        "¡Hola, pingüino! ¿Cómo estás?" 
        → "¡Hola, pingüino! ¿Cómo estás?"
    """
    # Normaliza para conservar acentos y símbolos Unicode en forma consistente
    text = unicodedata.normalize("NFC", text)

    # Elimina saltos de línea múltiples y espacios redundantes
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\s{2,}', ' ', text)

    # Conserva letras (de cualquier idioma), marcas diacríticas, números, espacios y puntuación básica
    text = re.sub(r"[^\p{L}\p{M}0-9\s.,!?;:()\-¿¡]", "", text)

    return text.strip()


def normalize_whitespace(text: str) -> str:
    """
    Normaliza espacios, tabs y saltos de línea.
    """
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def to_lower(text: str) -> str:
    """
    Convierte texto a minúsculas manteniendo caracteres especiales.
    """
    return text.lower()
