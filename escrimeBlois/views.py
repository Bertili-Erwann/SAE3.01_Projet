from flask import redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash
from hashlib import sha256
from .app import app,db
from .models import *
from datetime import date
from escrimeBlois.models import Formulaire, Personne, Demande_inscription, Inscription, Evenement
from escrimeBlois.form import FormInscription
import os

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/inscription/', )
def inscription():
    form = FormInscription(request.form)
    return render_template('inscription.html', formInscription=form)


@app.route('/inscription/insert', methods=("POST", ))
def insert_inscription():
    form = FormInscription()
    if form.validate_on_submit():
        form.commit_inscription()

    return render_template('inscription.html', formInscription=form)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Personne.query.filter_by(email_personne=email).first()
        
        if user:
            m = sha256()
            m.update(password.encode('utf-8'))
            hashed_password = m.hexdigest()
            
            if user.mdp == hashed_password:
                login_user(user)
                flash('Connexion réussie !', 'success')
                if user.role == "membre":
                    return redirect(url_for('infos_persos'))
                elif user.role == "responsable":
                    return redirect(url_for('ajouter_article')) # Exemple de redirection pour responsable
                else:
                    return redirect(url_for('index'))
            else:
                flash('Mot de passe incorrect.', 'error')
        else:
            flash('Email inconnu.', 'error')
            
    return render_template("login.html")

@app.route('/logout/')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/mdp_oublier_envoyer_code/')
def mdp_oublier_envoyer_code():
    return render_template("mdp_oublier_envoyer_code.html")


@app.route('/mdp_oublier_code/')
def mdp_oublier_code():
    return render_template("mdp_oublier_code.html")


@app.route('/mdp_oublier_confirmer_mdp/', methods=['GET', 'POST'])
def mdp_oublier_confirmer_mdp():
    if request.method == 'POST':
        newpassword = request.form.get('newpassword')
        newpasswordconfirm = request.form.get('newpasswordconfirm')

        if newpassword != newpasswordconfirm:
            return render_template('mdp_oublier_confirmer_mdp.html')

        # Ici, tu peux ajouter la logique pour mettre à jour le mot de passe en base
        return redirect(url_for('login'))  # Ou une autre page

    return render_template('mdp_oublier_confirmer_mdp.html')

@app.route('/admin/miseajour/membres')
def admin_miseajour_membres():
        les_responsables = []
        les_membres = []
        personne = Personne.query.all()
        for e in personne:
                if e.role == "responsable":
                        les_responsables.append(e)
                elif e.role == "membre":
                        les_membres.append(e)
        return render_template('admin_miseajour_membres.html',  membres = les_membres, responsables = les_responsables)

@app.route('/admin/supprimer/membre/<int:id_personne>', methods=['POST'])
def supprimer_membre(id_personne):
        try:
                personne = Personne.query.get(id_personne)
                if personne:
                        db.session.delete(personne)
                        db.session.commit()
                        flash('Membre supprimé avec succès', 'success')
                else:
                        flash('Membre non trouvé', 'error')
        except Exception as e:
                db.session.rollback()
                flash('Erreur lors de la suppression', 'error')
        return redirect(url_for('admin_miseajour_membres'))

@app.route('/admin/gestion_inscription/club')
def admin_inscription_club():
    demandes = Demande_inscription.query.all()
    return render_template('admin_gestion_inscription_club.html', demandes=demandes)


@app.route('/admin/gestion_inscription/club/view/<int:id_inscription>', methods=['GET', 'POST'])
def admin_inscription_club_view(id_inscription):
    demande = Demande_inscription.query.get_or_404(id_inscription)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'accepter':
            # Créer un nouveau membre avec les infos de la demande
            nouveau_membre = Personne(
                mdp=demande.mot_de_passe,
                nom_personne=demande.nom,
                prenom_personne=demande.prenom,
                email_personne=demande.adresse_mail,
                telephone=demande.num_tel,
                sexe=demande.sexe,
                adresse=demande.adresse_postale,
                date_naissance=demande.date_naissance,
                eleve=demande.eleve,
                arme_principale='Non défini',
                niveau='Débutant',
                role='membre'
            )
            db.session.add(nouveau_membre)
            db.session.delete(demande)
            db.session.commit()
        
        elif action == 'refuser':
            # Supprimer la demande
            db.session.delete(demande)
            db.session.commit()
        
        return redirect(url_for('admin_inscription_club'))
    
    return render_template('admin_gestion_inscription_club_view.html', demande=demande)


