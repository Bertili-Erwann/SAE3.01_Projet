from wtforms import StringField, PasswordField, RadioField, DateField, FileField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, Length, Optional
from flask_wtf import FlaskForm
from hashlib import sha256
from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from werkzeug.utils import secure_filename
from .app import app, db
from .models import Demande_inscription, Formulaire, Commentaire, Information
from sqlalchemy import func
import os


class FormInformation(FlaskForm):
    titre = StringField('Titre', validators=[DataRequired()])
    contenu = TextAreaField('Contenu', validators=[DataRequired()])
    ordre = IntegerField('Ordre', validators=[DataRequired()])


class FormInscription(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
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
    eleve = RadioField('Élève / Scolarisé',
                       choices=[('Oui', 'Oui'), ('Non', 'Non')],
                       validators=[DataRequired()])
    justificatif = FileField('Justificatif (si élève)')

    @staticmethod
    def max_id() -> int:
        max_id = db.session.query(func.max(
            Demande_inscription.id_inscription)).scalar()
        return (int(max_id) + 1) if max_id is not None else 1

    def bon_mdp(self) -> bool:
        return self.mot_de_passe.data == self.conf_mot_de_passe.data

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.adresse_mail.data,
                                  check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))
            raise

    def commit_inscription(self):
        if not self.bon_mdp():
            raise ValueError("Les mots de passe ne correspondent pas")

        id_inscription = self.max_id()
        mail = self.format_mail()
        m = sha256()
        m.update(self.mot_de_passe.data.encode('utf-8'))
        est_scolarise = self.eleve.data == 'Oui'

        # Gestion du justificatif
        justificatif_data = None
        file_data = self.justificatif.data
        
        if file_data and getattr(file_data, "filename", ""):
            # Sécuriser le nom du fichier
            filename = secure_filename(file_data.filename)
            # Définir le chemin d'upload relatif
            upload_folder = os.path.join(os.path.dirname(__file__), 'uploads', 'files')
            os.makedirs(upload_folder, exist_ok=True)
            # Sauvegarder le fichier
            file_path = os.path.join(upload_folder, filename)
            file_data.save(file_path)
            
            # Stocker les métadonnées en JSON (nom et chemin relatif)
            justificatif_data = {
                'filename': filename,
                'path': f'uploads/files/{filename}',
                'original_filename': file_data.filename
            }

        db.session.add(
            Demande_inscription(
                id_inscription=id_inscription,
                nom=self.nom.data,
                prenom=self.prenom.data,
                mot_de_passe=m.hexdigest(),
                sexe=self.sexe.data,
                date_naissance=self.date_naissance.data,
                num_tel=self.num_tel.data,
                adresse_mail=mail.normalized,
                adresse_postale=self.adresse_postale.data,
                eleve=est_scolarise,
                justificatif=justificatif_data
            )
        )
        db.session.commit()


class FormInscriptionEvent(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    date_naissance = DateField('Date de naissance', validators=[DataRequired()])
    sexe = RadioField('Sexe', choices=[('H', 'Homme'), ('F', 'Femme')], validators=[DataRequired()])
    justificatif = FileField('Justificatif de catégorie', validators=[DataRequired()])
   
class FormFormulaire(FlaskForm):
    nom = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    objet = TextAreaField('Objet',
                          validators=[
                              DataRequired(),
                              Length(
                                  min=1,
                                  max=80,
                                  message="Trop long, maximum 80 caractères")
                          ])
    message = TextAreaField(
        'Message',
        validators=[
            DataRequired(),
            Length(min=1,
                   max=1200,
                   message="Trop long, maximum 1200 caractères")
        ])

    @staticmethod
    def max_id() -> int:
        max_id = db.session.query(func.max(Formulaire.id_formulaire)).scalar()
        return (int(max_id) + 1) if max_id is not None else 1

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.email.data, check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))
            raise

    def commit_formulaire(self):
        id_form = self.max_id()
        mail = self.format_mail()
        db.session.add(
            Formulaire(
                id_formulaire=id_form,
                nom_auteur=self.nom.data,
                email_auteur=mail.normalized,
                objet=self.objet.data,
                message=self.message.
                data  # Ajout du message (manquant dans develop original ?)
            ))
        db.session.commit()
        
class FormRechercheArticle(FlaskForm):
    choix_year = SelectField("Sélectionner un mois",
                             choices=[],
                             validators=[DataRequired()])
    recherche = StringField("Rechercher un article", validators=[Optional()])
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Charger les choix dynamiquement
        from .models import Article
        from sqlalchemy import extract
        try:
            lesArticles = db.session.query(
                extract('year', Article.date_publication).label('year'),
                extract('month', Article.date_publication).label('month'),
                func.count().label('count')).group_by(
                    'year', 'month').order_by('year', 'month').all()
            choices = []
            for ar in lesArticles:
                value = f"{ar.month}-{ar.year}"
                label = f"{ar.month}-{ar.year} ({ar.count})"
                choices.append((value, label))
            self.choix_year.choices = choices
        except:
            # Si la table n'existe pas encore (tests), laisser vide
            self.choix_year.choices = []


