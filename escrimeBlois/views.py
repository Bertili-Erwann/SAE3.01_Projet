from flask import flash, redirect, render_template, request, url_for
from .app import app, db
from escrimeBlois.models import Personne

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

@app.route('/historique/')
def historique():
        return render_template('historique.html')
