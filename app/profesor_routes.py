from datetime import datetime
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
        if profesor and check_password_hash(profesor.parola, password):
            session['profesor_login'] = profesor.login
            session.permanent = True
            return redirect(url_for('profesor.dashboard', login=profesor.login), 301)
        else:
            flash("Login sau parola incorectă", "error")
            return redirect(url_for('profesor.login'))

    return render_template("profesor_login.html")




@profesor.route('/dashboard/profesor=<login>', methods=['GET', 'POST'])
def dashboard(login):
    if "profesor_login" not in session:
        flash("Sesiunea a expirat! Te rugăm să te loghezi din nou.", "error")
        return redirect(url_for('profesor.login'))

    profesor = Profesor.query.filter_by(login=session['profesor_login']).first()
    if not profesor:
        flash("Profesorul nu a fost găsit!", "error")
        return redirect(url_for('profesor.login'))

    disciplina = Disciplina.query.filter_by(nume_disciplina=profesor.disciplina).first()

    grupa_selectata = request.args.get('grupa')
    studenti = Students.query.filter_by(grupa=grupa_selectata).all() if grupa_selectata else []

    if request.method == 'POST':
        data_absenta = request.form['data_absenta']
        for student in studenti:
            absenta_key = f"absenta_{student.id}"
            motivata_key = f"motivata_{student.id}"
            absenta = request.form.get(absenta_key)
            motivata = request.form.get(motivata_key)

            if absenta:
                motivata_bool = True if motivata == "motivata" else False
                absenta_noua = Absenta(
                    student_id=student.id,
                    profesor_id=profesor.id,
                    disciplina_id=disciplina.id,
                    data=datetime.strptime(data_absenta, '%Y-%m-%d'),
                    motivat=motivata_bool
                )

                try:
                    db.session.add(absenta_noua)
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    flash(f"Eroare la salvarea absenței: {str(e)}", "error")

        flash("Absențele au fost salvate cu succes!", "success")
        return redirect(url_for('profesor.dashboard', login=login, grupa=grupa_selectata), 301)

    return render_template("profesor_dashboard.html",
                           profesor=profesor,
                           studenti=studenti,
                           disciplina=disciplina,
                           grupa_selectata=grupa_selectata)

@profesor.route('/logout/profesor')
def logout():
    session.pop('profesor_login', None)
    return redirect(url_for('profesor.login'))
