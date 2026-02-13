import pytest
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from escrimeBlois.app import app, db
from escrimeBlois.models import *


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def session(test_app):
    with test_app.app_context():
        yield db.session


@pytest.fixture
def personne_admin(session):
    admin = Personne(
        id_personne=1,
        mdp='admin123',
        nom_personne='Durand',
        prenom_personne='Jean',
        email_personne='admin@test.fr',
        telephone='0612345678',
        role='admin'
    )
    session.add(admin)
    session.commit()
    return admin


@pytest.fixture
def personne_membre(session):
    membre = Personne(
        id_personne=2,
        mdp='membre123',
        nom_personne='Martin',
        prenom_personne='Sophie',
        email_personne='membre@test.fr',
        telephone='0698765432',
        sexe='F',
        adresse='10 rue de Paris',
        date_naissance=date(1995, 5, 15),
        eleve=True,
        arme_principale='épée',
        niveau='intermédiaire',
        role='membre'
    )
    session.add(membre)
    session.commit()
    return membre


@pytest.fixture
def evenement_competition(session):
    event = Evenement(
        id_evenement=1,
        nom='Championnat Regional',
        date=date(2026, 6, 15),
        heure=540,
        categorie='Senior',
        lieu='Gymnase Municipal',
        description='Compétition régionale',
        sexe='M',
        niveau='avancé',
        discipline='épée',
        cooperative='FFE',
        type_evenement='Compétition'
    )
    session.add(event)
    session.commit()
    return event


@pytest.fixture
def evenement_simple(session):
    event = Evenement(
        id_evenement=2,
        nom='Stage débutants',
        date=date(2026, 7, 20),
        heure=840,
        categorie='Débutant',
        lieu='Salle Escrime',
        description='Stage pour débutants',
        type_evenement='Stage'
    )
    session.add(event)
    session.commit()
    return event
