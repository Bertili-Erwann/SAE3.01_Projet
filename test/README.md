# Tests Unitaires - Escrime Blois

## Structure des tests

- `conftest.py` : Fixtures communes pour tous les tests
- `test_models.py` : Tests des modèles de base de données
- `test_forms.py` : Tests des formulaires WTForms
- `test_views.py` : Tests des routes et vues Flask
- `test_config.py` : Tests de la configuration
- `test_app.py` : Tests des fonctions de l'application

## Lancer les tests

```bash
pytest test/
```

Pour un rapport détaillé :
```bash
pytest test/ -v
```

Pour voir la couverture :
```bash
pytest test/ --cov=escrimeBlois
```
