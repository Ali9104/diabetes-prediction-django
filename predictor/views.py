import os
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render

ML_MODEL_DIR = os.path.join(settings.BASE_DIR, "predictor", "ml_model")

logreg_model = None
rf_model = None
mlp_model = None

logreg_path = os.path.join(ML_MODEL_DIR, "best_logreg_pipeline.joblib")
rf_path = os.path.join(ML_MODEL_DIR, "best_logreg_pipeline_v2.joblib")
mlp_path = os.path.join(ML_MODEL_DIR, "best_logreg_pipeline_v3.joblib")

if os.path.exists(logreg_path):
    logreg_model = joblib.load(logreg_path)

if os.path.exists(rf_path):
    rf_model = joblib.load(rf_path)

if os.path.exists(mlp_path):
    mlp_model = joblib.load(mlp_path)


def format_result(model, features, model_name):
    if model is None:
        return {
            "name": model_name,
            "status": "Model not available",
            "probability": None,
        }

    pred = model.predict(features)[0]
    prob = None

    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(features)[0][1] * 100)

    return {
        "name": model_name,
        "status": "Diabetic" if pred == 1 else "Non-Diabetic",
        "probability": prob,
    }


def home(request):
    results = []

    if request.method == "POST":
        try:
            pregnancies = float(request.POST.get("pregnancies", 0))
            glucose = float(request.POST.get("glucose", 0))
            blood_pressure = float(request.POST.get("blood_pressure", 0))
            skin_thickness = float(request.POST.get("skin_thickness", 0))
            insulin = float(request.POST.get("insulin", 0))
            bmi = float(request.POST.get("bmi", 0))
            dpf = float(request.POST.get("diabetes_pedigree_function", 0))
            age = float(request.POST.get("age", 0))

            features = pd.DataFrame([{
                "Pregnancies": pregnancies,
                "Glucose": glucose,
                "BloodPressure": blood_pressure,
                "SkinThickness": skin_thickness,
                "Insulin": insulin,
                "BMI": bmi,
                "DiabetesPedigreeFunction": dpf,
                "Age": age,

                "Glucose_BMI": glucose * bmi,
                "Glucose_Age": glucose * age,
                "BMI_Age": bmi * age,
                "Pregnancies_Age": pregnancies * age,
                "Insulin_Glucose": insulin * glucose,
                "DPF_Age": dpf * age,
            }])

            results.append(format_result(logreg_model, features, "Logistic Regression"))
            results.append(format_result(rf_model, features, "Random Forest"))
            results.append(format_result(mlp_model, features, "Neural Network"))

        except Exception as e:
            results = [{
                "name": "Input Error",
                "status": str(e),
                "probability": None,
            }]

    return render(request, "predictor/home.html", {"results": results})