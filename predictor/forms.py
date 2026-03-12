from django import forms
from .models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "age", "gender"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "age": forms.NumberInput(attrs={"placeholder": "Age"}),
            "gender": forms.Select(
                choices=[
                    ("", "Select gender"),
                    ("Female", "Female"),
                    ("Male", "Male"),
                ]
            ),
        }


class PredictionInputForm(forms.Form):
    pregnancies = forms.FloatField()
    glucose = forms.FloatField()
    blood_pressure = forms.FloatField()
    skin_thickness = forms.FloatField()
    insulin = forms.FloatField()
    bmi = forms.FloatField()
    diabetes_pedigree_function = forms.FloatField()
    age = forms.FloatField()