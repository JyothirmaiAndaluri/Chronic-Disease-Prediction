import joblib
import pandas as pd
import numpy as np

# ✅ Load model
artifact = joblib.load("app/diabetes_xai_model.pkl")
model = artifact["model"]
explainer = artifact["explainer"]
features = artifact["features"]

print("FEATURE ORDER:", features)
# 🔥 SHAP explanation
def get_explanation(data):
    import numpy as np

    # Create input row in correct feature order
    X_input = pd.DataFrame([data])[features]

    # Get SHAP values
    shap_values = explainer.shap_values(X_input)

    # Handle different SHAP formats
    if isinstance(shap_values, list):
        shap_vals = shap_values[1][0]
    else:
        shap_vals = shap_values[0]

    # Store feature importance
    feature_importance = []

    for i, name in enumerate(features):
        val = np.array(shap_vals[i]).flatten()[0]
        feature_importance.append((name, abs(val)))

    # Sort by importance
    feature_importance.sort(key=lambda x: x[1], reverse=True)

    # Take top 5 important features
    top_features = [f[0] for f in feature_importance[:5]]

    # Separate drivers and inhibitors
    drivers = [f for f in top_features if data.get(f) == 2]
    inhibitors = [f for f in top_features if data.get(f) == 1]

    return drivers, inhibitors


# 🔥 Prediction function
def predict_diabetes(data: dict):
    row = pd.DataFrame([data])[features]

    proba = float(model.predict_proba(row)[0][1])
    proba = max(proba, 0.02)

    if proba >= 0.75:
        level = "VERY HIGH"
    elif proba >= 0.55:
        level = "HIGH"
    elif proba >= 0.30:
        level = "MODERATE"
    else:
        level = "LOW"

    drivers, inhibitors = get_explanation(data)

    return {
        "prediction": "POSITIVE" if proba >= 0.3 else "NEGATIVE",
        "risk_probability": round(proba * 100, 2),
        "risk_level": level,
        "top_drivers": drivers,
        "protective_factors": inhibitors
    }