from app.admin import admin_bp


@admin_bp.route('/')
def index():
    return "I am admin index"
