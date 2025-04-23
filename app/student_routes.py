from flask import Blueprint, render_template, url_for, request, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from .models.models import Students
from sqlalchemy import text

from . import db
student = Blueprint('student', __name__)

@student.route('/', methods=['GET','POST'])
@student.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("email")

        if not email:
            return "Email este oblicatoriu", 400

        student = Students.query.filter_by(email=email).first()
        if student:
            return f"Salut {student.nume} {student.prenume}", 200
        else:
            return "Nu sa gasit asa email!", 404

    return render_template("student_login.html")


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
