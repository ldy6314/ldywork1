from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired,Length
from flask_wtf import FlaskForm


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')
