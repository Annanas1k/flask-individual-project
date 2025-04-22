from flask import Blueprint, render_template

student = Blueprint('student', __name__)

@student.route('/')
def login():
    return render_template("student_login.html")