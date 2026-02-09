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


class FormGestionLogin(FlaskForm):
    email = StringField('email', validators=[DataRequired()])
    mdp = PasswordField('Password', validators=[DataRequired()])

    def authenticate_user(self):
        """
        Authentifie l'utilisateur et retourne un tuple (user, error_message).
        Si l'authentification réussit, retourne (user, None).
        Sinon, retourne (None, error_message).
        """
        from .models import Personne

        user = Personne.query.filter_by(email_personne=self.email.data).first()

        if not user:
            return None, "Email inconnu."

        # Vérifier le mot de passe
        m = sha256()
        m.update(self.mdp.data.encode("utf-8"))
        hashed_password = m.hexdigest()

        if user.mdp == hashed_password or user.mdp == self.mdp.data:
            return user, None
        else:
            return None, "Mot de passe incorrect."


class FormGestionMdpOublier(FlaskForm):
    email = StringField('email', validators=[DataRequired()])

    def etape_1(self):
        from .models import Personne
        from flask_mail import Message
        from .app import mail
        import random

        user = Personne.query.filter_by(email_personne=self.email.data).first()
        if not user:
            return None, "Email inconnu."
        code_verification = str(random.randint(100000, 999999))
        try:
            msg = Message(subject='Code de vérification - Mot de passe oublié',
                          recipients=[self.email.data])
            msg.body = f'Votre code de vérification est : {code_verification}\n\nCe code est valable pendant 15 minutes.'
            mail.send(msg)
            print(f"Email envoyé avec succès à {self.email.data}")
        except Exception as e:
            print(f" > ERREUR d'envoi d'email (mode développement): {str(e)}")
            print(f" > Email simulé envoyé à: {self.email.data}")
            print(f" > Code de vérification: {code_verification}")

        return user, None
