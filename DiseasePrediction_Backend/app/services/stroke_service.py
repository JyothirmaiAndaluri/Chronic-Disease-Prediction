import joblib
import pandas as pd
import numpy as np
from pathlib import Path

# Base path
BASE_DIR = Path(__file__).resolve().parent.parent

# Load model
artifact = joblib.load(BASE_DIR / "stroke_risk_model_v2.pkl")

model = artifact["model"]
features = artifact["features"]

# ===============================
# 🧠 EXPLANATION FUNCTION
# ===============================
def get_explanation(data):

    row = pd.DataFrame([{f: data.get(f, 0) for f in features}])

    proba = model.predict_proba(row)[0][1]

    # Simple contribution logic (same as your colab)
    present = [f for f in features if f != "Age" and data.get(f, 0) == 1]
    absent = [f for f in features if f != "Age" and data.get(f, 0) == 0]

    # Sort based on importance (basic logic)
    drivers = present[:5]
    inhibitors = absent[:3]

    return drivers, inhibitors


# ===============================
# 🔮 PREDICTION FUNCTION
# ===============================
def predict_stroke(data: dict):

    row = pd.DataFrame([{f: data.get(f, 0) for f in features}])

    proba = float(model.predict_proba(row)[0][1])

    # ✅ Prevent 0% / 100% extreme
    proba = np.clip(proba, 0.01, 0.99)

    # Risk level
    if proba >= 0.70:
        level = "HIGH"
    elif proba >= 0.35:
        level = "MEDIUM"
    elif proba >= 0.15:
        level = "LOW-MEDIUM"
    else:
        level = "LOW"

    drivers, inhibitors = get_explanation(data)

    return {
        "prediction": "AT RISK" if proba >= 0.5 else "NOT AT RISK",
        "risk_probability": round(proba * 100, 2),
        "risk_level": level,
        "top_drivers": drivers,
        "protective_factors": inhibitors
    }