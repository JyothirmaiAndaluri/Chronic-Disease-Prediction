import joblib
import pandas as pd
from pathlib import Path

# Get project root (app folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Correct paths
import numpy as np

explainer = joblib.load(BASE_DIR/ "lung_cancer_explainer.pkl")
model_path = BASE_DIR / "lung_cancer_model.pkl"
features_path = BASE_DIR / "feature_columns.pkl"

# Load files
model = joblib.load(model_path)
features = joblib.load(features_path)
def get_explanation(data):
    X_input = pd.DataFrame([data])[features]

    shap_values = explainer.shap_values(X_input)

    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]
    else:
        shap_vals = shap_values[0]

    # ✅ FIX HERE
    shap_vals = np.array(shap_vals).flatten()

    combined = list(zip(features, shap_vals))

    # Now sorting works
    combined = sorted(combined, key=lambda x: abs(x[1]), reverse=True)

    drivers = []
    inhibitors = []

    for name, val in combined:
        if data.get(name) == 2 and val > 0:
            drivers.append(name)
        elif data.get(name) == 1 and val < 0:
            inhibitors.append(name)

    return drivers[:5], inhibitors[:3]

def predict_lung(data: dict):

    row = pd.DataFrame([[data.get(f, 1) for f in features]], columns=features)

    proba = model.predict_proba(row)[0][1]

    if proba >= 0.7:
        level = "HIGH"
    elif proba >= 0.4:
        level = "MEDIUM"
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