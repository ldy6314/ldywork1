from flask import Blueprint, send_file, session, jsonify, flash, current_app, redirect, url_for
from forms import AddForm, AddSubjectForm, UploadClassForm, AddStudentForm, UploadSubjectsForm, EditSubjectForm,\
    UploadUserForm, EditStudentForm
from flask import render_template
from models import Subject, Student, User, Class
from extensions import db
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Side
from io import BytesIO
from flask_login import login_required
from utils import redirect_back, random_filename, get_subjects, get_time_list, parser_class_id,\
    get_students_information, to_class_id, get_users_information, get_class_info
import os
from openpyxl.worksheet.datavalidation import DataValidation
from urllib.parse import quote

admin_bp = Blueprint('admin', __name__)


@admin_bp.before_request
@login_required
def login_required():
    pass


@admin_bp.route('/')
def index():
    return "I am appblueprint index"


@admin_bp.route('/add', methods=['GET', 'POST'])
def add():
    form = AddForm()
    if form.validate_on_submit():
        for i in form.data:
            print(i, form.data[i])

    return render_template('adduser.html', form=form)


@admin_bp.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form1 = AddStudentForm()
    time_list = get_time_list()
    sublist = [form1.sub1, form1.sub2, form1.sub3, form1.sub4]
    for item in zip(sublist, time_list):
        item[0].label.text = item[1] + "课程"
        item[0].choices = [subject.name for subject in Subject.query.filter_by(time=item[1]).all()]
        item[0].choices.insert(0, "不选")
    form1 = AddStudentForm()
    time_list = get_time_list()
    sublist = [form1.sub1, form1.sub2, form1.sub3, form1.sub4]
    for item in zip(sublist, time_list):
        item[0].label.text = item[1] + "课程"
        item[0].choices = [subject.name for subject in Subject.query.filter_by(time=item[1]).all()]
        item[0].choices.insert(0, "不选")

    if form1.validate_on_submit():
        class_id = session['class_id']
        data = form1.data
        name = data['name']
        con1 = data['contact1']
        con2 = data['contact2']
        subs = [data['sub1'], data['sub2'], data['sub3'], data['sub4']]
        res = Student.query.filter_by(name=name, class_id=class_id).all()
        if not res:
            student = Student(name=name, class_id=class_id, contact1=con1, contact2=con2)
            
            for sub in subs:
                if sub != "不选":
                    sub = Subject.query.filter_by(name=sub).first()
                    if sub:
                        student.subjects.append(sub)
             
            if len(student.subjects):       
                db.session.add(student)
                db.session.commit()
                flash('添加成功')
            else:
                flash('至少选择一项科目')
        
        else:
            flash('该学生已经存在')

    return render_template("addstudent.html", form1=form1)


@admin_bp.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        subject = Subject(name=form.data['name'], time=form.data['time'], price=form.data['price'],
                          remark=form.data['remark'])

        db.session.add(subject)
        db.session.commit()
        res = Subject.query.all()
        for i in res:
            print(i.name)
        return jsonify({'result': "插入成功", "type": "alert alert-success"})
    else:
        return jsonify({'result': "项目已经存在无法添加", "type": "alert  alert-danger"})


@admin_bp.route('/download_subjects')
def download_subjects():
    wb = Workbook()
    ws = wb.worksheets[0]
    ws.append(["项目开设表", "", "", "", ""])
    ws.append(["编号", "名称", "时间", "价格", "备注"])
    res = Subject.query.all()
    for i in enumerate(res, 1):
        # print(i[0], i[1].name, i[1].time, i[1].price, i[1].remark)
        ws.append([i[0], i[1].name, i[1].time, i[1].price, i[1].remark])
    ws.merge_cells("A1:E1")
    border = Border(
        left=Side(style='medium', color='FF000000'),
        right=Side(style='medium', color='FF000000'),
        bottom=Side(style='medium', color='FF000000'),
        top=Side(style='medium', color='FF000000')
    )
    align_center = Alignment(horizontal='center', vertical='center')
    ws_area = ws["A1:E22"]
    for row in ws_area:
        for cell in row:
            cell.alignment = align_center
            cell.border = border
    for i in "BCE":
        ws.column_dimensions[i].width = 30

    virtual_book = BytesIO()
    wb.save(virtual_book)
    virtual_book.seek(0)
    rv = send_file(virtual_book, as_attachment=True, attachment_filename="test.xlsx")
    rv.headers['Content-Disposition'] += ";filename*=utf-8' 'test.xlsx"
    return rv


