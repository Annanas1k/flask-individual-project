import time
from time import sleep

from flask import Blueprint, render_template, url_for, request, redirect, session, flash
from .models.models import *

student = Blueprint('student', __name__)

@student.route('/', methods=['GET','POST'])
@student.route('/login/student', methods=['GET','POST'])
def login():
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
    if 'student_id' not in session:
        return redirect(url_for('student.login'))

    student = Students.query.get(session['student_id'])

    if not student:
        return f"Nu sa gasit asa student", 404

    return render_template("student_dashboard.html", student=student)



@student.route('/logout/student')
def logout():
    session.pop('student_id', None)
    return redirect(url_for('student.login'))





#
# @student.route('/test')
# def test_db_connection():
#     try:
#         result = db.session.execute(text('SELECT * FROM students'))
#
#         rows = result.fetchall()
#         output = ""
#         for row in rows:
#             output += f"\n|{str(row.nume)} - {row.prenume}|"
#         return output
#     except Exception as e:
#         return f'Eroare la conectarea la baza de date: {str(e)}'
#
