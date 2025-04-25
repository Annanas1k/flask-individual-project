from collections import defaultdict
from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from sqlalchemy.orm import joinedload

from .models.models import *

student = Blueprint('student', __name__)

@student.before_request
def before_request():
    if "student_id" not in session and request.endpoint not in ['student.login']:
        flash("Sesiunea a expirat! Te rugăm să te loghezi din nou.", "error")
        return redirect(url_for('student.login'))
    return None


@student.route('/', methods=['GET','POST'])
@student.route('/login/student', methods=['GET','POST'])
def login():
    """
    Handles the student login process. If the email is found, a session is created and the student is redirected to the dashboard.
    If the email is not found, an error message is shown.
    """
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            flash("Email-ul este obligatoriu", "error")

        student = Students.query.filter_by(email=email).first()
        if student:
            session['student_id'] = student.id
            session.permanent = True
            #flash("succesfuly!", "success")
            return redirect(url_for("student.dashboard", id=student.id), 301)
        else:
            flash("Stundentul nu a fost gasit", "error")
            return redirect(url_for("student.login"), 301)

    return render_template("student_login.html")


@student.route('/dashboard/student_id=<int:id>', methods=['GET','POST'])
def dashboard(id):
    """
    Displays the student dashboard with their absences grouped by subject.
    If the student is not found or the session has expired, they are redirected to the login page.
    """

    student = Students.query.get(session['student_id'])

    if not student:
        flash("Studentul nu a fost găsit!", "error")
        return redirect(url_for('student.login'))

    absente = (
        Absenta.query
        .options(joinedload(Absenta.disciplina))
        .filter_by(student_id=student.id)
        .order_by(Absenta.data.desc())
        .all()
    )

    total_absente = len(absente)

    absente_pe_disciplina = defaultdict(list)
    for absenta in absente:
        absente_pe_disciplina[absenta.disciplina.nume_disciplina].append(absenta)

    return render_template(
        "student_dashboard.html",
        student=student,
        absente_pe_disciplina=absente_pe_disciplina,
        total_absente=total_absente
    )

@student.route('/logout/student')
def logout():
    """
    Logs out the student by clearing the session.
    """
    session.pop('student_id', None)
    return redirect(url_for('student.login'))
