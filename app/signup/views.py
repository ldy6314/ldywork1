from app.signup import signup_bp


@signup_bp.route('/')
def index():
    return "I am signup index"
