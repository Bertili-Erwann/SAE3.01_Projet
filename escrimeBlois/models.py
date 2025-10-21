from .app import db
from flask_login import UserMixin
from .app import login_manager
    
@login_manager.user_loader
def load_user(id):
    return Personne.query.get(id)

class Personne(UserMixin, db.Model):
    id_personne = db.Column(db.String(64), primary_key=True)
    mdp = db.Column(db.String(64))
    role = db.Column(db.String(6))
    nom_personne = db.Column(db.String(64))
    prenom_personne = db.Column(db.String(64))
    email_personne = db.Column(db.String(64))

