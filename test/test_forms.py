import pytest
from datetime import date
from io import BytesIO
from werkzeug.datastructures import FileStorage
from escrimeBlois.form import *
from escrimeBlois.models import *


def test_form_inscription_bon_mdp(test_app):
    with test_app.app_context():
        form = FormInscription()
        form.mot_de_passe.data = 'test123'
        form.conf_mot_de_passe.data = 'test123'
        assert form.bon_mdp() == True


def test_form_inscription_mauvais_mdp(test_app):
    with test_app.app_context():
        form = FormInscription()
        form.mot_de_passe.data = 'test123'
        form.conf_mot_de_passe.data = 'test456'
        assert form.bon_mdp() == False


def test_form_inscription_format_mail_valide(test_app):
    with test_app.app_context():
        form = FormInscription()
        form.adresse_mail.data = 'test@example.com'
        mail = form.format_mail()
        assert mail.normalized == 'test@example.com'


def test_form_inscription_format_mail_invalide(test_app):
    with test_app.app_context():
        form = FormInscription()
        form.adresse_mail.data = 'invalid-email'
        with pytest.raises(ValueError):
            form.format_mail()


def test_form_inscription_max_id_vide(test_app, session):
    with test_app.app_context():
        assert FormInscription.max_id() == 1


def test_form_inscription_max_id_avec_data(test_app, session):
    with test_app.app_context():
        demande = Demande_inscription(id_inscription=5, nom='Test')
        session.add(demande)
        session.commit()
        assert FormInscription.max_id() == 6


def test_form_inscription_commit_sans_justificatif(test_app, session):
    with test_app.app_context():
        form = FormInscription()
        form.nom.data = 'Dupont'
        form.prenom.data = 'Jean'
        form.mot_de_passe.data = 'pass123'
        form.conf_mot_de_passe.data = 'pass123'
        form.sexe.data = 'H'
        form.date_naissance.data = date(2000, 5, 10)
        form.num_tel.data = '0123456789'
        form.adresse_mail.data = 'jean@test.fr'
        form.adresse_postale.data = '10 rue Test'
        form.eleve.data = 'Non'
        form.justificatif.data = None
        
        form.commit_inscription()
        
        demande = Demande_inscription.query.first()
        assert demande.nom == 'Dupont'
        assert demande.eleve == False


def test_form_inscription_commit_mdp_different(test_app, session):
    with test_app.app_context():
        form = FormInscription()
        form.mot_de_passe.data = 'pass123'
        form.conf_mot_de_passe.data = 'pass456'
        
        with pytest.raises(ValueError):
            form.commit_inscription()


def test_form_formulaire_max_id_vide(test_app, session):
    with test_app.app_context():
        assert FormFormulaire.max_id() == 1


def test_form_formulaire_max_id_avec_data(test_app, session):
    with test_app.app_context():
        form = Formulaire(id_formulaire=3, objet='Test')
        session.add(form)
        session.commit()
        assert FormFormulaire.max_id() == 4


def test_form_formulaire_format_mail_valide(test_app):
    with test_app.app_context():
        form = FormFormulaire()
        form.email.data = 'user@test.com'
        mail = form.format_mail()
        assert mail.normalized == 'user@test.com'


def test_form_formulaire_commit(test_app, session):
    with test_app.app_context():
        form = FormFormulaire()
        form.nom.data = 'Martin'
        form.email.data = 'martin@test.fr'
        form.objet.data = 'Question'
        form.message.data = 'Bonjour, question sur les tarifs'
        
        form.commit_formulaire()
        
        formulaire = Formulaire.query.first()
        assert formulaire.nom_auteur == 'Martin'
        assert formulaire.objet == 'Question'


def test_form_commentaire_max_id_vide(test_app, session):
    with test_app.app_context():
        assert FormCommentaire.max_id() == 1


def test_form_commentaire_max_id_avec_data(test_app, session):
    with test_app.app_context():
        comment = Commentaire(id_commentaire=7, id_article=1, nom_aut='Test')
        session.add(comment)
        session.commit()
        assert FormCommentaire.max_id() == 8


def test_form_commentaire_format_mail_valide(test_app):
    with test_app.app_context():
        form = FormCommentaire()
        form.email_aut.data = 'comment@test.fr'
        mail = form.format_mail()
        assert mail.normalized == 'comment@test.fr'


def test_form_commentaire_envoyer(test_app, session):
    with test_app.app_context():
        article = Article(id_article=1, titre='Test Article', commentable=True)
        session.add(article)
        session.commit()
        
        form = FormCommentaire()
        form.nom_aut.data = 'Dupuis'
        form.email_aut.data = 'dupuis@test.fr'
        form.message.data = 'Super article!'
        
        form.envoyer_commentaire(1)
        
        comment = Commentaire.query.first()
        assert comment.nom_aut == 'Dupuis'
        assert comment.message_com == 'Super article!'


def test_form_modif_membre_format_mail_valide(test_app):
    with test_app.app_context():
        form = FormModifMembre()
        form.email.data = 'membre@test.fr'
        mail = form.format_mail()
        assert mail.normalized == 'membre@test.fr'


