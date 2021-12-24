from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, IntegerField, TextAreaField,\
    HiddenField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, ValidationError
from flask_wtf import FlaskForm
from models import User, Subject

grade_list = [i + '年级' for i in "一二三四五六"]
class_list = [str(i + 1) + '班' for i in range(10)]


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(), Length(3)])
    password = PasswordField('密码', validators=[DataRequired(), Length(3)])
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
    time = SelectField('时间')
    price = IntegerField('价格', validators=[DataRequired()])
    remark = TextAreaField('备注')
    submit = SubmitField('添加', render_kw={"id": "add_subject_button"})

    def validate_name(form, field):
        name = field.data
        res = Subject.query.filter_by(name=name).count()
        if res:
            raise ValidationError('科目已经存在')


class UploadClassForm(FlaskForm):
    file = FileField('上传班级报名表', validators=[FileRequired(), FileAllowed(['xlsx'])])
    submit = SubmitField('上传', render_kw={"id": "submit"})


class UploadSubjectsForm(FlaskForm):
    file = FileField('上传课程信息表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'])])
    submit = SubmitField('上传', render_kw={"id": "submit"})


class AddStudentForm(FlaskForm):
    name = StringField('姓名', validators=[DataRequired()])
    contact1 = StringField('联系电话1', validators=[DataRequired()])
    contact2 = StringField('联系电话2')
    sub1 = SelectField('项目一', choices=["", 1, 2, 3, 4, 5, 6, 7])
    sub2 = SelectField('项目二', choices=["", 1, 2, 3, 4, 5, 6, 7])
    sub3 = SelectField('项目三', choices=["", 1, 2, 3, 4, 5, 6, 7])
    sub4 = SelectField('项目四', choices=["", 1, 2, 3, 4, 5, 6, 7])
    add_submit = SubmitField('添加')


class EditSubjectForm(AddSubjectForm):
    name = HiddenField()
    canceled = BooleanField('取消')
    submit = SubmitField('修改', render_kw={'class': "btn-block"})


class UploadUserForm(FlaskForm):
    file = FileField('请上传账户添加表', validators=[FileRequired(), FileAllowed(['xls', 'xlsx'])])
    submit = SubmitField('上传', render_kw={"id": "submit"})