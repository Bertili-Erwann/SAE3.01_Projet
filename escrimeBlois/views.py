from flask import redirect, render_template, request, url_for
from .app import app, db
from escrimeBlois.models import Personne, Demande_inscription, Inscription, Evenement


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
