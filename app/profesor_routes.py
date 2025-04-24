from flask import Blueprint, render_template, flash, redirect, url_for, request, session
from werkzeug.security import check_password_hash
from .models.models import *

profesor = Blueprint('profesor', __name__)


@profesor.route('/login/profesor', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        if not login or not password:
            flash("Datele sunt gresite sau incomplete!!", "error")
            return redirect(url_for('profesor.login'))

        profesor = Profesor.query.filter_by(login=login).first()
        if profesor:
            # print(f"Parola stocată în DB: {profesor.parola}")
            # print(f"Parola introdusă: {password}")

            if check_password_hash(profesor.parola, password):
                session['profesor_login'] = profesor.login
                session.permanent = True
                return redirect(url_for('profesor.dashboard', login=profesor.login), 301)
            else:
                flash("Parola este incorectă", "error")
                return redirect(url_for('profesor.login'))
        else:
            flash("Nu s-a găsit acest utilizator", "error")
            return redirect(url_for('profesor.login'))

    return render_template("profesor_login.html")

@profesor.route('/dashboard/profesor=<string:login>', methods=['GET', 'POST'])
def dashboard(login):
    if "profesor_login" not in session:
        return redirect(url_for('profesor.login'))

    profesor = Profesor.query.filter_by(login=login).first()

    if not profesor:
        return redirect(url_for('profesor.login'))

    return f"Salut {profesor.nume} {profesor.prenume} {profesor.parola}"
