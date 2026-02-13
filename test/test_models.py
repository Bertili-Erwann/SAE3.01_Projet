import pytest
from datetime import date
from escrimeBlois.models import *


def test_personne_creation_admin(session):
    admin = Personne(
        id_personne=10,
        mdp='test123',
        nom_personne='Admin',
        prenom_personne='Test',
        email_personne='admin@test.com',
        role='admin'
    )
    session.add(admin)
    session.commit()
    
    result = Personne.query.get(10)
    assert result.nom_personne == 'Admin'
    assert result.role == 'admin'


def test_personne_creation_membre(session):
    membre = Personne(
        id_personne=11,
        mdp='membre456',
        nom_personne='Membre',
        prenom_personne='Test',
        email_personne='membre@test.com',
        sexe='H',
        adresse='5 rue Test',
        date_naissance=date(2000, 1, 1),
        eleve=False,
        arme_principale='fleuret',
        niveau='débutant',
        role='membre'
    )
    session.add(membre)
    session.commit()
    
    result = Personne.query.get(11)
    assert result.arme_principale == 'fleuret'
    assert result.niveau == 'débutant'


def test_personne_validation_role_membre_sans_infos(session):
    with pytest.raises(ValueError):
        personne = Personne(
            id_personne=12,
            mdp='test',
            nom_personne='Test',
            prenom_personne='Test',
            email_personne='test@test.com',
            role='membre'
        )
        session.add(personne)
        session.commit()


def test_personne_get_id(personne_admin):
    assert personne_admin.get_id() == 1


def test_personne_repr(personne_admin):
    assert repr(personne_admin) == "Personne 1"


def test_personne_str(personne_admin):
    assert str(personne_admin) == "Durand Jean"


def test_demande_inscription_creation(session):
    demande = Demande_inscription(
        id_inscription=1,
        nom='Dupont',
        prenom='Marie',
        mot_de_passe='pass123',
        sexe='F',
        date_naissance=date(1998, 3, 10),
        num_tel='0123456789',
        adresse_mail='marie@test.fr',
        adresse_postale='12 rue Test',
        eleve=True,
        justificatif={'filename': 'test.pdf'}
    )
    session.add(demande)
    session.commit()
    
    result = Demande_inscription.query.get(1)
    assert result.nom == 'Dupont'
    assert result.eleve == True


def test_demande_inscription_repr(session):
    demande = Demande_inscription(id_inscription=2, nom='Test')
    session.add(demande)
    session.commit()
    assert repr(demande) == "Demande_inscription 2"


def test_evenement_creation_competition(session):
    event = Evenement(
        id_evenement=10,
        nom='Test Competition',
        date=date(2026, 12, 1),
        heure=600,
        categorie='Junior',
        lieu='Salle Test',
        description='Test',
        sexe='M',
        niveau='avancé',
        discipline='sabre',
        cooperative='Test Club',
        type_evenement='Compétition'
    )
    session.add(event)
    session.commit()
    
    result = Evenement.query.get(10)
    assert result.discipline == 'sabre'
    assert result.type_evenement == 'Compétition'


def test_evenement_heure_formatee(evenement_competition):
    assert evenement_competition.heure_formatee == "09:00"


def test_evenement_heure_formatee_none(session):
    event = Evenement(
        id_evenement=11,
        nom='Test',
        date=date(2026, 1, 1),
        type_evenement='Stage'
    )
    session.add(event)
    session.commit()
    assert event.heure_formatee == "-"


def test_evenement_validation_competition_sans_infos(session):
    with pytest.raises(ValueError):
        event = Evenement(
            id_evenement=12,
            nom='Test',
            date=date(2026, 1, 1),
            type_evenement='Compétition'
        )
        session.add(event)
        session.commit()


def test_evenement_validation_stage_avec_infos(session):
    with pytest.raises(ValueError):
        event = Evenement(
            id_evenement=13,
            nom='Test',
            date=date(2026, 1, 1),
            niveau='avancé',
            type_evenement='Stage'
        )
        session.add(event)
        session.commit()


def test_evenement_repr(evenement_simple):
    assert repr(evenement_simple) == "Evenement 2"


