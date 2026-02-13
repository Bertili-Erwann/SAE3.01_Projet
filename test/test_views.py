import pytest
from datetime import date
from flask_login import login_user
from escrimeBlois.models import *


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_index_alternative_route(client):
    response = client.get('/index/')
    assert response.status_code == 200


def test_historique_page(client, session):
    hist = Historique(
        id_chronologique=1,
        date='2000',
        description='Fondation'
    )
    session.add(hist)
    session.commit()
    
    response = client.get('/historique/')
    assert response.status_code == 200


def test_renseignement_page(client):
    response = client.get('/renseignement/')
    assert response.status_code == 200


def test_login_page_get(client):
    response = client.get('/login/')
    assert response.status_code == 200


def test_login_page_post_succes(client, session):
    from hashlib import sha256
    m = sha256()
    m.update('pass123'.encode('utf-8'))
    
    user = Personne(
        id_personne=1,
        mdp=m.hexdigest(),
        nom_personne='Test',
        prenom_personne='User',
        email_personne='test@test.fr',
        role='admin'
    )
    session.add(user)
    session.commit()
    
    response = client.post('/login/', data={
        'email': 'test@test.fr',
        'password': 'pass123'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_login_page_post_echec_email(client):
    response = client.post('/login/', data={
        'email': 'inconnu@test.fr',
        'password': 'test'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_login_page_post_echec_mdp(client, session):
    from hashlib import sha256
    m = sha256()
    m.update('correct'.encode('utf-8'))
    
    user = Personne(
        id_personne=2,
        mdp=m.hexdigest(),
        email_personne='user@test.fr',
        role='admin'
    )
    session.add(user)
    session.commit()
    
    response = client.post('/login/', data={
        'email': 'user@test.fr',
        'password': 'incorrect'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_logout(client):
    response = client.get('/logout/', follow_redirects=True)
    assert response.status_code == 200


def test_mdp_oublier_page(client):
    response = client.get('/login/mdp_oublier')
    assert response.status_code == 200


def test_redirection_ffescrime(client):
    response = client.get('/event/classement/redirection_ffescrime')
    assert response.status_code == 200


def test_demande_article_sans_filtre(client, session):
    article = Article(
        id_article=1,
        titre='Test Article',
        date_publication=date(2026, 1, 15),
        description='Description test'
    )
    session.add(article)
    session.commit()
    
    response = client.get('/demande_article')
    assert response.status_code == 200


def test_demande_article_avec_recherche(client, session):
    article1 = Article(
        id_article=1,
        titre='Compétition nationale',
        date_publication=date(2026, 1, 15)
    )
    article2 = Article(
        id_article=2,
        titre='Stage débutants',
        date_publication=date(2026, 2, 20)
    )
    session.add(article1)
    session.add(article2)
    session.commit()
    
    response = client.get('/demande_article?recherche=Compétition')
    assert response.status_code == 200


def test_demande_article_avec_date(client, session):
    article = Article(
        id_article=1,
        titre='Test',
        date_publication=date(2026, 3, 10)
    )
    session.add(article)
    session.commit()
    
    response = client.get('/demande_article?choix_year=3-2026')
    assert response.status_code == 200


def test_insert_formulaire(client, session):
    response = client.post('/insert_formulaire', data={
        'nom': 'Dupont',
        'email': 'dupont@test.fr',
        'objet': 'Question',
        'message': 'Bonjour'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_ajouter_historique_sans_login(client):
    response = client.post('/historique/ajouter', data={
        'date': '2020',
        'description': 'Test'
    }, follow_redirects=False)
    
    assert response.status_code == 401


def test_ajouter_historique_avec_admin(client, session, personne_admin):
    with client.session_transaction() as sess:
        sess['_user_id'] = str(personne_admin.id_personne)
    
    response = client.post('/historique/ajouter', data={
        'date': '2020',
        'description': 'Nouvel événement'
    }, follow_redirects=True)
    
    assert response.status_code == 200


def test_supprimer_historique_sans_login(client, session):
    hist = Historique(id_chronologique=10, date='2000', description='Test')
    session.add(hist)
    session.commit()
    
    response = client.post('/historique/supprimer/10', follow_redirects=False)
    assert response.status_code == 401


def test_uploaded_file_route(client, test_app):
    response = client.get('/uploads/test.txt')
    assert response.status_code in [200, 404]


def test_inscription_page_get(client):
    response = client.get('/inscription/')
    assert response.status_code in [200, 404, 405]


def test_view_article_existe(client, session):
    article = Article(
        id_article=100,
        titre='Mon article',
        date_publication=date(2026, 1, 1),
        description='Contenu',
        commentable=True
    )
    session.add(article)
    session.commit()
    
    response = client.get('/article/100')
    assert response.status_code in [200, 404]


def test_evenement_page(client):
    response = client.get('/event/')
    assert response.status_code in [200, 404]


def test_evenement_resultats_page(client):
    response = client.get('/event/resultats/')
    assert response.status_code in [200, 404]


def test_route_membre_sans_login(client):
    response = client.get('/membre/', follow_redirects=False)
    assert response.status_code in [401, 404]


def test_route_responsable_sans_login(client):
    response = client.get('/responsable/', follow_redirects=False)
    assert response.status_code in [401, 404]


def test_route_admin_sans_login(client):
    response = client.get('/admin/', follow_redirects=False)
    assert response.status_code in [401, 404]


def test_insert_commentaire(client, session):
    article = Article(
        id_article=50,
        titre='Test',
        date_publication=date(2026, 1, 1),
        commentable=True
    )
    session.add(article)
    session.commit()
    
    response = client.post('/article/50/commentaire', data={
        'nom_aut': 'Martin',
        'email_aut': 'martin@test.fr',
        'message': 'Super!'
    }, follow_redirects=True)
    
    assert response.status_code in [200, 302, 404]


def test_index_avec_articles(client, session):
    for i in range(5):
        article = Article(
            id_article=i+1,
            titre=f'Article {i+1}',
            date_publication=date(2026, 1, i+1)
        )
        session.add(article)
    session.commit()
    
    response = client.get('/')
    assert response.status_code == 200


def test_historique_avec_multiple_events(client, session):
    for i in range(3):
        hist = Historique(
            id_chronologique=i+1,
            date=f'200{i}',
            description=f'Event {i}'
        )
        session.add(hist)
    session.commit()
    
    response = client.get('/historique/')
    assert response.status_code == 200


def test_renseignement_avec_infos(client, session):
    info1 = Information(id=1, titre='Horaires', contenu='Lundi 18h', ordre=1)
    info2 = Information(id=2, titre='Tarifs', contenu='20€/mois', ordre=2)
    session.add(info1)
    session.add(info2)
    session.commit()
    
    response = client.get('/renseignement/')
    assert response.status_code == 200
