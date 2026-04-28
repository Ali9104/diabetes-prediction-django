# Patch ostéoporose appliqué

- `mon-espace/test/` utilise maintenant `OsteoporosisPredictionForm`.
- La prédiction charge les modèles dans `predictor/ml_model/`.
- Les résultats restent sauvegardés dans `CDCPrediction` pour garder les dashboards patient/médecin sans migration.
- Les textes principaux des templates ont été adaptés vers ostéoporose/OsteoPredict.

Route à tester : `http://127.0.0.1:8000/mon-espace/test/`

Note : pour une version ultra propre à long terme, crée un modèle `OsteoporosisPrediction`. Ici j’ai volontairement gardé la base existante pour que ça marche vite.
