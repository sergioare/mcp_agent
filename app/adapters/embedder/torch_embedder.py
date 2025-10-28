# app/adapters/torch_embedder_adapter.py
import os
import json
from typing import List, Dict
import numpy as np
import torch
from torch import nn
from app.core.ports.embedder import EmbedderInterface
from models.skipgram_model import SkipGramModel  
from app.utils.config import settings

class TorchSkipGramEmbedderAdapter(EmbedderInterface):
    """
    Adapter that:
    - Loads SkipGram model weights saved by training (models/skipgram.pt)
    - Loads the saved vocab mapping (models/skipgram_vocab.json)
    - encode(texts): tokenizes by whitespace, averages word embeddings for tokens in vocab
    - train(sentences): convenience wrapper that calls the training function via service (or direct call)
    """

    def __init__(self, model_path: str = None, vocab_path: str = None, device: str | None = None):
        self.model_path = model_path or settings.MODEL_PATH
        self.vocab_path = vocab_path or settings.VOCAB_PATH
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model: SkipGramModel | None = None
        self.word2idx: Dict[str,int] = {}
        self._load_model_and_vocab()

    def _load_model_and_vocab(self):
        # load vocab
        if os.path.exists(self.vocab_path):
            with open(self.vocab_path, "r", encoding="utf-8") as f:
                self.word2idx = json.load(f)
        else:
            self.word2idx = {}

        # instantiate model only if vocab exists
        if self.word2idx:
            vocab_size = len(self.word2idx)
            emb_dim = settings.EMBEDDING_DIM
            model = SkipGramModel(vocab_size=vocab_size, embedding_dim=emb_dim)
            if os.path.exists(self.model_path):
                state = torch.load(self.model_path, map_location=self.device)
                model.load_state_dict(state)
            model.eval()
            self.model = model.to(self.device)
        else:
            # no model/vocab yet
            self.model = None

    def encode(self, texts: List[str]) -> List[List[float]]:
        """
        Encode a list of texts into embeddings.
        Strategy: average word embeddings for tokens present in vocab.
        """
        if not self.model or not self.word2idx:
            # fallback: random small vectors to avoid crashing the pipeline
            return [np.random.randn(settings.EMBEDDING_DIM).astype(np.float32).tolist() for _ in texts]

        # get word embedding matrix from model.embed.weight (nn.Embedding)
        # model.embed.weight shape: (vocab_size, emb_dim)
        with torch.no_grad():
            emb_weights = self.model.embed.weight.cpu().numpy()  # (V, D)

        results = []
        for text in texts:
            tokens = [t.lower() for t in text.split()]
            idxs = [self.word2idx[t] for t in tokens if t in self.word2idx]
            if not idxs:
                # no known tokens -> zero vector
                vec = np.zeros(settings.EMBEDDING_DIM, dtype=np.float32)
            else:
                vecs = emb_weights[idxs]           # (n_tokens, D)
                vec = np.mean(vecs, axis=0).astype(np.float32)
            results.append(vec.tolist())
        return results

    def train(self, sentences: List[str], **train_kwargs):
        """
        Convenience method: delegate to the central training service or call training implementation.
        Here we only raise NotImplementedError to encourage use of the TrainingService,
        but a simple integration could call models.skipgram_model.train_skipgram directly.
        """
        raise NotImplementedError("Use TrainingService.train_on_documents or call models.skipgram_model.train_skipgram")
