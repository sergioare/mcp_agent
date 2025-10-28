import torch
import torch.nn as nn

class SkipGramModel(nn.Module):
    def __init__(self, vocab_size, embedding_size):
        super().__init__()
        self.embed_layer = nn.Linear(vocab_size, embedding_size, bias=False)
        self.output_layer = nn.Linear(embedding_size, vocab_size)

    def forward(self, x):
        return self.output_layer(self.embed_layer(x))
