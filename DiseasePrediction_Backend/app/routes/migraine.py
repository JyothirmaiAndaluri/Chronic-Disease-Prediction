from fastapi import APIRouter
from app.services.migraine_service import predict_migraine

router = APIRouter()

@router.post("/predict-migraine")
def predict(data: dict):
    result = predict_migraine(data)
    return {"data": result}