@app.route('/admin/gestion_inscription/evenement')
def admin_inscription_evenement():
    # Récupérer toutes les inscriptions
    inscriptions = Inscription.query.all()
    return render_template('admin_gestion_inscription_evenement.html', inscriptions=inscriptions)


@app.route('/admin/gestion_inscription/evenement/view/<int:id_inscription>', methods=['GET', 'POST'])
def admin_inscription_evenement_view(id_inscription):
    inscription = Inscription.query.get_or_404(id_inscription)
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'accepter':
            # Valider l'inscription
            pass
        
        elif action == 'refuser':
            # Supprimer l'inscription
            db.session.delete(inscription)
            db.session.commit()
        
        return redirect(url_for('admin_inscription_evenement'))
    
    return render_template('admin_gestion_inscription_evenement_view.html', inscription=inscription)


@app.route('/historique/')
def historique():
    return render_template('historique.html')
  
@app.route('/renseignement/')
def renseignement():
    return render_template("renseignement.html",title = "renseignement")

@app.route('/nav_responsable/')
def nav_resp():
        return render_template('nav_responsable.html')

@app.route('/gestion_formulaire/')
def gest_form():
        lesFormulaires = Formulaire.query.all()
        return render_template('gestion_formulaire.html', formulaires = lesFormulaires)

@app.route('/create_event/')
def create_event():
        return render_template('resp_creation_event.html')

@app.route('/consultation_form/<id_formulaire>/')
def consult_form(id_formulaire):
        unForm = Formulaire.query.get(id_formulaire)
        return render_template('consultation_form.html', selectedFormulaire=unForm)

# Dossier de stockage des fichiers
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/ajouter_article', methods=['GET', 'POST'])
def ajouter_article():
    if request.method == 'POST':
        # Récupération des champs du formulaire
        titre = request.form.get('titre')
        description = request.form.get('description')
        theme = request.form.get('theme')  # correspond à "thème de l'article"
        commentable = True if request.form.get('commentable') == 'on' else False
        responsable_id = 1  # exemple : à remplacer par current_user.id si tu utilises Flask-Login
        fichiers = request.files.getlist('fichiers')

        # Création de l'article
        article = Article(
            titre=titre,
            description=description,
            categorie=theme,
            commentable=commentable,
            responsable_id=responsable_id,
            date_publication=date.today()
        )

        db.session.add(article)
        db.session.commit()

        # Sauvegarde des fichiers uploadés
        for fichier in fichiers:
            if fichier and fichier.filename != '':
                chemin_fichier = os.path.join(app.config['UPLOAD_FOLDER'], fichier.filename)
                fichier.save(chemin_fichier)

        flash("Article ajouté avec succès ✅", "success")
        return redirect(url_for('ajouter_article'))

    return render_template('ajout_article.html')

@app.route('/infos_persos/')
@login_required
def infos_persos():
    if current_user.role != 'membre':
        return redirect(url_for('index'))
    return render_template('infos_persos_espMembre.html', personne=current_user)

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not new_password or not confirm_password:
        flash('Les deux champs de mot de passe sont requis.', 'error')
        return redirect(url_for('infos_persos'))
        
    if new_password != confirm_password:
        flash('Les mots de passe ne correspondent pas.', 'error')
        return redirect(url_for('infos_persos'))
    
    # Vérification de la complexité du mot de passe
    if len(new_password) < 8:
        flash('Le mot de passe doit contenir au moins 8 caractères.', 'error')
        return redirect(url_for('infos_persos'))
    
    if not any(c.isalpha() for c in new_password) or not any(c.isdigit() for c in new_password):
        flash('Le mot de passe doit contenir au moins une lettre et un chiffre.', 'error')
        return redirect(url_for('infos_persos'))
    
    try:
        # Hasher le nouveau mot de passe
        m = sha256()
        m.update(new_password.encode('utf-8'))
        hashed_password = m.hexdigest()
        current_user.mdp = hashed_password
        db.session.commit()
        flash('Votre mot de passe a été mis à jour avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Une erreur est survenue lors de la mise à jour du mot de passe.', 'error')
        app.logger.error(f'Erreur lors du changement de mot de passe: {str(e)}')
    
    return redirect(url_for('infos_persos'))

@app.route('/update_arme', methods=['POST'])
@login_required
def update_arme():
    arme = request.form.get('arme_principale') 
    try:
        current_user.arme_principale = arme
        db.session.commit()
        flash('Votre arme principale a été mise à jour avec succès.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Une erreur est survenue lors de la mise à jour de l\'arme.', 'error')
        app.logger.error(f'Erreur lors de la mise à jour de l\'arme: {str(e)}')
    
    return redirect(url_for('infos_persos'))


