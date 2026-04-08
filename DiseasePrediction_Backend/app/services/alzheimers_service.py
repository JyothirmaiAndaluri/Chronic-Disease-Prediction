import joblib
import pandas as pd
import numpy as np

# ✅ Load model
model_data = joblib.load("app/alzheimers_xai_model.pkl")

model = model_data["model"]
explainer = model_data["explainer"]
features = model_data["features"]


# ✅ Risk level
def get_risk_level(prob):
    if prob < 25:
        return "LOW"
    elif prob < 50:
        return "MODERATE"
    elif prob < 75:
        return "HIGH"
    else:
        return "VERY HIGH"


# ✅ SHAP Explanation
def get_explanation(data):
    X_input = pd.DataFrame([data])[features]

    shap_values = explainer.shap_values(X_input)

    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]
    else:
        shap_vals = shap_values[0]

    shap_vals = np.array(shap_vals).flatten()

    drivers = []
    inhibitors = []

    for i, name in enumerate(features):
        val = shap_vals[i]

        # ignore useless fields
        if name in ["Gender", "Ethnicity", "EducationLevel"]:
            continue

        # 🔴 Risk factors
        if val > 0 and data.get(name, 0) == 1:
            drivers.append(name)

        # 🟢 Protective
        elif val < 0:
            inhibitors.append(name)

    return drivers[:5], inhibitors[:3]


# ✅ MAIN FUNCTION
def predict_alzheimers(patient: dict):

    # fill missing features
    data = {f: patient.get(f, 0) for f in features}

    df = pd.DataFrame([data])

    prob = model.predict_proba(df)[0][1]
    prob_pct = round(prob * 100, 2)

    level = get_risk_level(prob_pct)

    drivers, inhibitors = get_explanation(data)

    return {
        "prediction": "AT RISK" if prob >= 0.5 else "NOT AT RISK",
        "risk_probability": prob_pct,
        "risk_level": level,
        "top_drivers": drivers,
        "protective_factors": inhibitors
    }