@admin_bp.route('/school_admin', methods=['GET', 'POST'])
def school_admin():
    permission = session['permission']
    if permission == 2:
        form = UploadSubjectsForm()
        subjects = Subject.query.all()
        form1 = AddSubjectForm()
        time_list = db.session.query(Subject.time).all()
        time_list = [time[0] for time in set(time_list)]
        form1.time.choices = time_list
        form2 = AddForm()
        users = User.query.all()
        subjects_info = []
        subject_list = Subject.query.all()
        for subject in subject_list:
            subjects_info.append((subject.name, len(subject.students)))
        class_list = Class.query.all()
        class_infos = []
        student_cnt = 0
        subject_cnt = 0
        tot_cost = 0
        for cls in class_list:
            info = get_class_info(cls.id)[1]
            clsname = parser_class_id(cls.id)
            clsname = clsname[0] + str(clsname[1]) + "班"
            class_infos.append((clsname, info[0][1], info[1][1], info[2][1]))
            student_cnt += info[0][1]
            subject_cnt += info[1][1]
            tot_cost += info[2][1]

        tot_info = "合计", student_cnt, subject_cnt, tot_cost
        class_infos.append(tot_info)
        return render_template('schooladmin.html', form=form, form1=form1, form2=form2, subjects=subjects, users=users,
                               subjects_info=subjects_info, class_infos=class_infos)
    else:
        return render_template("permission_deny.html")


@admin_bp.route('/class_admin')
def class_admin():
    form = UploadClassForm()
    permission = session['permission']
    class_id = session['class_id']
    if permission == 1:
        infos, tot_info = get_class_info(class_id)
        return render_template('classadmin.html', form=form, infos=infos, tot_info=tot_info)
    return render_template("permission_deny.html")


@admin_bp.route('/edit_subject/<int:subject_id>', methods=['GET', 'POST'])
def edit_subject(subject_id):
    time_list = get_time_list()
    form = EditSubjectForm()
    form.time.choices = time_list
    subject = Subject.query.get(subject_id)
    if form.validate_on_submit():
        subject.time = form.time.data
        subject.price = form.price.data
        subject.remark = form.remark.data
        subject.canceled = 1 if form.canceled.data else 0
        db.session.commit()
        flash("课程修改成功")
        return redirect(url_for('admin.school_admin'))

    name = subject.name
    tm = subject.time
    pr = subject.price
    rm = subject.remark
    cn = True if subject.canceled == 1 else False
    form.remark.data = rm
    form.price.data = pr
    form.time.choices = time_list
    form.time.data = tm
    form.canceled.data = cn
    return render_template('editsubject.html', form=form, subject_name=name)


@admin_bp.route('/delete/<int:subject_id>', methods=['GET', 'POST'])
def delete_subject(subject_id):
    subject = Subject.query.filter_by(id=subject_id).first()
    db.session.delete(subject)
    flash("已经删除 {}".format(subject.name))
    db.session.commit()
    return redirect_back('/')


@admin_bp.route('/upload_subjects', methods=['GET', 'POST'])
def upload_subjects():
    path = os.path.join(current_app.root_path, 'upload\\')
    print("path=", path)
    form = UploadSubjectsForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = random_filename(f.filename)
        f.save(path+filename)
        try:
            subjects = get_subjects(path+filename)
        except Exception as e:
            print(e)
            flash('上传的表格不正确')
            return redirect_back('/')
        infos = []
        for i in subjects:
            if not i[0]:
                break
            res = Subject.query.filter_by(name=i[0]).first()
            if not res:
                subject = Subject(name=i[0], time=i[1], price=i[2].strip('元'), canceled=0, remark="")
                infos.append(subject)
            else:
                flash('{}已经存在！'.format(i[0]))

        for i in infos:
            try:
                db.session.add(i)
                db.session.commit()
            except Exception as e:
                print(e)

    else:
        flash('上传失败')
    return redirect_back('/')


@admin_bp.route('/download_class_table')
def download_class_table():
    class_id = session['class_id']
    grd, cls = parser_class_id(class_id)
    # print(grd, cls)
    time_list = get_time_list()
    subject_list = []
    for time in time_list:
        subjects = db.session.query(Subject.name).filter_by(time=time).all()
        subjects = [i[0] for i in subjects]
        subject_list.append(','.join(subjects))
    wb = Workbook()
    ws = wb.worksheets[0]
    ws.append(["年级", "", "班级", ""])
    col_name = ["姓名", "联系电话1", "联系电话2"]
    tm_lst = [tm+'项目' for tm in time_list]
    col_name.extend(tm_lst)
    ws.append(col_name)
    dv = DataValidation(type="list", formula1='"一,二,三,四,五,六"', allow_blank=True)
    dv.error = "输入的值不在下拉列表中"
    dv.errorTitle = "错误"
    dv.prompt = "从下拉列表中选择年级"
    dv.promptTitle = "列表选择"
    dv.add('B1')
    ws.add_data_validation(dv)
    dv1 = DataValidation(type="list", formula1='"1,2,3,4,5,6,7,8"', allow_blank=True)
    dv1.error = "输入的值不在下拉列表中"
    dv1.errorTitle = "错误"
    dv1.prompt = "从下拉列表中选择班级"
    dv1.promptTitle = "列表选择"
    dv1.add('D1')
    ws.add_data_validation(dv1)
    ws['B1'].value = grd
    ws['D1'].value = cls
    for infos in zip(subject_list, ["D3:D50", "E3:E50", "F3:F50", "G3:G50"]):
        dv = DataValidation(type="list", formula1='"{}"'.format(infos[0]), allow_blank=True)
        dv.error = "输入的值不在下拉列表中"
        dv.errorTitle = "错误"
        dv.prompt = "请从下拉列表中选择课程"
        dv.promptTitle = "列表选择"
        dv.add(infos[1])
        ws.add_data_validation(dv)

    border = Border(
        left=Side(border_style='thin', color="FF000000"),
        right=Side(border_style='thin', color="FF000000"),
        bottom=Side(border_style='thin', color="FF000000"),
        top=Side(border_style='thin', color="FF000000")
    )
    align_center = Alignment(horizontal='center', vertical='center', wrapText=True)
    ws_area = ws["A1:G50"]
    for row in ws_area:
        for cell in row:
            cell.alignment = align_center
            cell.border = border
    for i in "BCDEFG":
        ws.column_dimensions[i].width = 18

    virtual_book = BytesIO()
    wb.save(virtual_book)
    virtual_book.seek(0)
    rv = send_file(virtual_book, as_attachment=True, attachment_filename="class_table.xlsx")
    rv.headers['Content-Disposition'] += ";filename*=utf-8' '{}{}{}.xlsx".format(quote(grd), cls, quote("班级俱乐部报名表"))
    return rv


