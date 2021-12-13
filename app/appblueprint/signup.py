from flask import Blueprint

signup_bp = Blueprint('signup', __name__)


@signup_bp.route('/')
def index():
    return "I am signup index"



