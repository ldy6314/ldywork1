from app.appblueprint import app_bp
from app.forms import LoginForm, AddForm
from flask import request, render_template
from models import User

@app_bp.route('/')
def index():
    return "I am app index"


@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        return "POST is not ready"

    return render_template('login.html', form=form)


@app_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        for i in form.data:
            print(i, form.data[i])

    return render_template('add.html', form=form)