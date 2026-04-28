from django.contrib import admin
from .models import UserProfile, Patient, Treatment,OsteoporosisPrediction

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'age', 'doctor', 'user']

@admin.register(OsteoporosisPrediction)
class OsteoporosisPredictionAdmin(admin.ModelAdmin):
    list_display = ['patient', 'probability', 'result', 'created_at']
    list_filter = ['result', 'model_used']

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['prediction', 'doctor', 'created_at']
