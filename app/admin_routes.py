from .models.models import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

@admin.route('/login', methods=['GET', 'POST'])
def login():
    return render_template("admin/login.html")

@admin.route('/', methods=['GET', 'POST'])
@admin.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    return render_template("admin/dashboard.html")

@admin.route('/students', methods=['GET', 'POST'])
def students():
    return render_template("admin/students.html")

@admin.route('/profesori', methods=['GET', 'POST'])
def profesori():
    return render_template("admin/profesori.html")

@admin.route('/discipline', methods=['GET', 'POST'])
def discipline():
    return render_template("admin/discipline.html")

@admin.route('/absente', methods=['GET', 'POST'])
def absente():
    return render_template("admin/absente.html")

@admin.route('/logout')
def logout():
    return redirect(url_for('admin.login'))