def test_evenement_str(evenement_simple):
    assert str(evenement_simple) == "Stage"


def test_inscription_creation(session, evenement_simple):
    inscription = Inscription(
        id_inscription=1,
        id_evenement=evenement_simple.id_evenement,
        nom='Dupuis',
        prenom='Alice',
        email='alice@test.fr',
        sexe='F',
        date_naissance=date(2005, 8, 20)
    )
    session.add(inscription)
    session.commit()
    
    result = Inscription.query.get(1)
    assert result.nom == 'Dupuis'
    assert result.email == 'alice@test.fr'


def test_inscription_avec_personne(session, evenement_simple, personne_membre):
    inscription = Inscription(
        id_inscription=2,
        id_evenement=evenement_simple.id_evenement,
        nom=personne_membre.nom_personne,
        prenom=personne_membre.prenom_personne,
        email=personne_membre.email_personne,
        id_personne=personne_membre.id_personne
    )
    session.add(inscription)
    session.commit()
    
    result = Inscription.query.get(2)
    assert result.id_personne == 2


def test_inscription_repr(session, evenement_simple):
    inscription = Inscription(id_inscription=3, id_evenement=evenement_simple.id_evenement)
    session.add(inscription)
    session.commit()
    assert repr(inscription) == "Inscription 3"


def test_classer_creation(session, evenement_competition):
    inscription = Inscription(
        id_inscription=10,
        id_evenement=evenement_competition.id_evenement,
        nom='Test',
        prenom='Test'
    )
    session.add(inscription)
    session.commit()
    
    classement = Classer(
        id_competition=evenement_competition.id_evenement,
        id_inscription=inscription.id_inscription,
        point=150
    )
    session.add(classement)
    session.commit()
    
    result = Classer.query.filter_by(
        id_competition=evenement_competition.id_evenement,
        id_inscription=inscription.id_inscription
    ).first()
    assert result.point == 150


def test_classer_validation_pas_competition(session, evenement_simple):
    inscription = Inscription(
        id_inscription=11,
        id_evenement=evenement_simple.id_evenement,
        nom='Test',
        prenom='Test'
    )
    session.add(inscription)
    session.commit()
    
    with pytest.raises(ValueError):
        classement = Classer(
            id_competition=evenement_simple.id_evenement,
            id_inscription=inscription.id_inscription,
            point=100
        )
        session.add(classement)
        session.commit()


def test_classer_repr(session, evenement_competition):
    inscription = Inscription(
        id_inscription=12,
        id_evenement=evenement_competition.id_evenement,
        nom='Test'
    )
    session.add(inscription)
    session.commit()
    
    classement = Classer(
        id_competition=evenement_competition.id_evenement,
        id_inscription=inscription.id_inscription,
        point=200
    )
    session.add(classement)
    session.commit()
    
    assert repr(classement) == f"Classer {evenement_competition.id_evenement}-{inscription.id_inscription}"


def test_classer_str(session, evenement_competition):
    inscription = Inscription(
        id_inscription=13,
        id_evenement=evenement_competition.id_evenement,
        nom='Test'
    )
    session.add(inscription)
    session.commit()
    
    classement = Classer(
        id_competition=evenement_competition.id_evenement,
        id_inscription=inscription.id_inscription,
        point=175
    )
    session.add(classement)
    session.commit()
    
    assert str(classement) == "Points: 175"


def test_formulaire_creation(session):
    form = Formulaire(
        id_formulaire=1,
        nom_auteur='Lemoine',
        email_auteur='lemoine@test.fr',
        objet='Question sur les horaires',
        message='Bonjour, quels sont les horaires?'
    )
    session.add(form)
    session.commit()
    
    result = Formulaire.query.get(1)
    assert result.objet == 'Question sur les horaires'


def test_formulaire_repr(session):
    form = Formulaire(id_formulaire=2, objet='Test')
    session.add(form)
    session.commit()
    assert repr(form) == "Formulaire 2"


def test_formulaire_str(session):
    form = Formulaire(id_formulaire=3, objet='Mon objet')
    session.add(form)
    session.commit()
    assert str(form) == 'Mon objet'


