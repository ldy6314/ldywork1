from flask import Blueprint

app_bp = Blueprint('rootbp', __name__)

from app.views import *
