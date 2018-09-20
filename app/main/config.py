import os
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'my_precious_secret_key')
    DB = 'mysql+pymysql://' + os.getenv('DB_USER_NAME')+':'+os.getenv(
        'DP_PASSWORD') + '@' + os.getenv('DB_ADDR') + ':'+os.getenv('DB_PORT') + '/'+os.getenv('DB_NAME')
    OAUTH_CREDENTIALS = {
        'facebook': {
            'id':  os.getenv('FACEBOOK_APP_ID'),
            'secret':  os.getenv('FACEBOOK_APP_SECRET')
        },
        'google': {
            'id':  os.getenv('GOOGLE_CLIENT_ID'),
            'secret':  os.getenv('GOOGLE_CLIENT_SECRET')
        }
    }
    REDIRECT_URI = os.getenv('REDIRECT_URI')
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = Config.DB
    OAUTH_CREDENTIALS = Config.OAUTH_CREDENTIALS
    REDIRECT_URI= Config.REDIRECT_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    OAUTH_CREDENTIALS = Config.OAUTH_CREDENTIALS
    SQLALCHEMY_DATABASE_URI = Config.DB
    REDIRECT_URI= Config.REDIRECT_URI
    PRESERVE_CONTEXT_ON_EXCEPTION = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)

key = Config.SECRET_KEY
