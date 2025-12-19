from escrimeBlois.models import Evenement
import pytest


def test_evenement_creation(sample_evenement):
    assert sample_evenement.id_evenement == 1
    assert sample_evenement.type_evenement == "Compétition"


def test_evenement_repr(sample_evenement):
    assert repr(sample_evenement) == "Evenement 1"


def test_evenement_str(sample_evenement):
    assert str(sample_evenement) == "Compétition"


def test_validate_type_evenement_valid_competition(sample_evenement):
    result = sample_evenement.validate_attributs_evenement(
        'type_evenement', 'Compétition')
    assert result == 'Compétition'


def test_validate_type_evenement_invalid_competition():
    with pytest.raises(ValueError,
                       match="n'a pas rempli un des champs requis"):
        ev = Evenement(type_evenement="Compétition")


def test_validate_type_evenement_valid_other():
    ev = Evenement(type_evenement="autre")
    result = ev.validate_attributs_evenement('type_evenement', 'autre')
    assert result == 'autre'


def test_validate_type_evenement_invalid_other():
    ev = Evenement(type_evenement="autre", niveau="test")
    with pytest.raises(ValueError, match="a des informations en trop"):
        ev.validate_attributs_evenement('type_evenement', 'autre')
