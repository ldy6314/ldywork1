from app.admin import admin_bp
from app.forms import AddForm
from flask import render_template


@admin_bp.route('/')
def index():
    return "I am admin index"


@admin_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        for i in form.data:
            print(i, form.data[i])

    return render_template('add.html', form=form)