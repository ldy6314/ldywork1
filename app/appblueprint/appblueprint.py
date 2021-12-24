from flask import Blueprint, url_for, redirect, session, request, current_app
from forms import LoginForm, AddForm
from flask import flash, render_template
from models import User, Subject, Class
from extensions import db, login_manager
from flask_login import login_user, logout_user
from utils import is_safe_url, to_class_id

app_bp = Blueprint('rootbp', __name__)


@app_bp.before_app_first_request
def add_class_id():
    print('add_class_id')
    grade_list = current_app.config['GRADE_LIST']
    class_number = current_app.config['CLASS_NUMBER']
    res = Class.query.all()
    if not res:
        for i in range(len(grade_list)):
            for j in range(class_number[i]):
                class_name = grade_list[i] + str(j+1)
                class_id = to_class_id(class_name)
                class_ = Class(id=class_id)
                db.session.add(class_)

    user = User(username="admin", password_hash=0, class_id=0, permission=2, name="admin")
    user.set_password("ldy7842431")
    res = User.query.filter_by(username="admin").all()
    if not res:
        db.session.add(user)
        db.session.commit()
    else:
        print("admin has exist")


    db.session.commit()


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@app_bp.route('/')
def index():
    return render_template('base.html')


@app_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        remember_me = form.remember_me.data
        user = User.query.filter_by(username=username).first()
        class_id = user.class_id
        permission = user.permission
        login_user(user, remember_me)
        session["class_id"] = class_id
        session["permission"] = permission
        arg_next = request.args.get('next',  '/')
        if is_safe_url(arg_next):
            return redirect(arg_next)

    return render_template('login.html', form=form)


@app_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('rootbp.index'))


@app_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    res = User.query.first()
    if form.validate_on_submit():
        data = form.data
        username = data['username']
        password = data['password']
        class_id = 10 * "一二三四五六".index(data['grd'][0]) + int(data['cls'][:-1])
        permission = ['学生', '班主任', '管理员'].index(data['role'])
        name = data['name']
        user = User(username=username, password_hash=0, class_id=class_id, permission=permission, name=name)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('账户添加成功')

    return render_template("adduser.html", form=form)


@app_bp.route('/subject_info')
def show_subjects():
    infos = Subject.query.all()
    return render_template('showsubject.html', infos=infos)
