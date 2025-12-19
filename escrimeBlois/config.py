import os


class Config:
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'escrimeBlois.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = "b'O?\x02\xdf'"

    MAIL_SERVER = "partage.univ-orleans.fr"
    MAIL_PORT = 465
    SMTP_USER = "o22401211"
    MAIL_USERNAME = "magomed.arsamerzoev@etu.univ-orleans.fr"

    # Mail configuration
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_DEBUG = True
    MAIL_SUPRESS_SEND = False

    MAIL_PASSWORD = ""
    MAIL_DEFAULT_SENDER = ('Flask Mailer',
                           'magomed.arsamerzoev@etu.univ-orleans.fr')
    MAIL_MAX_EMAILS = 1000

    # MAIL_SUPPRESS_SEND = app.testing
    MAIL_ASCII_ATTACHEMENTS = False
