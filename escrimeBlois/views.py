from flask import flash, redirect, render_template, request, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from .app import app,db
from .models import *
from datetime import date
import os

@app.route('/')
@app.route('/index/')
def index():
        return render_template("index.html")

@app.route('/login/')
def login():
        return render_template("login.html")

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
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template('mdp_oublier_confirmer_mdp.html')
        
        # Ici, tu peux ajouter la logique pour mettre à jour le mot de passe en base
        flash("Mot de passe mis à jour avec succès.", "success")
        return redirect(url_for('login'))  # Ou une autre page
    
    return render_template('mdp_oublier_confirmer_mdp.html')

@app.route('/historique/')
def historique():
        return render_template('historique.html')


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
        hashed_password = generate_password_hash(new_password)
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


