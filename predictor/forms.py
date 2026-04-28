from django import forms
from django.contrib.auth.models import User
from .models import Patient, Treatment

class PatientForm(forms.ModelForm):
    # Also create a Django User account for the patient
    username = forms.CharField(max_length=150, label="Nom d'utilisateur du patient")
    password = forms.CharField(widget=forms.PasswordInput, label="Mot de passe")
    email = forms.EmailField(required=False, label="Email (optionnel)")

    class Meta:
        model = Patient
        fields = ["first_name", "last_name", "age", "gender"]
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Nom"}),
            "age": forms.NumberInput(attrs={"placeholder": "Âge"}),
            "gender": forms.Select(choices=[
                ("", "Sélectionner le genre"),
                ("Femme", "Femme"),
                ("Homme", "Homme"),
            ]),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username


class CDCQuestionnaireForm(forms.Form):
    high_bp = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous de l'hypertension artérielle (tension élevée) ?",
        widget=forms.RadioSelect
    )
    high_chol = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous un taux de cholestérol élevé ?",
        widget=forms.RadioSelect
    )
    chol_check = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous fait une vérification du cholestérol dans les 5 dernières années ?",
        widget=forms.RadioSelect
    )
    bmi = forms.FloatField(
        label="Quel est votre IMC (Indice de Masse Corporelle) ?",
        min_value=10, max_value=100,
        widget=forms.NumberInput(attrs={"placeholder": "Ex: 25.4", "step": "0.1"})
    )
    smoker = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous fumé au moins 100 cigarettes dans votre vie ?",
        widget=forms.RadioSelect
    )
    stroke = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous déjà eu un AVC (accident vasculaire cérébral) ?",
        widget=forms.RadioSelect
    )
    heart_disease = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous une maladie coronarienne ou avez-vous eu une crise cardiaque ?",
        widget=forms.RadioSelect
    )
    phys_activity = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Pratiquez-vous une activité physique (hors travail) au cours des 30 derniers jours ?",
        widget=forms.RadioSelect
    )
    fruits = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Mangez-vous des fruits au moins une fois par jour ?",
        widget=forms.RadioSelect
    )
    veggies = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Mangez-vous des légumes au moins une fois par jour ?",
        widget=forms.RadioSelect
    )
    heavy_alcohol = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Consommez-vous beaucoup d'alcool ? (>14 verres/semaine pour hommes, >7 pour femmes)",
        widget=forms.RadioSelect
    )
    any_healthcare = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous une couverture médicale (assurance, mutuelle) ?",
        widget=forms.RadioSelect
    )
    no_doc_cost = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Y a-t-il eu un moment où vous n'avez pas pu voir un médecin par manque d'argent ?",
        widget=forms.RadioSelect
    )
    gen_hlth = forms.ChoiceField(
        choices=[
            ('1', '1 - Excellente'),
            ('2', '2 - Très bonne'),
            ('3', '3 - Bonne'),
            ('4', '4 - Passable'),
            ('5', '5 - Mauvaise'),
        ],
        label="Comment évaluez-vous votre santé générale ?",
        widget=forms.RadioSelect
    )
    ment_hlth = forms.IntegerField(
        label="Combien de jours dans les 30 derniers votre santé mentale n'était pas bonne ?",
        min_value=0, max_value=30,
        widget=forms.NumberInput(attrs={"placeholder": "0-30"})
    )
    phys_hlth = forms.IntegerField(
        label="Combien de jours dans les 30 derniers votre santé physique n'était pas bonne ?",
        min_value=0, max_value=30,
        widget=forms.NumberInput(attrs={"placeholder": "0-30"})
    )
    diff_walk = forms.ChoiceField(
        choices=[('1', 'Oui'), ('0', 'Non')],
        label="Avez-vous des difficultés à marcher ou monter des escaliers ?",
        widget=forms.RadioSelect
    )
    sex = forms.ChoiceField(
        choices=[('0', 'Femme'), ('1', 'Homme')],
        label="Genre",
        widget=forms.RadioSelect
    )
    age_category = forms.ChoiceField(
        choices=[
            ('1', '18-24 ans'), ('2', '25-29 ans'), ('3', '30-34 ans'),
            ('4', '35-39 ans'), ('5', '40-44 ans'), ('6', '45-49 ans'),
            ('7', '50-54 ans'), ('8', '55-59 ans'), ('9', '60-64 ans'),
            ('10', '65-69 ans'), ('11', '70-74 ans'), ('12', '75-79 ans'),
            ('13', '80 ans et plus'),
        ],
        label="Tranche d'âge"
    )
    education = forms.ChoiceField(
        choices=[
            ('1', 'Jamais scolarisé / École primaire'),
            ('2', 'Primaire'),
            ('3', 'Collège'),
            ('4', 'Lycée (sans baccalauréat)'),
            ('5', 'Baccalauréat'),
            ('6', 'Études supérieures'),
        ],
        label="Niveau d'éducation"
    )
    income = forms.ChoiceField(
        choices=[
            ('1', 'Moins de 10 000 €/an'),
            ('2', '10 000 - 15 000 €/an'),
            ('3', '15 000 - 20 000 €/an'),
            ('4', '20 000 - 25 000 €/an'),
            ('5', '25 000 - 35 000 €/an'),
            ('6', '35 000 - 50 000 €/an'),
            ('7', '50 000 - 75 000 €/an'),
            ('8', 'Plus de 75 000 €/an'),
        ],
        label="Niveau de revenus annuels"
    )


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['notes', 'medications', 'followup_date']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Recommandations médicales, conseils de mode de vie...'}),
            'medications': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Médicaments prescrits, dosages...'}),
            'followup_date': forms.DateInput(attrs={'type': 'date'}),
        }
        labels = {
            'notes': 'Recommandations',
            'medications': 'Médicaments (optionnel)',
            'followup_date': 'Date de suivi (optionnel)',
        }

