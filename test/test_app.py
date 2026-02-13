import pytest
from escrimeBlois.app import urlify


def test_urlify_avec_url():
    text = "Visitez https://example.com pour plus d'infos"
    result = urlify(text)
    assert 'href="https://example.com"' in str(result)
    assert 'target="_blank"' in str(result)


def test_urlify_sans_url():
    text = "Texte sans lien"
    result = urlify(text)
    assert 'href' not in str(result)


def test_urlify_multiple_urls():
    text = "Voir https://site1.com et http://site2.com"
    result = urlify(text)
    assert 'href="https://site1.com"' in str(result)
    assert 'href="http://site2.com"' in str(result)


def test_urlify_url_complexe():
    text = "Page: https://example.com/path?param=value"
    result = urlify(text)
    assert 'href="https://example.com/path?param=value"' in str(result)
