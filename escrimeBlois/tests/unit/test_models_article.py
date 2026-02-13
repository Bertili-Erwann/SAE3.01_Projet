from escrimeBlois.models import Article, Personne
from escrimeBlois import db
import pytest
import datetime


def test_article_creation(testapp, sample_personne):
    with testapp.app_context():
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=sample_personne.id_personne)
        assert art.titre == "Test Article"


def test_article_repr(testapp, sample_personne):
    with testapp.app_context():
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=sample_personne.id_personne)
        assert repr(art) == "Article 1"


def test_article_str(testapp, sample_personne):
    with testapp.app_context():
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=sample_personne.id_personne)
        assert str(art) == "Test Article"


def test_validate_responsable_type_valid(testapp, sample_personne):
    with testapp.app_context():
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=sample_personne.id_personne)
        sample_personne.role = "responsable"
        db.session.commit()
        result = art.validate_responsable_type('id_responsable', sample_personne.id_personne)
        assert result == sample_personne.id_personne


def test_validate_responsable_type_invalid_not_resp(testapp):
    with testapp.app_context():
        pers = Personne(mdp="hash",
                        nom_personne="Pontdu",
                        prenom_personne="Naej",
                        email_personne="neah@example.com",
                        telephone="0123456789",
                        sexe="M",
                        adresse="123 Rue Test",
                        date_naissance=datetime.date(1990, 1, 1),
                        eleve=True,
                        arme_principale="épée",
                        niveau="pro",
                        role="membre")
        db.session.add(pers)
        db.session.commit()
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=2)
        with pytest.raises(ValueError,
                           match="doit être de type 'responsable'"):
            art.validate_responsable_type('id_responsable', pers.id_personne)


def test_validate_responsable_type_invalid_not_found(testapp):
    with testapp.app_context():
        art = Article(id_article=1,
                      titre="Test Article",
                      date_publication=datetime.date.today(),
                      description="Desc",
                      categorie="News",
                      commentable=True,
                      responsable_id=999)
        with pytest.raises(ValueError, match="introuvable"):
            art.validate_responsable_type('id_responsable', 999)
