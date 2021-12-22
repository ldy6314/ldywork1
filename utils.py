from urllib.parse import urlparse, urljoin
from flask import request, redirect, url_for
from uuid import uuid4
import os
from openpyxl import load_workbook


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
    for row in ws.iter_rows(min_row=2, max_row=maxr, max_col=maxc-1):
        subject = []
        for cell in row:
            subject.append(cell.value)
        subjects.append(subject)
    return subjects
