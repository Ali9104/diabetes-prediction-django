import os
import joblib
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.db.models import Avg
from django.core.paginator import Paginator # Added for pagination
from .models import Prediction

ML_MODEL_DIR = os.path.join(settings.BASE_DIR, "predictor", "ml_model")

def load_model(name):
    path = os.path.join(ML_MODEL_DIR, name)
    if os.path.exists(path):
        return joblib.load(path)
    return None

logreg_model = load_model("LR.joblib")
rf_model = load_model("RF.joblib")
mlp_model = load_model("NN.joblib")

def get_prediction(model, features):
    if model is None:
        return 0, 0.0
    pred = int(model.predict(features)[0])
    prob = 0.0
    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(features)[0][1] * 100)
    return pred, prob

def home(request):
    results = []
    if request.method == "POST":
        try:
            data = request.POST
            features = pd.DataFrame([{
                "Pregnancies": float(data["pregnancies"]),
                "Glucose": float(data["glucose"]),
                "BloodPressure": float(data["blood_pressure"]),
                "SkinThickness": float(data["skin_thickness"]),
                "Insulin": float(data["insulin"]),
                "BMI": float(data["bmi"]),
                "DiabetesPedigreeFunction": float(data["diabetes_pedigree_function"]),
                "Age": float(data["age"]),
                "Glucose_BMI": float(data["glucose"]) * float(data["bmi"]),
                "Glucose_Age": float(data["glucose"]) * float(data["age"]),
                "BMI_Age": float(data["bmi"]) * float(data["age"]),
                "Pregnancies_Age": float(data["pregnancies"]) * float(data["age"]),
                "Insulin_Glucose": float(data["insulin"]) * float(data["glucose"]),
                "DPF_Age": float(data["diabetes_pedigree_function"]) * float(data["age"]),
            }])

            models_map = {
                "Logistic Regression": logreg_model,
                "Random Forest": rf_model,
                "Neural Network": mlp_model,
            }

            db_results = {}
            for name, model in models_map.items():
                pred, prob = get_prediction(model, features)
                results.append({
                    "name": name,
                    "is_diabetic": pred == 1, # Direct boolean for template
                    "probability": prob,
                })
                db_results[name] = pred

            Prediction.objects.create(
                pregnancies=float(data["pregnancies"]),
                glucose=float(data["glucose"]),
                blood_pressure=float(data["blood_pressure"]),
                skin_thickness=float(data["skin_thickness"]),
                insulin=float(data["insulin"]),
                bmi=float(data["bmi"]),
                dpf=float(data["diabetes_pedigree_function"]),
                age=float(data["age"]),
                result_logreg=db_results["Logistic Regression"],
                result_rf=db_results["Random Forest"],
                result_mlp=db_results["Neural Network"],
            )
        except Exception as e:
            results = [{"name": "Error", "is_diabetic": False, "probability": str(e)}]

    return render(request, "predictor/home.html", {"results": results})

def dashboard(request):
    all_preds = Prediction.objects.all()
    context = {
        'total': all_preds.count(),
        'diabetic': all_preds.filter(result_rf=1).count(),
        'non_diabetic': all_preds.filter(result_rf=0).count(),
        'avg_age': all_preds.aggregate(Avg('age'))['age__avg'] or 0,
        'results': all_preds.order_by('-created_at')[:5]
    }
    return render(request, "predictor/dashboard.html", context)

def history(request):
    prediction_list = Prediction.objects.all().order_by('-created_at')
    paginator = Paginator(prediction_list, 10) # Show 10 per page
    page_number = request.GET.get('page')
    predictions = paginator.get_page(page_number)
    return render(request, "predictor/history.html", {'predictions': predictions})