from escrimeBlois.models import Repondre, Personne, Formulaire
from escrimeBlois import db
import pytest
import datetime


def test_repondre_creation(testapp, sample_personne):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        db.session.add(form)
        db.session.commit()
        rep = Repondre(id_responsable=sample_personne.id_personne,
                       id_formulaire=1)
        assert rep.id_responsable == sample_personne.id_personne


def test_repondre_repr(testapp, sample_personne):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        db.session.add(form)
        db.session.commit()
        rep = Repondre(id_responsable=sample_personne.id_personne,
                       id_formulaire=1)
        assert repr(rep) == f"Repondre {sample_personne.id_personne}-1"


def test_repondre_str(testapp, sample_personne):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        db.session.add(form)
        db.session.commit()
        rep = Repondre(id_responsable=sample_personne.id_personne,
                       id_formulaire=1)
        assert str(rep) == f"Repondre {sample_personne.id_personne}-1"


def test_validate_responsable_type_valid(testapp, sample_personne):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        db.session.add(form)
        db.session.commit()
        rep = Repondre(id_responsable=sample_personne.id_personne,
                       id_formulaire=1)
        result = rep.validate_responsable_type('id_responsable', sample_personne.id_personne)
        assert result == sample_personne.id_personne


def test_validate_responsable_type_invalid_not_responsable(testapp):
    with testapp.app_context():
        resp = Personne(mdp="hash",
                        nom_personne="Dup",
                        prenom_personne="Hayaa",
                        email_personne="hayaa@example.com",
                        telephone="0123456789",
                        sexe="M",
                        adresse="123 Rue Test",
                        date_naissance=datetime.date(1990, 1, 1),
                        eleve=True,
                        arme_principale="épée",
                        niveau="pro",
                        role="membre")
        db.session.add(resp)
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        db.session.add(form)
        db.session.commit()
        with pytest.raises(ValueError,
                           match="doit être de type 'responsable'"):
            rep = Repondre(id_responsable=resp.id_personne, id_formulaire=1)


def test_validate_responsable_type_invalid_not_found(testapp):
    with testapp.app_context():
        with pytest.raises(ValueError, match="introuvable"):
            rep = Repondre(id_responsable=999, id_formulaire=1)
