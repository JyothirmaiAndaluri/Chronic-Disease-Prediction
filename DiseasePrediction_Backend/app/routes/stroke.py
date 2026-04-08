from fastapi import APIRouter
from app.services.stroke_service import predict_stroke

router = APIRouter()

@router.post("/predict-stroke")
def predict(data: dict):
    result = predict_stroke(data)
    return {"data": result}