class OsteoporosisPredictionForm(forms.Form):
    Age = forms.IntegerField(
        min_value=1,
        max_value=120,
        label="Age",
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Ex: 65"})
    )

    Gender = forms.ChoiceField(
        choices=[("Male", "Male"), ("Female", "Female")],
        label="Gender",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Hormonal_Changes = forms.ChoiceField(
        choices=[("Normal", "Normal"), ("Postmenopausal", "Postmenopausal")],
        label="Hormonal Changes",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Family_History = forms.ChoiceField(
        choices=[("Yes", "Yes"), ("No", "No")],
        label="Family History",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Race_Ethnicity = forms.ChoiceField(
        choices=[
            ("Asian", "Asian"),
            ("Caucasian", "Caucasian"),
            ("African American", "African American"),
        ],
        label="Race/Ethnicity",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Body_Weight = forms.ChoiceField(
        choices=[("Normal", "Normal"), ("Underweight", "Underweight")],
        label="Body Weight",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Calcium_Intake = forms.ChoiceField(
        choices=[("Low", "Low"), ("Adequate", "Adequate")],
        label="Calcium Intake",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Vitamin_D_Intake = forms.ChoiceField(
        choices=[("Sufficient", "Sufficient"), ("Insufficient", "Insufficient")],
        label="Vitamin D Intake",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Physical_Activity = forms.ChoiceField(
        choices=[("Active", "Active"), ("Sedentary", "Sedentary")],
        label="Physical Activity",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Smoking = forms.ChoiceField(
        choices=[("Yes", "Yes"), ("No", "No")],
        label="Smoking",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Alcohol_Consumption = forms.ChoiceField(
        choices=[("None", "None"), ("Moderate", "Moderate")],
        label="Alcohol Consumption",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Medical_Conditions = forms.ChoiceField(
        choices=[
            ("None", "None"),
            ("Rheumatoid Arthritis", "Rheumatoid Arthritis"),
            ("Hyperthyroidism", "Hyperthyroidism"),
        ],
        label="Medical Conditions",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Medications = forms.ChoiceField(
        choices=[
            ("None", "None"),
            ("Corticosteroids", "Corticosteroids"),
        ],
        label="Medications",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Prior_Fractures = forms.ChoiceField(
        choices=[("Yes", "Yes"), ("No", "No")],
        label="Prior Fractures",
        widget=forms.Select(attrs={"class": "form-control"})
    )

    Model = forms.ChoiceField(
        choices=[
            ("cat", "CatBoost"),
            ("xgb", "XGBoost"),
            ("rf", "Random Forest"),
            ("lr", "Logistic Regression"),
        ],
        label="Model",
        initial="cat",
        widget=forms.Select(attrs={"class": "form-control"})
    )
