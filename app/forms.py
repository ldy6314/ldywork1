from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm


grade_list = [i+'年级' for i in "一二三四五六"]
class_list = [str(i+1)+'班' for i in range(10)]


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')


class AddForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8)])
    grd = SelectField('年级', choices=grade_list)
    cls = SelectField('班级', choices=class_list)
    status = SelectField('角色', choices=['学生', '班主任', '管理员'])
    submit = SubmitField('登录')