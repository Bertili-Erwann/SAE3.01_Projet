import pytest
from escrimeBlois import app, db
from escrimeBlois.models import Personne, Evenement
import datetime


@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })
    with app.app_context():
        db.create_all()

    yield app
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(testapp):
    return testapp.test_client()


@pytest.fixture
def sample_personne(testapp):
    with testapp.app_context():
        resp = Personne(mdp="hash",
                        nom_personne="Pontdu",
                        prenom_personne="Naej",
                        email_personne="neah@example.com",
                        telephone="0123456789",
                        sexe="M",
                        adresse="123 Rue de Test",
                        date_naissance=datetime.date(1990, 1, 1),
                        eleve=True,
                        arme_principale="épée",
                        niveau="pro",
                        role="responsable")
        db.session.add(resp)
        db.session.commit()
        yield resp
        db.session.delete(resp)
        db.session.commit()


@pytest.fixture
def sample_evenement(testapp):
    with testapp.app_context():
        ev = Evenement(id_evenement=1,
                       nom="Compétition Test",
                       date=datetime.date.today(),
                       heure=10,
                       categorie="Senior",
                       lieu="Blois",
                       description="Test",
                       sexe="M",
                       niveau="avancé",
                       discipline="épée",
                       cooperative="Club X",
                       type_evenement="Compétition")
        db.session.add(ev)
        db.session.commit()
        yield ev
        db.session.delete(ev)
        db.session.commit()
