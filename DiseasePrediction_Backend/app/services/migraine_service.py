import joblib
import pandas as pd
import numpy as np
from pathlib import Path
import json
import shap

# ===============================
# LOAD FILES
# ===============================
BASE_DIR = Path(__file__).resolve().parent.parent

model = joblib.load(BASE_DIR / "migraine_model_final.pkl")
scaler = joblib.load(BASE_DIR / "migraine_scaler_final.pkl")
label_encoder = joblib.load(BASE_DIR / "migraine_label_encoder.pkl")

with open(BASE_DIR / "migraine_model_meta.json") as f:
    meta = json.load(f)

features = meta["features"]
classes = meta["classes"]
risk_map = meta["risk_map"]

# ===============================
# SHAP EXPLAINER (XGBoost)
# ===============================
explainer = shap.TreeExplainer(model)

# ===============================
# PREDICTION FUNCTION
# ===============================
def predict_migraine(data: dict):

    row = pd.DataFrame([{f: data.get(f, 0) for f in features}])

    # Scale
    row_scaled = scaler.transform(row)

    # Predict
    pred = model.predict(row_scaled)[0]
    pred_type = label_encoder.inverse_transform([pred])[0]

    proba = model.predict_proba(row_scaled)[0]
    confidence = float(proba[pred] * 100)

    # Risk mapping
    risk_info = risk_map[pred_type]
    base_score = risk_info["score"]

    final_score = round(min(99, max(5, base_score * (confidence/100) + base_score*0.3)), 2)

    # ===============================
    # SHAP EXPLANATION
    # ===============================
    shap_values = explainer.shap_values(row_scaled)

    if isinstance(shap_values, list):
        vals = shap_values[pred][0]
    else:
        vals = shap_values[0]

    vals = np.array(vals).flatten()

    combined = list(zip(features, vals))
    combined = sorted(combined, key=lambda x: abs(float(x[1])), reverse=True)


    drivers = [f for f, v in combined[:4]]
    protective = [f for f, v in combined[-3:]]

    return {
        "prediction": pred_type,
        "confidence": round(confidence, 2),
        "risk_score": final_score,
        "risk_level": risk_info["level"],
        "top_drivers": drivers,
        "protective_factors": protective
    }