from fastapi import APIRouter
from app.database.db import SessionLocal
from app.database.models import User, LoginLog, DiseaseLog
from sqlalchemy import func
router = APIRouter()

@router.post("/track-disease")
def track_disease(data: dict):

    db = SessionLocal()

    log = DiseaseLog(
        user_id=data["user_id"],
        disease=data["disease"]
    )

    db.add(log)
    db.commit()

    return {"message": "tracked"}
@router.get("/analytics")
def get_analytics():

    db = SessionLocal()

    total_users = db.query(User).count()
    total_logins = db.query(LoginLog).count()

    disease_counts = db.query(
        DiseaseLog.disease,
        func.count(DiseaseLog.id)
    ).group_by(DiseaseLog.disease).all()

    # ✅ FIX HERE
    disease_counts = [
        {"disease": d[0], "count": d[1]}
        for d in disease_counts
    ]

    return {
        "total_users": total_users,
        "total_logins": total_logins,
        "disease_stats": disease_counts
    }