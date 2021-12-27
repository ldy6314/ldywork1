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
    GRADE_LIST = "一二三四五六"
    CLASS_NUMBER = [8, 7, 6, 5, 4, 4]
    CLASS_OF_GRADE = 10
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