@admin_bp.route("/upload_class_table", methods=['GET', 'POST'])
def upload_class_table():
    path = os.path.join(current_app.root_path, 'upload\\')
    # print("path=", path)
    form = UploadSubjectsForm()
    if form.validate_on_submit():
        f = form.file.data
        filename = f.filename
        f.save(path + filename)
        try:
            grd, cls, infos = get_students_information(path+filename)
            class_id = to_class_id(grd+str(cls))
            if class_id != session['class_id']:
                flash('班级填写不正确,请修改')
                return redirect_back('/')

            for i in infos:
                res = Student.query.filter_by(class_id=class_id, name=i[0]).all()
                if not res:
                    student = Student(class_id=class_id, name=i[0], contact1=i[1] if i[1] else "", contact2=i[2] if i[2]
                                      else "")

                    for sub in i[-4:]:
                        if sub:
                            sub = Subject.query.filter_by(name=sub).first()
                            if not sub:
                                flash('表格填写有错误')
                                return redirect_back('/')
                            student.subjects.append(sub)
                else:
                    flash("学生 {} 已经存在".format(i[0]))
                db.session.commit()
            flash("上传成功")
        except Exception as e:
            print(e)
            flash('上传的表格不正确')
            return redirect_back('/')

    else:
        flash('上传失败')
    return redirect_back('/')


@admin_bp.route('/upload_user_table', methods=['GET', 'POST'])
def upload_users_table():
    form = UploadUserForm()
    path = os.path.join(current_app.root_path, 'upload\\')

    if form.validate_on_submit():
        f = form.file.data
        filename = f.filename
        f.save(path + filename)
        try:
            infos = get_users_information(path + filename)
            for i in infos:
                res = User.query.filter_by(username=i[0]).all()
                if not res:
                    name = "{}{}班主任".format(i[2], i[3])
                    class_id = to_class_id(i[2]+str(i[3]))
                    print(name, class_id)
                    user = User(username=i[0], class_id=class_id, name=name, permission=i[4])
                    user.set_password(i[0])
                    db.session.add(user)
                    print(i[0], "添加成功")
                else:
                    flash("账号 {} 已经存在".format(i[0]))
                db.session.commit()
            flash("上传成功")
        except Exception as e:
            print(e)
            flash('上传的表格不正确')
            return redirect_back('/')

        else:
            flash('上传失败')
            return redirect_back('/')

    else:
        return render_template("upload_user_table.html", form=form)


@admin_bp.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    form1 = EditStudentForm()
    form1.submit.label.text = "修改"
    time_list = get_time_list()
    sublist = [form1.sub1, form1.sub2, form1.sub3, form1.sub4]
    for item in zip(sublist, time_list):
        item[0].label.text = item[1] + "课程"
        item[0].choices = [subject.name for subject in Subject.query.filter_by(time=item[1]).all()]
        item[0].choices.insert(0, "不选")
    student = Student.query.filter_by(id=student_id).first()
    if form1.validate_on_submit():
        data = form1.data
        con1 = data['contact1']
        con2 = data['contact2']
        subs = [data['sub1'], data['sub2'], data['sub3'], data['sub4']]
        num_of_subs = 4 - subs.count('不选')
        if not num_of_subs:
            db.session.delete(student)
            db.session.commit()
            flash('因修改该学生没有任何科目，删除该学生')
        else:
            student.contact1 = con1
            student.contact2 = con2
            student.subjects.clear()
            for sub in subs:
                if sub != "不选":
                    sub = Subject.query.filter_by(name=sub).first()
                    if sub:
                        student.subjects.append(sub)
            db.session.commit()
            flash('修改成功')

    name = student.name
    form1.contact1.data = student.contact1
    form1.contact2.data = student.contact2
    subjects = student.subjects
    for subject in subjects:
        idx = time_list.index(subject.time)
        sublist[idx].data = subject.name

    return render_template("editstudent.html", form=form1, name=name)