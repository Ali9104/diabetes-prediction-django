from django.db import models
from django.contrib.auth.models import User


class Patient(models.Model):
    doctor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="patients"
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Prediction(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="predictions",
        null=True,
        blank=True
    )

    pregnancies = models.FloatField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    dpf = models.FloatField()
    age = models.FloatField()

    result_logreg = models.IntegerField()
    result_rf = models.IntegerField()
    result_mlp = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        patient_name = self.patient if self.patient else "No patient"
        return f"{patient_name} - {self.created_at.date()}"