from fastapi import APIRouter
from app.services.lung_service import predict_lung

router = APIRouter()

@router.post("/predict-lung")
def predict(data: dict):
    result = predict_lung(data)
    return {"data": result}