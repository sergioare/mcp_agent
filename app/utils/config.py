from pydantic import BaseSettings
from pathlib import Path
import torch

class Settings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    MODEL_DIR: Path = BASE_DIR / "models"
    TMP_DIR: Path = BASE_DIR / "tmp"

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: str | None = None

    EMBEDDING_SIZE: int = 300
    WINDOW_SIZE: int = 2
    LEARNING_RATE: float = 0.001
    NUM_EPOCHS: int = 1000
    BATCH_SIZE: int = 1

    CHUNK_SIZE: int = 500
    CHUNK_OVERLAP: int = 50

    LOG_LEVEL: str = "INFO"
    USE_GPU: bool = False

    @property
    def DEVICE(self) -> str:
        return "cuda" if self.USE_GPU and torch.cuda.is_available() else "cpu"

    class Config:
        env_file = ".env"

# Instancia global
settings = Settings()
