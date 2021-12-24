from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for, current_app
from uuid import uuid4
import os
from openpyxl import load_workbook
from extensions import db
from models import Subject

# 函数功能，传入当前url 跳转回当前url的前一个url
def redirect_back(backurl, **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(backurl, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def random_filename(filename):
    ext = os.path.splitext(filename)[1]
    new_filename = uuid4().hex + ext
    return new_filename


def get_subjects(filename):
    wb = load_workbook(filename)
    ws = wb.active
    minr = ws.min_row
    minc = ws.min_column
    maxr = ws.max_row
    maxc = ws.max_column

    subjects = []
    for row in ws.iter_rows(min_row=2, max_row=maxr, max_col=maxc):
        subject = []
        for cell in row:
            subject.append(cell.value)
        subjects.append(subject)
    return subjects


def to_class_id(class_string):
    grd = class_string[0]
    cls = class_string[1]
    grade_list = current_app.config['GRADE_LIST']
    class_of_grade = current_app.config['CLASS_OF_GRADE']
    try:
        grd_idx = grade_list.index(grd)
        cls_idx = int(cls)
    except IndexError:
        return -1
    return grd_idx*class_of_grade + cls_idx


def parser_class_id(class_id):
    grade_list = current_app.config['GRADE_LIST']
    class_of_grade = current_app.config['CLASS_OF_GRADE']
    grd = grade_list[class_id // class_of_grade]
    cls = class_id % class_of_grade
    return grd, cls


def get_time_list():
    time_list = db.session.query(Subject.time).all()
    time_list = [time[0] for time in set(time_list)]
    return time_list


def get_students_information(filename):
    print(filename)
    wb = load_workbook(filename)
    ws = wb.active
    grd = ws['B1'].value
    cls = ws['D1'].value
    infos = []
    for row in ws.iter_rows(min_row=3, max_row=50, max_col=7):
        info = []
        for cell in row:
            info.append(cell.value)
        if info[0]:
            infos.append(info)
    return grd, cls, infos
