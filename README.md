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

### 3. Configuration des emails (optionnel)

Pour activer l'envoi d'emails (récupération de mot de passe, notifications, etc.), copier le fichier `.env.example` et le renommer en `.env` :

**Windows :**
```powershell
Copy-Item escrimeBlois\.env.example escrimeBlois\.env
```

**Linux :**
```bash
cp escrimeBlois/.env.example escrimeBlois/.env
```

Ensuite, éditer le fichier `escrimeBlois/.env` et configurer les paramètres SMTP :
- **SendGrid** (recommandé, gratuit jusqu'à 100 emails/jour) : créer un compte sur [sendgrid.com](https://sendgrid.com) et générer une API Key
- Ou utiliser un autre service SMTP en modifiant les paramètres dans le fichier `.env`

### 4. Initialiser la base de données

```bash
flask syncdb
flask loaddb ./escrimeBlois/data/data.yml
```

### 5. Lancer le serveur

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