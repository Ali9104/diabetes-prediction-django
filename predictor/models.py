from django.db import models

class Prediction(models.Model):
    pregnancies = models.FloatField()
    glucose = models.FloatField()
    blood_pressure = models.FloatField()
    skin_thickness = models.FloatField()
    insulin = models.FloatField()
    bmi = models.FloatField()
    dpf = models.FloatField()
    age = models.FloatField()

    # Changed to IntegerField for better logic handling (0=Healthy, 1=Diabetic)
    result_logreg = models.IntegerField()
    result_rf = models.IntegerField()
    result_mlp = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction {self.id} - {self.created_at.date()}"