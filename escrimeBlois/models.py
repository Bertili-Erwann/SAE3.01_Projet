from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import validates


@login_manager.user_loader
def load_user(id):
    return Personne.query.get(id)


class Personne(UserMixin, db.Model):
    id_personne = db.Column(db.Intger, primary_key=True)
    mdp = db.Column(db.String(64))
    role = db.Column(db.String(6))
    nom_personne = db.Column(db.String(64))
    prenom_personne = db.Column(db.String(64))
    email_personne = db.Column(db.String(64), primary_key=True)


class Evenement(db.Model):
    id_evenement = db.Column(db.Intger, primary_key=True)
    date = db.Column(db.Date)
    heure = db.Column(db.Integer)
    type_evenement = db.Column(db.String(64))
    lieu = db.Column(db.String(64))
    description = db.Column(db.String(255))

    def __repr__(self):
        return "<Evenement (%d) %s>" % (self.id_evenement, self.type_evenement)


class Classer(db.Model):
    id_competition = db.Column(db.Intger,
                               db.ForeignKey("evenement.id_evenement"))
    id_inscription = db.Column(db.Intger,
                               db.ForeignKey("evenement.id_evenement"))

    @validates('id_competition', 'id_inscription')
    def validate_evenement_type(self, key, value):
        ev = Evenement.query.get(value)
        if ev is None:
            raise ValueError(f"Événement {value} introuvable")
        val_attendu = 'competition' if key == 'id_competition' else 'inscription'
        if ev.type_evenement != val_attendu:
            raise ValueError(
                f"L'événement {value} doit être de type '{val_attendu}'")
        return value


class Formulaire(db.Model):
    id_formulaire = db.Column(db.Intger, primary_key=True)
    nom_auteur = db.Column(db.String(64))
    prenom_auteur = db.Column(db.String(64))
    email_auteur = db.Column(db.String(64))
    objet = db.Column(db.String(100))
    message = db.Column(db.String(500))


class Repondre(db.Model):
    id_responsable = db.ForeignKey("personne.id_personne")
    id_formulaire = db.ForeignKey("formulaire.id_formulaire")

    @validates('id_responsable')
    def validate_responsable_type(self, key, value):
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        role_attendu = "resp"
        if pers.role != role_attendu:
            raise ValueError(
                f"La personne {value} doit être de type '{role_attendu}' vous avez le type {pers.role}"
            )
        return value


class Article(db.Model):
    id_article = db.Column(db.Intger, primary_key=True)
    titre = db.Column(db.String(64))
    date_publication = db.Column(db.Date)
    contenu = db.Column(db.String(1000))
    categorie = db.Column(db.String(20))
    commentable = db.Column(db.Boolean)
    responsable_id = db.ForeignKey("personne.id_personne")
    responsable = None 
    @validates('id_responsable')
    def validate_responsable_type(self, key, value):
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        role_attendu = "resp"
        if pers.role != role_attendu:
            raise ValueError(
                f"La personne {value} doit être de type '{role_attendu}' vous avez le type {pers.role}"
            )
        self.responsable = db.relationship("Personne",
                                      backref=db.backref("articles",
                                                         lazy="dynamic"))
        return value
