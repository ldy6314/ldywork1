from flask import Flask
from app.admin import admin_bp
from app.signup import signup_bp
from app.settings import config
import os
from app.extensions import bootstrap, db
# login_manager
from app.appblueprint import app_bp


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask("app")
    app.config.from_object(config[config_name])
    bootstrap.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)

    app.register_blueprint(app_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(signup_bp, url_prefix='/signup')
    return app


if __name__ == '__main__':
    app1 = create_app()
    app1.run()
