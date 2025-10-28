# app/services/training_service.py
import os
import json
from typing import List
import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader

from app.adapters.storage.local_file_storage import LocalFileStorageAdapter
from app.utils.config import settings
from app.models.skipgram_dataset import SkipGramDataset
from app.models.skipgram_model import SkipGramModel
from app.models.train_skipgram import train_skipgram

class TrainingService:
    """
    Servicio responsable del entrenamiento del modelo SkipGram:
    - Carga textos desde almacenamiento.
    - Entrena el modelo con PyTorch.
    - Guarda pesos y vocabulario.
    """

    def __init__(self, storage_adapter: LocalFileStorageAdapter | None = None):
        self.storage = storage_adapter or LocalFileStorageAdapter()
        self.model_dir = os.path.dirname(settings.MODEL_PATH)
        os.makedirs(self.model_dir, exist_ok=True)

    def train_on_documents(self, doc_ids: List[str], num_epochs: int = 5, lr: float = 0.001):
        """
        Entrena el modelo SkipGram usando los documentos almacenados localmente.
        """
        # 1️⃣ Reunir texto de todos los documentos
        all_sentences = []
        for doc_id in doc_ids:
            chunks = self.storage.load(doc_id)
            all_sentences.extend(chunks)

        # 2️⃣ Crear dataset y modelo
        dataset = SkipGramDataset(all_sentences)
        data_loader = DataLoader(dataset, batch_size=1, shuffle=True)
        model = SkipGramModel(vocab_size=len(dataset.vocab), embedding_dim=settings.EMBEDDING_DIM)
        optimizer = optim.Adam(model.parameters(), lr=lr)
        loss_function = nn.CrossEntropyLoss()

        # 3️⃣ Entrenar modelo
        train_skipgram(model, loss_function, optimizer, data_loader, num_epochs=num_epochs)

        # 4️⃣ Guardar pesos y vocabulario
        torch.save(model.state_dict(), settings.MODEL_PATH)
        with open(settings.VOCAB_PATH, "w", encoding="utf-8") as f:
            json.dump(dataset.word2idx, f, indent=2)

        print(f"✅ Modelo entrenado y guardado en {settings.MODEL_PATH}")
        print(f"✅ Vocabulario guardado en {settings.VOCAB_PATH}")

        return {
            "vocab_size": len(dataset.vocab),
            "epochs": num_epochs,
            "model_path": settings.MODEL_PATH,
        }
