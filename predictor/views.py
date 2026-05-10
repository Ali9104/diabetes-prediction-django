import os
import joblib
import pandas as pd
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Patient, OsteoporosisPrediction, Treatment, UserProfile
from .forms import PatientForm, TreatmentForm, OsteoporosisPredictionForm

MODEL_DIR = os.path.join(settings.BASE_DIR, "predictor", "ml_model")

MODEL_FILES = {
    "cat": "CatBoost_osteoporosis.pkl",
    "xgb": "XGBoost_osteoporosis.pkl",
    "rf":  "RandomForest_osteoporosis.pkl",
    "lr":  "LogisticRegression_osteoporosis.pkl",
}

def load_model(model_key):
    filename = MODEL_FILES.get(model_key)
    path = os.path.join(MODEL_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f"Fichier modèle introuvable : {path}")
    return joblib.load(path)

def build_input_dataframe(data):
    df = pd.DataFrame([{
        "Age": int(data["Age"]),
        "Gender": data["Gender"],
        "Hormonal Changes": data["Hormonal_Changes"],
        "Family History": data["Family_History"],
        "Race/Ethnicity": data["Race_Ethnicity"],
        "Body Weight": data["Body_Weight"],
        "Calcium Intake": data["Calcium_Intake"],
        "Vitamin D Intake": data["Vitamin_D_Intake"],
        "Physical Activity": data["Physical_Activity"],
        "Smoking": data["Smoking"],
        "Alcohol Consumption": data["Alcohol_Consumption"],
        "Medical Conditions": data["Medical_Conditions"],
        "Medications": data["Medications"],
        "Prior Fractures": data["Prior_Fractures"],
    }])

    df["Risk_Age"] = (df["Age"] > 60).astype(int)
    df["Lifestyle_Risk"] = (
        (df["Smoking"] == "Yes").astype(int) +
        (df["Alcohol Consumption"] == "High").astype(int) -
        (df["Physical Activity"] == "Active").astype(int)
    )
    df["Nutrition_Risk"] = (
        (df["Calcium Intake"] == "Low").astype(int) +
        (df["Vitamin D Intake"] == "Insufficient").astype(int)
    )
    df["Medical_Risk"] = (
        (df["Medical Conditions"] != "Unknown").astype(int) +
        (df["Medications"] != "Unknown").astype(int)
    )
    return df

def get_user_role(user):
    try:
        return user.profile.role
    except UserProfile.DoesNotExist:
        return None

def require_role(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if get_user_role(request.user) != role:
                return redirect('home')
            return view_func(request, *args, **kwargs)
        wrapper.__name__ = view_func.__name__
        return wrapper
    return decorator

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    role = get_user_role(request.user)
    if role == 'doctor':
        return redirect('doctor_dashboard')
    return redirect('patient_dashboard')

@require_role('doctor')
@login_required
def doctor_dashboard(request):
    patients = Patient.objects.filter(doctor=request.user)
    recent_predictions = OsteoporosisPrediction.objects.filter(patient__doctor=request.user).order_by('-created_at')[:5]
    context = {
        'total_patients': patients.count(),
        'recent_predictions': recent_predictions,
        'patients': patients[:6],
    }
    return render(request, 'predictor/doctor_dashboard.html', context)

@require_role('doctor')
@login_required
def patient_list(request):
    patients = Patient.objects.filter(doctor=request.user)
    return render(request, 'predictor/patient_list.html', {'patients': patients})

@require_role('doctor')
@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id, doctor=request.user)
    predictions = patient.osteo_predictions.all().order_by('-created_at')
    return render(request, 'predictor/patient_detail.html', {'patient': patient, 'predictions': predictions})

@require_role('doctor')
@login_required
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserProfile.objects.create(user=user, role='patient')
            patient = form.save(commit=False)
            patient.doctor = request.user
            patient.user = user
            patient.save()
            return redirect('patient_list')
    else:
        form = PatientForm()
    return render(request, 'predictor/patient_form.html', {'form': form})

@require_role('patient')
@login_required
def patient_dashboard(request):
    patient = get_object_or_404(Patient, user=request.user)
    
    all_predictions = patient.osteo_predictions.all().order_by('-created_at')
    latest_prediction = all_predictions.first()
    treatment = None
    if latest_prediction and hasattr(latest_prediction, 'treatment'):
        treatment = latest_prediction.treatment

    return render(request, 'predictor/patient_dashboard.html', {
        'patient': patient,
        'predictions': all_predictions, 
        'prediction': latest_prediction, 
        'treatment': treatment,
        'latest': latest_prediction     
            
    })

@require_role('patient')
@login_required
def take_test(request):
    patient = get_object_or_404(Patient, user=request.user)
    if request.method == 'POST':
        form = OsteoporosisPredictionForm(request.POST)
        if form.is_valid():
            model_key = form.cleaned_data.get("Model", "cat")
            model_pipeline = load_model(model_key)
            
            X = build_input_dataframe(form.cleaned_data)
            
            proba = model_pipeline.predict_proba(X)[0][1]
            result = 1 if proba >= 0.40 else 0
            
            prediction = OsteoporosisPrediction.objects.create(
                patient=patient,
                age=int(form.cleaned_data['Age']),
                gender=form.cleaned_data['Gender'],
                hormonal_changes=form.cleaned_data['Hormonal_Changes'],
                family_history=form.cleaned_data['Family_History'],
                race_ethnicity=form.cleaned_data['Race_Ethnicity'],
                body_weight=form.cleaned_data['Body_Weight'],
                calcium_intake=form.cleaned_data['Calcium_Intake'],
                vitamin_d_intake=form.cleaned_data['Vitamin_D_Intake'],
                physical_activity=form.cleaned_data['Physical_Activity'],
                smoking=form.cleaned_data['Smoking'],
                alcohol_consumption=form.cleaned_data['Alcohol_Consumption'],
                medical_conditions=form.cleaned_data['Medical_Conditions'],
                medications=form.cleaned_data['Medications'],
                prior_fractures=form.cleaned_data['Prior_Fractures'],
                probability=round(float(proba) * 100, 2),
                result=result,
                model_used=model_key
            )
            return redirect('test_result', prediction_id=prediction.id)
    else:
        form = OsteoporosisPredictionForm(initial={'Age': patient.age, 'Gender': patient.gender})
    return render(request, 'predictor/take_test.html', {'form': form})

@require_role('patient')
@login_required
def test_result(request, prediction_id):
    prediction = get_object_or_404(OsteoporosisPrediction.objects.select_related('treatment'), id=prediction_id)
    return render(request, 'predictor/test_result.html', {'prediction': prediction})
@require_role('doctor')
@login_required
def add_treatment(request, prediction_id):
    prediction = get_object_or_404(OsteoporosisPrediction, id=prediction_id)
    patient = prediction.patient 

    if request.method == 'POST':
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save(commit=False)
            
            treatment.prediction = prediction
            treatment.patient = patient
            treatment.doctor = request.user 
            
            treatment.save()
            messages.success(request, "Le traitement a été ajouté avec succès.")
            return redirect('patient_detail', patient_id=patient.id)
    else:
        form = TreatmentForm()
    
    return render(request, 'predictor/treatment_form.html', {
        'form': form, 
        'prediction': prediction,
        'patient': patient
    })

