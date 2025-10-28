# models/skipgram_dataset.py
import torch
from torch.utils.data import Dataset

class SkipGramDataset(Dataset):
    def __init__(self, data, window_size=2):
        super().__init__()
        self.data = data
        self.window = window_size
        self.vocab = list(set([token.lower() for sentence in self.data 
                               for token in sentence.split()]))
        self.word2idx = {word: idx for idx, word in enumerate(self.vocab)}
        self.idx2word = {idx: word for word, idx in self.word2idx.items()}
        self.data = self.gen_dataset()
 
    def gen_dataset(self):
        data = []
        for sentence in self.data:
            text = sentence.lower().split()
            for center_idx, center_word in enumerate(text):
                for offset in range(-self.window, self.window + 1):
                    context_idx = center_idx + offset
                    if context_idx < 0 or context_idx >= len(text) or context_idx == center_idx:
                        continue
                    context_word = text[context_idx]
                    data.append((self.word2idx[center_word], self.word2idx[context_word]))
        return data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx]
