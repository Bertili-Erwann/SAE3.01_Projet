# SAE3.01_Projet

## Groupe 7 Sujet n°2 :
- BERTILI Erwann (chef de groupe)
- ARSAMERZOEV Magomed
- DRAME Zakharia
- DANZIN Titouan

[Lien google docs](https://docs.google.com/document/d/1KPeOIm2hwzRj-kSABxSznwqE1FfCwznEYwg0lbTOmic/edit?usp=sharing)

---

## Installation et lancement du site web

### Prérequis
- Python 3.11+
- pip

### 1. Créer l'environnement virtuel

**Windows :**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Linux :**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Installer les dépendances

```bash
pip install -r requirements.txt
```

### 3. Initialiser la base de données

```bash
flask syncdb
flask loaddb ./escrimeBlois/data/data.yml
```

### 4. Lancer le serveur

```bash
flask run
```

Le site sera accessible sur : [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## Tests

**ATTENTION !!:** les tests suppriment les informations dans la base de données escrimeBlois.db, il faudra donc refaire `syncdb` et `loaddb` pour pouvoir redémarrer le site web

### Lancer tous les tests

**Windows :**
```powershell
.venv\Scripts\python.exe -m pytest
```

**Linux :**
```bash
python -m pytest
```

### Lancer les tests avec rapport de couverture

**Windows :**
```powershell
.venv\Scripts\python.exe -m pytest --cov=escrimeBlois --cov-report=html
```

**Linux :**
```bash
python -m pytest --cov=escrimeBlois --cov-report=html
```

Le rapport de couverture sera généré dans le dossier `htmlcov/`. Ouvrir `htmlcov/index.html` dans un navigateur pour voir les résultats.