from app.appblueprint import app_bp
from app.forms import LoginForm
from flask import request, render_template


@app_bp.route('/')
def index():
    return "I am app index"


@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        return "POST is not ready"

    return render_template('login.html', form=form)
