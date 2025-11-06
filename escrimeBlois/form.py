from wtforms import StringField, HiddenField, RadioField, DateField, FileField
from wtforms import PasswordField
from .models import Demande_inscription
from hashlib import sha256
from email_validator import validate_email, EmailNotValidError, ValidatedEmail
from .app import app, db
from sqlalchemy import func


class FormInscription():
    nom = StringField('Nom')
    prenom = StringField('Prenom')
    mot_de_passe = PasswordField('Mot de passe')
    conf_mot_de_passe = PasswordField('Confirmer mot de passe')
    sexe = RadioField('Sexe')
    date_naissance = DateField('Date de naissance')
    num_tel = StringField('Numéro de téléphone')
    adresse_mail = StringField("Adresse mail")
    adresse_postale = StringField('Adresse postale')
    eleve = RadioField('Adresse postale')
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
        id = self.max_id()
        self.bon_mdp()
        mail = self.format_mail()
        m = sha256()
        m.update(self.mot_de_passe.data.encode('utf-8'))
        est_scolarisee = True if self.eleve.data == 'Oui' else False
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
                                justificatif=self.justificatif.data))
        db.session.commit()
