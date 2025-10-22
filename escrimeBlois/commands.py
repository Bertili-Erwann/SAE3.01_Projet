import click
import logging
from hashlib import sha256
from .models import Personne
from .app import app, db
from sqlalchemy import func
import datetime

lg = logging.getLogger(__name__)


@app.cli.command()
@click.argument('filename')
def loaddb(filename):
    """Creates the tables and populates them with data."""
    # recréer la base
    db.drop_all()
    db.create_all()

    import yaml
    from .models import Personne, Evenement, Classer, Formulaire, Repondre, Article, Inscription

    with open(filename, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file) or []

    for pers in data["personnes"]:
        date_naissance = None
        if pers.get('date_naissance'):
            date_naissance = datetime.date.fromisoformat(
                pers['date_naissance'])
        personne = Personne(id_personne=pers['id_personne'],
                            mdp=pers['mdp'],
                            nom_personne=pers['nom_personne'],
                            prenom_personne=pers['prenom_personne'],
                            email_personne=pers['email_personne'],
                            sexe=pers.get('sexe'),
                            adresse=pers.get('adresse'),
                            date_naissance=date_naissance,
                            etudiant=pers.get('etudiant'),
                            arme_principale=pers.get('arme_principale'),
                            niveau=pers.get('niveau'),
                            role=pers['role'])
        db.session.add(personne)
        db.session.commit()

    for ev in data["evenements"]:
        date_evenement = datetime.date.fromisoformat(ev['date'])
        evenement = Evenement(id_evenement=ev['id_evenement'],
                              date=date_evenement,
                              heure=ev['heure'],
                              categorie=ev.get('categorie'),
                              lieu=ev['lieu'],
                              description=ev['description'],
                              niveau=ev.get('niveau'),
                              discipline=ev.get('discipline'),
                              cooperative=ev.get('cooperative'),
                              type_evenement=ev['type_evenement'])
        db.session.add(evenement)
        db.session.commit()

    for insc in data.get("inscriptions", []):
        inscription = Inscription(id_inscription=insc['id_inscription'],
                                  id_evenement=insc['id_evenement'])
        db.session.add(inscription)
        db.session.commit()

    for clas in data["classers"]:
        classer = Classer(id_competition=clas['id_competition'],
                          id_inscription=clas['id_inscription'],
                          point=clas.get('point'))
        db.session.add(classer)
        db.session.commit()

    for form in data["formulaires"]:
        formul = Formulaire(id_formulaire=form['id_formulaire'],
                            nom_auteur=form['nom_auteur'],
                            prenom_auteur=form['prenom_auteur'],
                            email_auteur=form['email_auteur'],
                            objet=form['objet'],
                            message=form['message'])
        db.session.add(formul)
        db.session.commit()

    for rep in data['repondre']:
        reponse = Repondre(id_responsable=rep['id_responsable'],
                           id_formulaire=rep['id_formulaire'])
        db.session.add(reponse)
        db.session.commit()

    for art in data['articles']:
        date_publication = datetime.date.fromisoformat(art['date_publication'])
        article = Article(id_article=art['id_article'],
                          titre=art['titre'],
                          date_publication=date_publication,
                          description=art['description'],
                          categorie=art['categorie'],
                          commentable=art['commentable'],
                          responsable_id=art['responsable_id'])
        db.session.add(article)
        db.session.commit()


@app.cli.command()
def syncdb():
    """Crée les tables de la BD"""
    db.create_all()
    lg.warning('Base de donnée synchronisée!')


def maxutilisateur() -> int:
    """donne l'id de l'utilisateur le plus grand de la BD, 0 si il n'y en à pas
    """
    max_id = db.session.query(func.max(Personne.id_personne)).scalar()
    return (int(max_id) + 1) if max_id is not None else 1


@app.cli.command()
@click.argument('nom')
@click.argument('prenom')
@click.argument('role_user')
@click.argument('pwd')
@click.argument('mail')
def nouvpers(nom, prenom, role_user, pwd, mail):
    """Ajoute un nouveau membre dans la base de donnée 
    """

    if Personne.query.filter_by(email_personne=mail).first():
        lg.warning('User %s existe déjà', mail)
        return
    m = sha256()
    m.update(pwd.encode('utf-8'))

    pers = Personne(id_personne=maxutilisateur(),
                    mdp=m.hexdigest(),
                    role=role_user,
                    nom_personne=nom,
                    prenom_personne=prenom,
                    email_personne=mail)

    db.session.add(pers)
    db.session.commit()

    lg.info('Utilisateur %s crée', prenom)
