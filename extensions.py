from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap4
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect


db = SQLAlchemy()
bootstrap = Bootstrap4()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()
