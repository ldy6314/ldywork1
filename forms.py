from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField,IntegerField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from models import User, Subject

grade_list = [i+'年级' for i in "一二三四五六"]
class_list = [str(i+1)+'班' for i in range(10)]


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8)])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登录')

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(username=username).first()
        if not user:
            raise ValidationError('账号不存在或密码错误!')

        if not user.validate_password(self.password.data):
            raise ValidationError('账号不存在或密码错误!')


class AddForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(8)])
    password = PasswordField('密码', validators=[DataRequired(), Length(8)])
    grd = SelectField('年级', choices=grade_list)
    cls = SelectField('班级', choices=class_list)
    name = StringField('姓名', validators=[DataRequired()])
    role = SelectField('角色', choices=['学生', '班主任', '管理员'])
    submit = SubmitField('登录')

    def validate_username(self, field):
        username = field.data
        print(username)
        res = User.query.filter_by(username=username).count()
        if res == 1:
            raise ValidationError('账户已经存在')


class AddSubjectForm(FlaskForm):
    name = StringField('名称', validators=[DataRequired(), Length(3)])
    time = SelectField('日期', choices=['星期六上午8：00-9：30',
                                      '星期六上午9：50-11：20',
                                      '星期日下午2：00-3：30',
                                      '星期日下午3：50-5：20',
                                      ])
    price = IntegerField('价格', validators=[DataRequired()])
    remark = TextAreaField('备注')
    submit = SubmitField('添加')

    def validate_name(form, field):
        name = field.data
        res = Subject.query.filter_by(name=name).count()
        if res:
            raise ValidationError('科目已经存在')


class UploadClassForm(FlaskForm):
    file = FileField('上传班级报名表', validators=[FileRequired(), FileAllowed(['xlsx'])])
    submit = SubmitField()