class FormCommentaire(FlaskForm):
    nom_aut = StringField("Nom", validators=[DataRequired()])
    email_aut = StringField("Email", validators=[DataRequired()])
    message = TextAreaField("Message", validators=[DataRequired()])

    @staticmethod
    def max_id() -> int:
        max_id = db.session.query(func.max(
            Commentaire.id_commentaire)).scalar()
        return (int(max_id) + 1) if max_id is not None else 1

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.email_aut.data,
                                  check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))
            raise

    def envoyer_commentaire(self, id_article: int):
        mail = self.format_mail()
        id_com = self.max_id()

        db.session.add(
            Commentaire(id_commentaire=id_com,
                        nom_aut=self.nom_aut.data,
                        email_aut=mail.normalized,
                        id_article=id_article,
                        message_com=self.message.data))
        db.session.commit()


class FormModifMembre(FlaskForm):
    """Formulaire pour modifier les informations d'un membre par un admin"""
    nom = StringField('Nom', validators=[DataRequired()])
    prenom = StringField('Prénom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Numéro de téléphone', validators=[DataRequired()])
    sexe = RadioField('Sexe',
                      choices=[('H', 'Homme'), ('F', 'Femme')],
                      validators=[DataRequired()])
    date_naissance = DateField('Date de naissance',
                               validators=[DataRequired()])
    adresse = StringField('Adresse postale',
                         validators=[DataRequired()])
    eleve = RadioField('Élève / Scolarisé',
                       choices=[('Oui', 'Oui'), ('Non', 'Non')],
                       validators=[DataRequired()])
    arme_principale = SelectField('Arme principale',
                                  choices=[('épée', 'Épée'),
                                          ('fleuret', 'Fleuret'),
                                          ('sabre', 'Sabre')],
                                  validators=[DataRequired()])
    niveau = SelectField('Niveau',
                        choices=[('débutant', 'Débutant'),
                                ('intermédiaire', 'Intermédiaire'),
                                ('avancé', 'Avancé'),
                                ('expert', 'Expert')],
                        validators=[DataRequired()])
    role = SelectField('Rôle',
                      choices=[('membre', 'Membre'),
                              ('responsable', 'Responsable')],
                      validators=[DataRequired()])

    def format_mail(self) -> ValidatedEmail:
        try:
            return validate_email(self.email.data,
                                  check_deliverability=False)
        except EmailNotValidError as e:
            print(str(e))
            raise

    def update_membre(self, personne):
        """Met à jour les informations d'un membre"""
        from .models import Personne
        
        mail = self.format_mail()
        personne.nom_personne = self.nom.data
        personne.prenom_personne = self.prenom.data
        personne.email_personne = mail.normalized
        personne.telephone = self.telephone.data
        personne.sexe = self.sexe.data
        personne.date_naissance = self.date_naissance.data
        personne.adresse = self.adresse.data
        personne.eleve = (self.eleve.data == 'Oui')
        personne.arme_principale = self.arme_principale.data
        personne.niveau = self.niveau.data
        personne.role = self.role.data
        
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
        from datetime import datetime, timedelta

        user = Personne.query.filter_by(email_personne=self.email.data).first()
        if not user:
            return None, "Email inconnu."
        
        # Générer un code à 4 chiffres
        code_verification = str(random.randint(1000, 9999))
        
        # Définir l'expiration du code (15 minutes)
        code_expiration = datetime.now() + timedelta(minutes=15)
        
        # Sauvegarder le code et son expiration dans la base de données
        user.code_verification_mdp = code_verification
        user.code_verification_expiration = code_expiration
        
        try:
            msg = Message(subject='Code de vérification - Mot de passe oublié',
                          recipients=[self.email.data])
            msg.body = f'Votre code de vérification est : {code_verification}\n\nCe code est valable pendant 15 minutes.'
            mail.send(msg)
            db.session.commit()
            print(f"✉️  Email envoyé avec succès à {self.email.data}")
            return user, None 
        except Exception as e:
            db.session.commit()  # Sauvegarder quand même le code gen généré
            print(f"\n{'='*60}")
            print(f"⚠️  Mode DÉVELOPPEMENT - Email non envoyé")
            print(f"{'='*60}")
            print(f"Email destination : {self.email.data}")
            print(f"Code de vérification : {code_verification}")
            print(f"{'='*60}\n")
            # Retourner l'utilisateur même en cas d'erreur pour permettre le développement
            return user, None
            
