from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('doctor', 'Médecin'),
        ('patient', 'Patient'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='patient')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_doctor(self):
        return self.role == 'doctor'

    @property
    def is_patient(self):
        return self.role == 'patient'


class Patient(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patients")
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="patient_profile")
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class OsteoporosisPrediction(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='osteo_predictions')
    
    # Données du dataset osteoporosis.csv
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    hormonal_changes = models.CharField(max_length=50)
    family_history = models.CharField(max_length=10)
    race_ethnicity = models.CharField(max_length=50)
    body_weight = models.CharField(max_length=20)
    calcium_intake = models.CharField(max_length=20)
    vitamin_d_intake = models.CharField(max_length=20)
    physical_activity = models.CharField(max_length=20)
    smoking = models.CharField(max_length=10)
    alcohol_consumption = models.CharField(max_length=20)
    medical_conditions = models.CharField(max_length=100)
    medications = models.CharField(max_length=100)
    prior_fractures = models.CharField(max_length=10)

    # Résultats de l'IA
    probability = models.FloatField()
    result = models.IntegerField() # 0 ou 1
    model_used = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.patient} - {self.created_at.date()} - {self.probability:.1f}%"

    @property
    def risk_level(self):
        if self.probability >= 60:
            return 'critical'
        elif self.probability >= 35:
            return 'high'
        elif self.probability >= 15:
            return 'medium'
        return 'low'

    @property
    def risk_label(self):
        levels = {
            'critical': 'DANGER CRITIQUE',
            'high': 'Risque élevé', 
            'medium': 'Risque modéré', 
            'low': 'Risque faible'
        }
        return levels.get(self.risk_level, 'Inconnu')


class Treatment(models.Model):
    # Changement ici : lié à OsteoporosisPrediction au lieu de CDCPrediction
    prediction = models.OneToOneField(OsteoporosisPrediction, on_delete=models.CASCADE, related_name="treatment")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="treatments")
    notes = models.TextField()
    medications = models.TextField(blank=True, null=True)
    followup_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Traitement - {self.prediction.patient} - {self.created_at.date()}"