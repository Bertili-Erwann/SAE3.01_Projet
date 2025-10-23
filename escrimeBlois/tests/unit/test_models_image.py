from escrimeBlois.models import Image


def test_image_creation(testapp):
    with testapp.app_context():
        img = Image(id_image=1,
                    nom_image="test.jpg",
                    url_image="http://example.com/test.jpg")
        assert img.nom_image == "test.jpg"