def test_form_modif_membre_update(test_app, session):
    with test_app.app_context():
        personne = Personne(
            id_personne=1,
            mdp='test',
            nom_personne='Ancien',
            prenom_personne='Nom',
            email_personne='ancien@test.fr',
            telephone='0111111111',
            sexe='H',
            adresse='Ancienne adresse',
            date_naissance=date(1990, 1, 1),
            eleve=False,
            arme_principale='épée',
            niveau='débutant',
            role='membre'
        )
        session.add(personne)
        session.commit()
        
        form = FormModifMembre()
        form.nom.data = 'Nouveau'
        form.prenom.data = 'Prenom'
        form.email.data = 'nouveau@test.fr'
        form.telephone.data = '0222222222'
        form.sexe.data = 'F'
        form.date_naissance.data = date(1995, 5, 5)
        form.adresse.data = 'Nouvelle adresse'
        form.eleve.data = 'Oui'
        form.arme_principale.data = 'fleuret'
        form.niveau.data = 'avancé'
        form.role.data = 'responsable'
        
        form.update_membre(personne)
        
        assert personne.nom_personne == 'Nouveau'
        assert personne.prenom_personne == 'Prenom'
        assert personne.email_personne == 'nouveau@test.fr'
        assert personne.eleve == True
        assert personne.arme_principale == 'fleuret'
        assert personne.role == 'responsable'


def test_form_gestion_login_authenticate_success(test_app, session):
    with test_app.app_context():
        from hashlib import sha256
        m = sha256()
        m.update('password123'.encode('utf-8'))
        
        personne = Personne(
            id_personne=1,
            mdp=m.hexdigest(),
            nom_personne='Test',
            prenom_personne='User',
            email_personne='user@test.fr',
            role='admin'
        )
        session.add(personne)
        session.commit()
        
        form = FormGestionLogin()
        form.email.data = 'user@test.fr'
        form.mdp.data = 'password123'
        
        user, error = form.authenticate_user()
        assert user is not None
        assert error is None


def test_form_gestion_login_authenticate_mauvais_email(test_app, session):
    with test_app.app_context():
        form = FormGestionLogin()
        form.email.data = 'inexistant@test.fr'
        form.mdp.data = 'test'
        
        user, error = form.authenticate_user()
        assert user is None
        assert error == "Email inconnu."


def test_form_gestion_login_authenticate_mauvais_mdp(test_app, session):
    with test_app.app_context():
        from hashlib import sha256
        m = sha256()
        m.update('correct'.encode('utf-8'))
        
        personne = Personne(
            id_personne=2,
            mdp=m.hexdigest(),
            nom_personne='Test',
            email_personne='test@test.fr',
            role='admin'
        )
        session.add(personne)
        session.commit()
        
        form = FormGestionLogin()
        form.email.data = 'test@test.fr'
        form.mdp.data = 'incorrect'
        
        user, error = form.authenticate_user()
        assert user is None
        assert error == "Mot de passe incorrect."


def test_form_gestion_mdp_oublier_email_inconnu(test_app, session):
    with test_app.app_context():
        form = FormGestionMdpOublier()
        form.email.data = 'inconnu@test.fr'
        
        user, error = form.etape_1()
        assert user is None
        assert error == "Email inconnu."


def test_form_gestion_mdp_oublier_email_valide(test_app, session):
    with test_app.app_context():
        personne = Personne(
            id_personne=3,
            mdp='test',
            nom_personne='Test',
            email_personne='valid@test.fr',
            role='admin'
        )
        session.add(personne)
        session.commit()
        
        form = FormGestionMdpOublier()
        form.email.data = 'valid@test.fr'
        
        user, error = form.etape_1()
        assert user is not None
        assert error is None
        assert user.code_verification_mdp is not None


def test_form_information_fields(test_app):
    with test_app.app_context():
        form = FormInformation()
        assert hasattr(form, 'titre')
        assert hasattr(form, 'contenu')
        assert hasattr(form, 'ordre')


def test_form_inscription_event_fields(test_app):
    with test_app.app_context():
        form = FormInscriptionEvent()
        assert hasattr(form, 'nom')
        assert hasattr(form, 'prenom')
        assert hasattr(form, 'email')
        assert hasattr(form, 'date_naissance')
        assert hasattr(form, 'sexe')


def test_form_recherche_article_init(test_app, session):
    with test_app.app_context():
        article1 = Article(
            id_article=1,
            titre='Article 1',
            date_publication=date(2026, 1, 15)
        )
        article2 = Article(
            id_article=2,
            titre='Article 2',
            date_publication=date(2026, 2, 20)
        )
        session.add(article1)
        session.add(article2)
        session.commit()
        
        form = FormRechercheArticle()
        assert len(form.choix_year.choices) >= 1
        assert form.choix_year.choices[0] == ("all", "Tous les mois")


def test_form_configuration_mail_fields(test_app):
    with test_app.app_context():
        form = FormConfigurationMail()
        assert hasattr(form, 'mail_server')
        assert hasattr(form, 'mail_port')
        assert hasattr(form, 'mail_username')
        assert hasattr(form, 'mail_password')
