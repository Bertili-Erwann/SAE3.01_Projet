from escrimeBlois.models import Personne, load_user
import pytest


def test_personne_creation(sample_personne):
    assert sample_personne.id_personne is not None
    assert sample_personne.nom_personne == "Pontdu"


def test_personne_repr(sample_personne):
    assert repr(sample_personne) == f"Personne {sample_personne.id_personne}"


def test_personne_str(sample_personne):
    assert str(sample_personne) == "Pontdu Naej"


def test_validate_role_valid_membre(sample_personne):
    result = sample_personne.validate_role('role', 'responsable')
    assert result == 'responsable'


def test_validate_role_invalid_membre():
    with pytest.raises(ValueError,
                       match="n'a pas rempli un des champs requis"):
        pers = Personne(role="membre")


def test_validate_role_valid_admin():
    pers = Personne(role="admin")
    result = pers.validate_role('role', 'admin')
    assert result == 'admin'


def test_validate_role_invalid_admin():
    with pytest.raises(ValueError, match="a des informations en trop"):
        pers = Personne(eleve=True, role="admin")


def test_load_user_valid(testapp, sample_personne):
    with testapp.app_context():
        assert sample_personne == load_user(sample_personne.id_personne)
