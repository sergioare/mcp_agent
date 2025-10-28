from fastapi import APIRouter
from app.services.training_service import TrainingService

router = APIRouter(prefix="/train", tags=["training"])

train_service = TrainingService()

@router.post("/")
async def train_model(doc_ids: list[str], epochs: int = 10):
    """
    Starts training process for the embedding model using given document IDs.
    This is a simplified endpoint (in a real-world scenario, you might run this asynchronously).
    """
    train_service.train_on_documents(doc_ids, epochs)
    return {"status": "training_started", "doc_ids": doc_ids, "epochs": epochs}
