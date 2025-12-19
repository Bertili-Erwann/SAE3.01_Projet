import os

class Config:
    # Database configuration
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'escrimeBlois.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Secret key
    SECRET_KEY = "b'O?\x02\xdf'"

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'm4go83@gmail.com'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    MAIL_DEBUG = True
    MAIL_SUPRESS_SEND = False

    MAIL_PASSWORD = "djab0603"
    MAIL_DEFAULT_SENDER = ('Flask Mailer', 'm4go83@gmail.com')
    MAIL_MAX_EMAILS = 1000
    # MAIL_SUPPRESS_SEND = app.testing
    MAIL_ASCII_ATTACHEMENTS = False
