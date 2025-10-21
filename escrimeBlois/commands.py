import click
import logging
from hashlib import sha256
from .models import Personne
from .app import app, db
from sqlalchemy import func
lg = logging.getLogger(__name__)


@app.cli.command()
def syncdb():
    """Crée les tables de la BD"""
    db.create_all()
    lg.warning('Base de donnée synchronisée!')


def maxutilisateur() -> int:
    """donne l'id de l'utilisateur le plus grand de la BD, 0 si il n'y en à pas
    """
    max_id = db.session.query(func.max(Personne.id_personne)).scalar()
    return (int(max_id)+1) if max_id is not None else 1


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

    lg.info('Utilisateur %s crée',prenom)


