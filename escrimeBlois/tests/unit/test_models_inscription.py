from escrimeBlois.models import Inscription


def test_inscription_creation(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        assert insc.id_inscription == 1


def test_inscription_repr(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        assert repr(insc) == "Inscription 1"


def test_inscription_str(testapp, sample_evenement):
    with testapp.app_context():
        insc = Inscription(id_inscription=1,
                           id_evenement=sample_evenement.id_evenement)
        assert str(insc) == "Inscription 1"
