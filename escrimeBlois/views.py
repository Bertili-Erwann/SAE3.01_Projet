from flask import redirect, render_template, request, url_for, flash
from .app import app,db
from .models import Article
from datetime import date
from escrimeBlois.models import Formulaire, Personne, Demande_inscription, Inscription, Evenement
from escrimeBlois.form import FormInscription
import os

@app.route('/')
@app.route('/index/')
def index():
    return render_template("index.html")

@app.route('/historique/')
def historique():
    return render_template('historique.html')


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
            return render_template('mdp_oublier_confirmer_mdp.html')

        # Ici, tu peux ajouter la logique pour mettre à jour le mot de passe en base
        return redirect(url_for('login'))  # Ou une autre page

    return render_template('mdp_oublier_confirmer_mdp.html')


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

