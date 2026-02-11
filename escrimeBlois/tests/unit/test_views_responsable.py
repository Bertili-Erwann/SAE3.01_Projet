# Test de la views fait avec l'aide de l'IA

import pytest
from flask import url_for
from flask_login import login_user
from escrimeBlois.models import Personne, Article, Evenement, Formulaire
from escrimeBlois import db
import datetime
from hashlib import sha256


@pytest.fixture
def responsable_user(testapp):
    """Crée un utilisateur avec le rôle responsable"""
    with testapp.app_context():
        m = sha256()
        m.update("password123".encode("utf-8"))
        hashed_password = m.hexdigest()
        
        responsable = Personne(
            mdp=hashed_password,
            nom_personne="Dupont",
            prenom_personne="Marie",
            email_personne="marie.dupont@example.com",
            telephone="0234567890",
            sexe="F",
            adresse="456 Avenue Test",
            date_naissance=datetime.date(1985, 3, 20),
            eleve=False,
            arme_principale="fleuret",
            niveau="expert",
            role="responsable"
        )
        db.session.add(responsable)
        db.session.commit()
        yield responsable
        db.session.delete(responsable)
        db.session.commit()


@pytest.fixture
def logged_responsable_client(testapp, client, responsable_user):
    """Client avec un responsable connecté"""
    with client:
        with testapp.app_context():
            response = client.post('/login/', data={
                'email': responsable_user.email_personne,
                'password': 'password123'
            }, follow_redirects=True)
        yield client


