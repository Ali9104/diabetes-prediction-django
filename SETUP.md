# Guide de démarrage — DiabPredict v2

## 1. Installer les nouvelles dépendances

```bash
venv\Scripts\python.exe -m pip install catboost imbalanced-learn
```

## 2. Appliquer les migrations

```bash
venv\Scripts\python.exe manage.py migrate
```

## 3. Créer le compte médecin (superuser)

```bash
venv\Scripts\python.exe manage.py createsuperuser
```

Puis aller sur http://127.0.0.1:8000/admin/ et créer un **UserProfile** pour ce superuser avec le rôle **doctor**.

**OU** utiliser le script de création rapide :
```bash
venv\Scripts\python.exe manage.py shell
```
```python
from django.contrib.auth.models import User
from predictor.models import UserProfile
u = User.objects.get(username='ton_username_admin')
UserProfile.objects.create(user=u, role='doctor')
```

## 4. Entraîner le modèle CatBoost (nécessite le dataset Kaggle)

Télécharger le dataset CDC depuis Kaggle :
https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset

Fichier à utiliser : `diabetes_binary_health_indicators_BRFSS2015.csv`

```bash
venv\Scripts\python.exe predictor/ml_model/train_catboost.py --data chemin/vers/diabetes_binary_health_indicators_BRFSS2015.csv
```

Le modèle `catboost_cdc.joblib` sera créé dans `predictor/ml_model/`.
⚠️ **Sans ce fichier, l'app fonctionne quand même** (fallback à 35% par défaut).

## 5. Lancer le serveur

```bash
venv\Scripts\python.exe manage.py runserver
```

## Flux complet

1. Médecin se connecte → dashboard → crée un patient → note l'identifiant/mot de passe
2. Patient se connecte avec son identifiant → fait le questionnaire → voit son résultat
3. Médecin retourne dans le dossier patient → voit le résultat → rédige un traitement
4. Patient actualise sa page → voit les recommandations du médecin
