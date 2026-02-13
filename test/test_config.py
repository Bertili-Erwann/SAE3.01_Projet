import pytest
import os
from escrimeBlois.config import Config, _env_bool


def test_config_database_uri_default():
    config = Config()
    assert 'sqlite:///' in config.SQLALCHEMY_DATABASE_URI
    assert 'escrimeBlois.db' in config.SQLALCHEMY_DATABASE_URI


def test_config_sqlalchemy_track_modifications():
    config = Config()
    assert config.SQLALCHEMY_TRACK_MODIFICATIONS == False


def test_config_secret_key_default():
    config = Config()
    assert config.SECRET_KEY is not None


def test_config_mail_server_default():
    config = Config()
    assert config.MAIL_SERVER == 'smtp.gmail.com'


def test_config_mail_port_default():
    config = Config()
    assert config.MAIL_PORT == 587


def test_config_mail_use_tls_default():
    config = Config()
    assert config.MAIL_USE_TLS == True


def test_config_mail_use_ssl_default():
    config = Config()
    assert config.MAIL_USE_SSL == False


def test_config_mail_default_sender():
    config = Config()
    assert isinstance(config.MAIL_DEFAULT_SENDER, tuple)
    assert len(config.MAIL_DEFAULT_SENDER) == 2


def test_env_bool_true_values():
    assert _env_bool('TEST', default=False) == False
    
    os.environ['TEST'] = '1'
    assert _env_bool('TEST') == True
    
    os.environ['TEST'] = 'true'
    assert _env_bool('TEST') == True
    
    os.environ['TEST'] = 'yes'
    assert _env_bool('TEST') == True
    
    os.environ['TEST'] = 'y'
    assert _env_bool('TEST') == True
    
    os.environ['TEST'] = 'on'
    assert _env_bool('TEST') == True
    
    del os.environ['TEST']


def test_env_bool_false_values():
    os.environ['TEST'] = '0'
    assert _env_bool('TEST') == False
    
    os.environ['TEST'] = 'false'
    assert _env_bool('TEST') == False
    
    os.environ['TEST'] = 'no'
    assert _env_bool('TEST') == False
    
    del os.environ['TEST']


def test_env_bool_default():
    assert _env_bool('INEXISTANT', default=True) == True
    assert _env_bool('INEXISTANT', default=False) == False


def test_config_with_env_vars():
    old_db = os.environ.get('DATABASE_URL')
    old_key = os.environ.get('SECRET_KEY')
    old_server = os.environ.get('MAIL_SERVER')
    old_port = os.environ.get('MAIL_PORT')
    
    os.environ['DATABASE_URL'] = 'sqlite:///test.db'
    os.environ['SECRET_KEY'] = 'test-secret'
    os.environ['MAIL_SERVER'] = 'smtp.test.com'
    os.environ['MAIL_PORT'] = '465'
    
    from importlib import reload
    from escrimeBlois import config as cfg_module
    reload(cfg_module)
    config = cfg_module.Config()
    
    assert config.SQLALCHEMY_DATABASE_URI == 'sqlite:///test.db'
    assert config.SECRET_KEY == 'test-secret'
    assert config.MAIL_SERVER == 'smtp.test.com'
    assert config.MAIL_PORT == 465
    
    if old_db:
        os.environ['DATABASE_URL'] = old_db
    else:
        del os.environ['DATABASE_URL']
    if old_key:
        os.environ['SECRET_KEY'] = old_key
    else:
        del os.environ['SECRET_KEY']
    if old_server:
        os.environ['MAIL_SERVER'] = old_server
    else:
        del os.environ['MAIL_SERVER']
    if old_port:
        os.environ['MAIL_PORT'] = old_port
    else:
        del os.environ['MAIL_PORT']


def test_config_mail_username_password():
    config = Config()
    assert config.MAIL_USERNAME is None or isinstance(config.MAIL_USERNAME, str)
    assert config.MAIL_PASSWORD is None or isinstance(config.MAIL_PASSWORD, str)


def test_config_basedir():
    config = Config()
    assert os.path.isabs(config.basedir)
