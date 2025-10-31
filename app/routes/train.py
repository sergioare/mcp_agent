from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from app.services.training.training_service import TrainingService

router = APIRouter(prefix="/train", tags=["training"])

train_service = TrainingService()

# Definir modelo Pydantic para validación
class TrainRequest(BaseModel):
    doc_ids: List[str]
    epochs: int = 10

@router.post("/")
async def train_model(request: TrainRequest):
    """
    Starts training process for the embedding model using given document IDs.
    This is a simplified endpoint (in a real-world scenario, you might run this asynchronously).
    """
    train_service.train_on_documents(request.doc_ids, request.epochs)
    return {
        "status": "training_started", 
        "doc_ids": request.doc_ids, 
        "epochs": request.epochs
    }