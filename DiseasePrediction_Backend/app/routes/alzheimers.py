from fastapi import APIRouter
from app.services.alzheimers_service import predict_alzheimers

router = APIRouter()

@router.post("/predict-alzheimers")
def predict(data: dict):
    return {"data": predict_alzheimers(data)}