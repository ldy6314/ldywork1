from dotenv import find_dotenv, load_dotenv
import os

load_dotenv(find_dotenv(), override=True)


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "secret")
    DATABASE_URL_BASE = "mysql+pymysql://{}:{}@{}:{}/".format(
         os.getenv("USER"),
         os.getenv("PASSWORD"),
         os.getenv("HOST"),
        os.getenv("PORT")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "{}{}?charset=utf8".format(BaseConfig.DATABASE_URL_BASE, os.getenv('TEST_DATABASE', '1'))


class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "{}{}?charset=utf8".format(BaseConfig.DATABASE_URL_BASE, os.getenv('DATABASE', 'HAH'))


class TestConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLE = False
    SQLALCHEMY_DATABASE_URI = "{}{}?charset=utf8".format(BaseConfig.DATABASE_URL_BASE, os.getenv('TEST_DATABASE', '1'))


config = {
    'development': DevelopmentConfig,
    'testing': TestConfig,
    'production': ProductionConfig
}
