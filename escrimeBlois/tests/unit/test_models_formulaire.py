from escrimeBlois.models import Formulaire


def test_formulaire_creation(testapp):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        assert form.objet == "Sujet"


def test_formulaire_repr(testapp):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        assert repr(form) == "Formulaire 1"


def test_formulaire_str(testapp):
    with testapp.app_context():
        form = Formulaire(id_formulaire=1,
                          nom_auteur="Test",
                          email_auteur="test@example.com",
                          objet="Sujet",
                          message="Message")
        assert str(form) == "Sujet"
