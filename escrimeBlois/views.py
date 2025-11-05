from flask import flash, redirect, render_template, request, url_for, flash
from .app import app,db
from .models import Article
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

