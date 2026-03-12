import os
import joblib
import pandas as pd

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .models import Patient, Prediction
from .forms import PatientForm, PredictionInputForm


ML_MODEL_DIR = os.path.join(settings.BASE_DIR, "predictor", "ml_model")


def load_model(name):
    path = os.path.join(ML_MODEL_DIR, name)
    if os.path.exists(path):
        return joblib.load(path)
    return None


logreg_model = load_model("LR.joblib")
rf_model = load_model("RF.joblib")
mlp_model = load_model("NN.joblib")

def logout_view(request):
    logout(request)
    return redirect('login')

def get_prediction(model, features):
    if model is None:
        return 0, 0.0

    pred = int(model.predict(features)[0])
    prob = 0.0

    if hasattr(model, "predict_proba"):
        prob = float(model.predict_proba(features)[0][1] * 100)

    return pred, prob


def build_features(cleaned_data):
    return pd.DataFrame([{
        "Pregnancies": float(cleaned_data["pregnancies"]),
        "Glucose": float(cleaned_data["glucose"]),
        "BloodPressure": float(cleaned_data["blood_pressure"]),
        "SkinThickness": float(cleaned_data["skin_thickness"]),
        "Insulin": float(cleaned_data["insulin"]),
        "BMI": float(cleaned_data["bmi"]),
        "DiabetesPedigreeFunction": float(cleaned_data["diabetes_pedigree_function"]),
        "Age": float(cleaned_data["age"]),
        "Glucose_BMI": float(cleaned_data["glucose"]) * float(cleaned_data["bmi"]),
        "Glucose_Age": float(cleaned_data["glucose"]) * float(cleaned_data["age"]),
        "BMI_Age": float(cleaned_data["bmi"]) * float(cleaned_data["age"]),
        "Pregnancies_Age": float(cleaned_data["pregnancies"]) * float(cleaned_data["age"]),
        "Insulin_Glucose": float(cleaned_data["insulin"]) * float(cleaned_data["glucose"]),
        "DPF_Age": float(cleaned_data["diabetes_pedigree_function"]) * float(cleaned_data["age"]),
    }])


@login_required
def home(request):
    return redirect("dashboard")


@login_required
def dashboard(request):
    my_predictions = Prediction.objects.filter(patient__doctor=request.user)
    my_patients = Patient.objects.filter(doctor=request.user)

    context = {
        "total_patients": my_patients.count(),
        "total_tests": my_predictions.count(),
        "diabetic": my_predictions.filter(result_rf=1).count(),
        "non_diabetic": my_predictions.filter(result_rf=0).count(),
        "avg_age": my_predictions.aggregate(Avg("age"))["age__avg"] or 0,
        "results": my_predictions.select_related("patient")[:5],
        "patients": my_patients[:5],
    }
    return render(request, "predictor/dashboard.html", context)


@login_required
def patient_list(request):
    patients = Patient.objects.filter(doctor=request.user)
    return render(request, "predictor/patient_list.html", {"patients": patients})


@login_required
def add_patient(request):
    if request.method == "POST":
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.save()
            return redirect("patient_detail", patient_id=patient.id)
    else:
        form = PatientForm()

    return render(request, "predictor/patient_form.html", {"form": form})


@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    predictions = patient.predictions.all()
    results = []

    if request.method == "POST":
        form = PredictionInputForm(request.POST)

        if form.is_valid():
            cleaned = form.cleaned_data
            features = build_features(cleaned)

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
                    "is_diabetic": pred == 1,
                    "probability": prob,
                })
                db_results[name] = pred

            Prediction.objects.create(
                patient=patient,
                pregnancies=cleaned["pregnancies"],
                glucose=cleaned["glucose"],
                blood_pressure=cleaned["blood_pressure"],
                skin_thickness=cleaned["skin_thickness"],
                insulin=cleaned["insulin"],
                bmi=cleaned["bmi"],
                dpf=cleaned["diabetes_pedigree_function"],
                age=cleaned["age"],
                result_logreg=db_results["Logistic Regression"],
                result_rf=db_results["Random Forest"],
                result_mlp=db_results["Neural Network"],
            )

            return redirect("patient_detail", patient_id=patient.id)
    else:
        form = PredictionInputForm(initial={"age": patient.age})

    context = {
        "patient": patient,
        "form": form,
        "predictions": predictions[:10],
        "results": results,
    }
    return render(request, "predictor/patient_detail.html", context)


@login_required
def history(request):
    prediction_list = Prediction.objects.filter(
        patient__doctor=request.user
    ).select_related("patient")

    paginator = Paginator(prediction_list, 10)
    page_number = request.GET.get("page")
    predictions = paginator.get_page(page_number)

    return render(request, "predictor/history.html", {"predictions": predictions})