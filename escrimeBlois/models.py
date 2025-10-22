from .app import db
from flask_login import UserMixin
from .app import login_manager
from sqlalchemy.orm import validates


@login_manager.user_loader
def load_user(id):
    return Personne.query.get(id)


class Personne(UserMixin, db.Model):
    id_personne = db.Column(db.Integer, primary_key=True)
    mdp = db.Column(db.String(64))
    nom_personne = db.Column(db.String(64))
    prenom_personne = db.Column(db.String(64))
    email_personne = db.Column(db.String(64))
    sexe = db.Column(db.String(1))
    adresse = db.Column(db.String(64))
    date_naissance = db.Column(db.Date)
    etudiant = db.Column(db.Boolean)
    arme_principale = db.Column(db.String(30))
    niveau = db.Column(db.String(20))
    role = db.Column(db.String(10))

    @validates('role')
    def validate_role(self, key, value):
        match value:
            case "membre" | "responsable":
                if self.etudiant is None or self.arme_principale is None or self.niveau is None:
                    raise ValueError(
                        f"Le  '{value}' n'a pas rempli un des champs requis")
            case "personne" | "admin":
                if self.etudiant is not None or self.arme_principale is not None or self.niveau is not None:
                    raise ValueError(f"'{value}' a des informations en trop")
        return value 

class Evenement(db.Model):
    id_evenement = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    heure = db.Column(db.Integer)
    categorie = db.Column(db.String(30))
    lieu = db.Column(db.String(64))
    description = db.Column(db.String(255))

    niveau = db.Column(db.String(10))
    discipline = db.Column(db.String(60))
    cooperative = db.Column(db.String(60))

    type_evenement = db.Column(db.String(64))

    @validates('type_evenement')
    def validate_attributs_evenement(self, key, value):
        match value:
            case "competition":
                if self.niveau is None or self.discipline is None or self.cooperative is None:
                    raise ValueError(
                        f"'{value}' n'a pas rempli un des champs requis")
            case _:
                if self.niveau is not None or self.discipline is not None or self.cooperative is not None:
                    raise ValueError(f"'{value}' a des informations en trop")
        return value
    def __repr__(self):
        return f"<Evenement id={self.id_evenement!r} type={self.type_evenement!r} date={self.date!r} heure={self.heure!r} lieu={self.lieu!r}>"

    def __str__(self):
        return f"{self.type_evenement}"


class Inscription(db.Model):
    id_inscription = db.Column(db.Integer, primary_key=True)
    id_evenement = db.Column(db.Integer,
                             db.ForeignKey("evenement.id_evenement"))


class Classer(db.Model):
    id_competition = db.Column(db.Integer,
                               db.ForeignKey("inscription.id_inscription"),
                               primary_key=True)
    id_inscription = db.Column(db.Integer,
                               db.ForeignKey("evenement.id_evenement"),
                               primary_key=True)
    point = db.Column(db.Integer)

    @validates('id_competition')
    def validate_evenement_type(self, key, value):
        ev = Evenement.query.get(value)
        if ev is None:
            raise ValueError(f"Événement {value} introuvable")
        if ev.type_evenement != 'competition':
            raise ValueError(
                f"L'événement {value} doit être de type competition ")
        return value


class Formulaire(db.Model):
    id_formulaire = db.Column(db.Integer, primary_key=True)
    nom_auteur = db.Column(db.String(64))
    prenom_auteur = db.Column(db.String(64))
    email_auteur = db.Column(db.String(64))
    objet = db.Column(db.String(100))
    message = db.Column(db.String(500))


class Repondre(db.Model):
    id_responsable = db.Column(db.Integer,
                               db.ForeignKey("personne.id_personne"),
                               primary_key=True)
    id_formulaire = db.Column(db.Integer,
                              db.ForeignKey("formulaire.id_formulaire"),
                              primary_key=True)

    @validates('id_responsable')
    def validate_responsable_type(self, key, value):
        pers = Personne.query.get(value)
        if pers is None:
            raise ValueError(f"La personne {value} est introuvable")
        if pers.role != 'responsable':
            raise ValueError(
                f"La personne {value} doit être de type 'responsable' vous avez le type {pers.role}"
            )
        return value


class Article(db.Model):
    id_article = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(64))
    date_publication = db.Column(db.Date)
    description = db.Column(db.String(1000))
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
