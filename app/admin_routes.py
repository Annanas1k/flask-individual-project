from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from .models.models import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session

load_dotenv()

admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates')

ADMIN_LOGIN = os.getenv('ADMIN_LOGIN')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')


@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if not login or not password:
            flash("Datele sunt gresite sau incorecte!!", "error")
            return redirect(url_for('admin.login'))

        if login == ADMIN_LOGIN and check_password_hash(ADMIN_PASSWORD, password):
            session['admin'] = True
            return redirect(url_for('admin.dashboard'))
        else:
            flash("Datele sunt gresite!!", "error")


    return render_template("admin/login.html")

@admin.route('/', methods=['GET', 'POST'])
@admin.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if "admin" not in session:
        flash("Sesiunea a expirat! Te rugam sa te loghezi din nou", "error")
        return redirect(url_for('admin.login'))


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




@admin.route('/hashpass', methods=['GET', 'POST'])
def hashpass():
    parola = "admin"
    hash_parola = generate_password_hash(parola)
    return jsonify({"message": "Parolele au fost hashate și actualizate cu succes!",
                    "hashed_password:": hash_parola}), 200

