from wtforms import StringField, PasswordField, RadioField, DateField, FileField, TextAreaField
from .models import Demande_inscription, Formulaire
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm
from hashlib import sha256
from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from .app import app, db
from sqlalchemy import func
from sqlalchemy_media import StoreManager, FileSystemStore, File
import functools
import os

# Définir le chemin de stockage local dans le projet
UPLOAD_PATH = os.path.join(os.path.dirname(__file__), 'uploads')

# Créer le dossier s'il n'existe pas
os.makedirs(UPLOAD_PATH, exist_ok=True)

# Configurer le stockage local
StoreManager.register('fs',
                      functools.partial(FileSystemStore, UPLOAD_PATH,
                                        'http://localhost:5000/uploads/'),
                      default=True)


class FormInscription(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    conf_mot_de_passe = PasswordField('Confirmer mot de passe',
                                      validators=[DataRequired()])
    sexe = RadioField('Sexe',
                      choices=[('H', 'Homme'), ('F', 'Femme')],
                      validators=[DataRequired()])
    date_naissance = DateField('Date de naissance',
                               validators=[DataRequired()])
    num_tel = StringField('Numéro de téléphone', validators=[DataRequired()])
    adresse_mail = StringField("Adresse mail", validators=[DataRequired()])
    adresse_postale = StringField('Adresse postale',
                                  validators=[DataRequired()])
    eleve = RadioField('Adresse postale',
                       choices=[('Oui', 'Oui'), ('Non', 'Non')],
                       validators=[DataRequired()])
    justificatif = FileField('justificatif')

    def max_id() -> int:
        max_id = db.session.query(func.max(
            Demande_inscription.id_inscription)).scalar()
        return (int(max_id) + 1) if max_id is not None else 1

    def bon_mdp(self) -> bool:
        return True if self.mot_de_passe.data == self.conf_mot_de_passe.data else False

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.adresse_mail.data,
                                  check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))

    def commit_inscription(self):
        id = FormInscription.max_id()
        self.bon_mdp()
        mail = self.format_mail()
        m = sha256()
        m.update(self.mot_de_passe.data.encode('utf-8'))
        est_scolarisee = True if self.eleve.data == 'Oui' else False

        justificatif_parsed = None
        file_data = self.justificatif.data

        with StoreManager(db.session):
            if file_data and getattr(file_data, "filename", ""):
                justificatif_parsed = File.create_from(file_data)

            db.session.add(
                Demande_inscription(id_inscription=id,
                                    nom=self.nom.data,
                                    prenom=self.prenom.data,
                                    mot_de_passe=m.hexdigest(),
                                    sexe=self.sexe.data,
                                    date_naissance=self.date_naissance.data,
                                    num_tel=self.num_tel.data,
                                    adresse_mail=mail.normalized,
                                    adresse_postale=self.adresse_postale.data,
                                    eleve=est_scolarisee,
                                    justificatif=justificatif_parsed))

            db.session.commit()


class FormInscriptionEvent(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prenom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    date_naissance = DateField('Date de naissance',
                               validators=[DataRequired()])
    sexe = RadioField('Sexe',
                      choices=[('H', 'Homme'), ('F', 'Femme')],
                      validators=[DataRequired()])
    categorie = StringField('Catégorie', validators=[DataRequired()])
    justificatif = FileField('Justificatif de catégorie')


class FormFormulaire(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    objet = TextAreaField('Objet',
                          validators=[
                              DataRequired(),
                              Length(min=1,
                                     max=80,
                                     message="Trop long, maximum 80 caractère")
                          ])
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            Length(min=1,
                   max=1200,
                   message="Trop long, maximum 1200 caractère")
        ])

    def max_id() -> int:
        max_id = db.session.query(func.max(Formulaire.id_formulaire)).scalar()
        return (int(max_id) + 1) if max_id is not None else 1

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.email.data, check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))

    def commit_formulaire(self):
        id = FormFormulaire.max_id()
        mail = self.format_mail()
        db.session.add(
            Formulaire(id_formulaire=id,
                       nom_auteur=self.nom.data,
                       email_auteur=mail.normalized,
                       objet=self.objet.data))
        db.session.commit()
