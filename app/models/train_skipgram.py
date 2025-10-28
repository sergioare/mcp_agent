import torch
import torch.optim as optim
import torch.nn as nn
from torch.utils.data import DataLoader

from models.skipgram_dataset import SkipGramDataset
from models.skipgram_model import SkipGramModel

def train_skipgram(model, loss_function, optimizer, data_loader, num_epochs=1000):
    for epoch in range(num_epochs):
        total_loss = 0
        for center, context in data_loader:
            center_vector = torch.zeros(len(data_loader.dataset.vocab))
            center_vector[center] = 1.0
            center_vector = center_vector.unsqueeze(0)
            scores = model(center_vector)

            loss = loss_function(scores, torch.tensor([context]))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch + 1}: Loss: {total_loss / len(data_loader)}")


if __name__ == "__main__":
    # Simulación de prueba de entrenamiento
    sentences = [
        "El modelo aprende representaciones de palabras",
        "Las palabras similares tienen embeddings cercanos",
        "El aprendizaje de representaciones es útil"
    ]

    learning_rate = 0.001
    embedding_size = 300
    num_epochs = 10

    dataset = SkipGramDataset(sentences)
    data_loader = DataLoader(dataset, batch_size=1, shuffle=True)
    model = SkipGramModel(len(dataset.vocab), embedding_size=embedding_size)
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    loss_function = nn.CrossEntropyLoss()

    train_skipgram(model, loss_function, optimizer, data_loader, num_epochs=num_epochs)

    torch.save(model.state_dict(), "skipgram_model.pt")
    print("✅ Modelo entrenado y guardado en skipgram_model.pt")