class TestResponsableAccess:
    """Tests pour vérifier les accès d'un responsable connecté"""
    
    # ======================================== PAGES RESPONSABLE ACCESSIBLES ========================================
    
    def test_responsable_acces_gestion_formulaire(self, logged_responsable_client):
        """Un responsable peut accéder à la gestion des formulaires"""
        response = logged_responsable_client.get('/responsable/gestion_formulaire/')
        assert response.status_code == 200
    
    def test_responsable_acces_ajouter_article(self, logged_responsable_client):
        """Un responsable peut accéder à l'ajout d'article"""
        response = logged_responsable_client.get('/responsable/ajouter_article/')
        assert response.status_code == 200
    
    def test_responsable_acces_creer_evenement(self, logged_responsable_client):
        """Un responsable peut créer un événement"""
        response = logged_responsable_client.get('/responsable/creer_evenement/')
        assert response.status_code == 200
    
    def test_responsable_acces_consultation_formulaire(self, testapp, logged_responsable_client):
        """Un responsable peut consulter un formulaire spécifique"""
        with testapp.app_context():
            form = Formulaire(
                nom_auteur="Test User",
                email_auteur="test@test.com",
                objet="Test",
                message="Message test"
            )
            db.session.add(form)
            db.session.commit()
            form_id = form.id_formulaire
        
        response = logged_responsable_client.get(f'/responsable/consultation_formulaire/{form_id}/')
        assert response.status_code == 200
    
    def test_responsable_peut_ajouter_article(self, testapp, logged_responsable_client, responsable_user):
        """Un responsable peut ajouter un article via POST"""
        response = logged_responsable_client.post('/responsable/ajouter_article/',
                                                  data={
                                                      'titre': 'Nouvel article',
                                                      'description': 'Description test',
                                                      'theme': 'Actualités',
                                                      'lien': '',
                                                      'commentable': 'on'
                                                  },
                                                  follow_redirects=True)
        assert response.status_code == 200
    
    def test_responsable_peut_creer_evenement(self, logged_responsable_client):
        """Un responsable peut créer un événement via POST"""
        response = logged_responsable_client.post('/responsable/creer_evenement/',
                                                  data={
                                                      'name_create_event': 'Stage Test',
                                                      'categories_create_event': 'Senior',
                                                      'date_create_event': '2026-06-15',
                                                      'hour_create_event': '14:30',
                                                      'location_create_event': 'Blois',
                                                      'bottom_create_event': 'Description stage',
                                                      'types_create_event': 'stage'
                                                  },
                                                  follow_redirects=True)
        assert response.status_code == 200
    
    # ======================================== PAGES PUBLIQUES ACCESSIBLES ========================================
    
    def test_responsable_acces_index(self, logged_responsable_client):
        """Un responsable peut accéder à la page d'accueil"""
        response = logged_responsable_client.get('/')
        assert response.status_code == 200
    
    def test_responsable_acces_calendrier(self, logged_responsable_client):
        """Un responsable peut accéder au calendrier"""
        response = logged_responsable_client.get('/evenement/calendrier')
        assert response.status_code == 200
    
    def test_responsable_acces_resultats(self, logged_responsable_client):
        """Un responsable peut voir les résultats publics"""
        response = logged_responsable_client.get('/evenement/résultats')
        assert response.status_code == 200
    
    def test_responsable_acces_resultats_passes_membre(self, logged_responsable_client):
        """Un responsable peut voir les résultats passés (route membre autorisée pour responsable)"""
        response = logged_responsable_client.get('/membre/resultats_passes/')
        assert response.status_code == 200
    
    # ======================================== PAGES ADMIN INACCESSIBLES ========================================
    
    def test_responsable_refuse_admin_inscription_club(self, logged_responsable_client):
        """Un responsable ne peut pas accéder à la gestion des inscriptions club"""
        response = logged_responsable_client.get('/admin/gestion_inscription/club')
        assert response.status_code == 302
    
    def test_responsable_refuse_admin_inscription_evenement(self, logged_responsable_client):
        """Un responsable ne peut pas accéder à la gestion des inscriptions événements"""
        response = logged_responsable_client.get('/admin/gestion_inscription/evenement')
        assert response.status_code == 302
    
    def test_responsable_refuse_admin_miseajour_membres(self, logged_responsable_client):
        """Un responsable ne peut pas mettre à jour les membres"""
        response = logged_responsable_client.get('/admin/miseajour/membres')
        assert response.status_code == 302
    
    def test_responsable_refuse_admin_creation_competition(self, logged_responsable_client):
        """Un responsable ne peut pas créer de compétition (réservé admin)"""
        response = logged_responsable_client.get('/admin/creation_competition')
        assert response.status_code == 302
    
    def test_responsable_refuse_admin_resultats(self, logged_responsable_client):
        """Un responsable ne peut pas accéder à la gestion admin des résultats"""
        response = logged_responsable_client.get('/admin/resultats')
        assert response.status_code == 302
    
    def test_responsable_refuse_supprimer_membre(self, testapp, logged_responsable_client):
        """Un responsable ne peut pas supprimer un membre"""
        with testapp.app_context():
            membre = Personne(
                mdp="hash",
                nom_personne="ToDelete",
                prenom_personne="User",
                email_personne="delete@test.com",
                telephone="0000000000",
                sexe="M",
                adresse="Test",
                date_naissance=datetime.date(1990, 1, 1),
                eleve=False,
                arme_principale="épée",
                niveau="débutant",
                role="membre"
            )
            db.session.add(membre)
            db.session.commit()
            membre_id = membre.id_personne
        
        response = logged_responsable_client.post(f'/admin/supprimer/membre/{membre_id}')
        assert response.status_code == 302
    
    # ======================================== PAGES MEMBRES INACCESSIBLES ========================================
    
    def test_responsable_refuse_infos_persos_membre(self, logged_responsable_client):
        """Un responsable ne peut pas accéder aux infos persos d'un membre standard"""
        response = logged_responsable_client.get('/membre/information_personnel/')
        assert response.status_code == 302
    
    def test_responsable_refuse_event_inscrits_membre(self, logged_responsable_client):
        """Un responsable ne peut pas accéder aux événements inscrits membre"""
        response = logged_responsable_client.get('/membre/event_inscrits/')
        assert response.status_code == 302
