import torch
import torch.nn as nn

class SkipGramModel(nn.Module):
    def __init__(self, vocab_size, embedding_dim):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, embedding_dim)
        self.output = nn.Linear(embedding_dim, vocab_size)
    
    def forward(self, center_ids):
        embeds = self.embed(center_ids)
        scores = self.output(embeds)
        return scores