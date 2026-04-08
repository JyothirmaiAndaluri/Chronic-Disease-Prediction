from fastapi import APIRouter
from app.services.diabetes_service import predict_diabetes

router = APIRouter()

@router.post("/predict-diabetes")
def diabetes_api(data: dict):
    return {
        "success": True,
        "data": predict_diabetes(data)
    }