def test_repondre_creation(session, personne_membre):
    personne_membre.role = 'responsable'
    session.commit()
    
    form = Formulaire(
        id_formulaire=10,
        nom_auteur='Test',
        email_auteur='test@test.fr',
        objet='Test',
        message='Test'
    )
    session.add(form)
    session.commit()
    
    reponse = Repondre(
        id_responsable=personne_membre.id_personne,
        id_formulaire=form.id_formulaire
    )
    session.add(reponse)
    session.commit()
    
    result = Repondre.query.filter_by(
        id_responsable=personne_membre.id_personne
    ).first()
    assert result is not None


def test_repondre_validation_pas_responsable(session, personne_admin):
    form = Formulaire(id_formulaire=11, objet='Test')
    session.add(form)
    session.commit()
    
    with pytest.raises(ValueError):
        reponse = Repondre(
            id_responsable=personne_admin.id_personne,
            id_formulaire=form.id_formulaire
        )
        session.add(reponse)
        session.commit()


def test_article_creation(session):
    article = Article(
        id_article=1,
        titre='Nouveau club',
        date_publication=date(2026, 1, 15),
        description='Ouverture du nouveau club',
        categorie='Actualités',
        commentable=True
    )
    session.add(article)
    session.commit()
    
    result = Article.query.get(1)
    assert result.titre == 'Nouveau club'


def test_article_repr(session):
    article = Article(id_article=2, titre='Test')
    session.add(article)
    session.commit()
    assert repr(article) == "Article 2"


def test_article_str(session):
    article = Article(id_article=3, titre='Mon titre')
    session.add(article)
    session.commit()
    assert str(article) == 'Mon titre'


def test_image_creation(session):
    image = Image(
        id_image=1,
        nom_image='logo.png',
        url_image='/static/images/logo.png'
    )
    session.add(image)
    session.commit()
    
    result = Image.query.get(1)
    assert result.nom_image == 'logo.png'


def test_posseder_creation(session):
    article = Article(id_article=10, titre='Test')
    image = Image(id_image=10, nom_image='test.jpg')
    session.add(article)
    session.add(image)
    session.commit()
    
    posseder = Posseder(
        id_article=article.id_article,
        id_image=image.id_image
    )
    session.add(posseder)
    session.commit()
    
    result = Posseder.query.filter_by(id_article=10).first()
    assert result.id_image == 10


def test_gerer_creation(session, personne_admin):
    demande = Demande_inscription(
        id_inscription=10,
        nom='Test'
    )
    session.add(demande)
    session.commit()
    
    gerer = Gerer(
        id_admin=personne_admin.id_personne,
        id_inscription=demande.id_inscription
    )
    session.add(gerer)
    session.commit()
    
    result = Gerer.query.filter_by(id_admin=1).first()
    assert result is not None


def test_gerer_validation_pas_admin(session, personne_membre):
    demande = Demande_inscription(id_inscription=11, nom='Test')
    session.add(demande)
    session.commit()
    
    with pytest.raises(ValueError):
        gerer = Gerer(
            id_admin=personne_membre.id_personne,
            id_inscription=demande.id_inscription
        )
        session.add(gerer)
        session.commit()


def test_commentaire_creation(session):
    article = Article(id_article=20, titre='Test', commentable=True)
    session.add(article)
    session.commit()
    
    commentaire = Commentaire(
        id_commentaire=1,
        id_article=article.id_article,
        nom_aut='Dupont',
        email_aut='dupont@test.fr',
        message_com='Super article!'
    )
    session.add(commentaire)
    session.commit()
    
    result = Commentaire.query.get(1)
    assert result.message_com == 'Super article!'


def test_information_creation(session):
    info = Information(
        id=1,
        titre='Horaires',
        contenu='Lundi: 18h-20h',
        ordre=1
    )
    session.add(info)
    session.commit()
    
    result = Information.query.get(1)
    assert result.titre == 'Horaires'


def test_historique_creation(session):
    hist = Historique(
        id_chronologique=1,
        date='1995',
        description='Fondation du club'
    )
    session.add(hist)
    session.commit()
    
    result = Historique.query.get(1)
    assert result.description == 'Fondation du club'
