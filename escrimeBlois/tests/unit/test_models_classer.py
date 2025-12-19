from escrimeBlois.models import Classer, Inscription, Evenement
from escrimeBlois import db
import pytest
import datetime


def test_classer_creation(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        db.session.add(insc)
        db.session.commit()
        clas = Classer(id_competition=1, id_inscription=1, point=10)
        assert clas.point == 10


def test_classer_repr(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        db.session.add(insc)
        db.session.commit()
        clas = Classer(id_competition=1, id_inscription=1, point=10)
        assert repr(clas) == "Classer 1-1"


def test_classer_str(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        db.session.add(insc)
        db.session.commit()
        clas = Classer(id_competition=1, id_inscription=1, point=10)
        assert str(clas) == "Points: 10"


def test_validate_evenement_type_valid(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        db.session.add(insc)
        db.session.commit()
        clas = Classer(id_competition=1, id_inscription=1, point=10)
        result = clas.validate_evenement_type('id_competition', 1)
        assert result == 1


def test_validate_evenement_type_invalid_not_competition(testapp):
    with testapp.app_context():
        ev = Evenement(id_evenement=2,
                       nom="Autre Événement",
                       date=datetime.date.today(),
                       heure=10,
                       categorie="Loisir",
                       lieu="Test",
                       description="Test",
                       type_evenement="autre")
        db.session.add(ev)
        insc = Inscription(id_inscription=2, id_evenement=2)
        db.session.add(insc)
        db.session.commit()
        with pytest.raises(ValueError, match="doit être de type Compétition"):
            clas = Classer(id_competition=2, id_inscription=2, point=10)


def test_validate_evenement_type_invalid_not_found(testapp):
    with testapp.app_context():
        with pytest.raises(ValueError, match="Événement 999 introuvable"):
            clas = Classer(id_inscription=1, id_competition=999, point=10)
