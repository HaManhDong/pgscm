from flask import render_template
from . import admin
from flask_security import roles_required


@admin.route('/')
@roles_required('admin')
def index():
    return render_template('admin/index.html')


@admin.route('/users')
@roles_required('admin')
def users():
    return render_template('admin/index.html')


@admin.route('/configs')
@roles_required('admin')
def configs():
    return render_template('admin/index.html')
