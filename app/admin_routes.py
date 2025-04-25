from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from .models.models import *
from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash, session
from sqlalchemy import func
import matplotlib.pyplot as plt
import io
import base64
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
    if "admin" not in session:
        flash("Sesiunea a expirat! Te rugam sa te loghezi din nou", "error")
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        if "add_student" in request.form:
            nume = request.form['nume']
            prenume = request.form['prenume']
            patronimic = request.form['patronimic']
            email = request.form['email']
            specialitate = request.form['specialitate']
            grupa = request.form['grupa']

            existing_student = Students.query.filter_by(email=email).first()
            if existing_student:
                flash("Student cu asa email deja exista!", "error")
                return redirect(url_for('admin.students'))
            else:
                new_student = Students(nume=nume,
                                       prenume=prenume,
                                       patronimic=patronimic,
                                       email=email,
                                       specialitate=specialitate,
                                       grupa=grupa)
                db.session.add(new_student)
                db.session.commit()
                flash('Studentul a fost adaugat cu succes!', 'success')
                return redirect(url_for('admin.students'))


        elif "edit_student" in request.form:
            student_id = request.form['student_id']
            student = Students.query.get_or_404(student_id)
            student.nume = request.form['nume']
            student.prenume = request.form['prenume']
            student.patronimic = request.form['patronimic']
            student.email = request.form['email']
            student.specialitate = request.form['specialitate']
            student.grupa = request.form['grupa']

            db.session.commit()

            flash('Studentul a fost actualizat cu succes!', 'success')
            return redirect(url_for('admin.students'))

        elif "delete_student" in request.form:
            student_id = request.form['student_id']
            student = Students.query.get_or_404(student_id)
            db.session.delete(student)
            db.session.commit()

            flash('Studentul a fost sters cu succes!', 'danger')
            return redirect(url_for('admin.students'))







    students = Students.query.all()
    return render_template("admin/students.html", students=students)

@admin.route('/profesori', methods=['GET', 'POST'])
def profesori():
    if "admin" not in session:
        flash("Sesiunea a expirat! Te rugam sa te loghezi din nou", "error")
        return redirect(url_for('admin.login'))

    if request.method == 'POST':
        if "add_profesor" in request.form:
            nume = request.form['nume']
            prenume = request.form['prenume']
            login = request.form['login']
            parola = request.form['parola']
            parola_hashata = generate_password_hash(parola)
            disciplina = request.form['disciplina']

            # Verificăm dacă există deja un profesor cu același login
            existing_profesor = Profesor.query.filter_by(login=login).first()
            if existing_profesor:
                flash("Profesor cu acest login deja există!", "error")
                return redirect(url_for('admin.profesori'))
            else:
                new_profesor = Profesor(nume=nume,
                                        prenume=prenume,
                                        login=login,
                                        parola=parola_hashata,
                                        disciplina=disciplina)
                db.session.add(new_profesor)
                db.session.commit()
                flash('Profesorul a fost adăugat cu succes!', 'success')
                return redirect(url_for('admin.profesori'))

        elif "edit_profesor" in request.form:
            profesor_id = request.form['profesor_id']
            profesor = Profesor.query.get_or_404(profesor_id)
            profesor.nume = request.form['nume']
            profesor.prenume = request.form['prenume']
            profesor.login = request.form['login']
            profesor.disciplina = request.form['disciplina']

            parola = request.form.get('parola')
            if parola:
                profesor.parola_hashata = generate_password_hash(parola)

            db.session.commit()
            flash('Profesorul a fost actualizat cu succes!', 'success')
            return redirect(url_for('admin.profesori'))

        elif "delete_profesor" in request.form:
            profesor_id = request.form['profesor_id']
            profesor = Profesor.query.get_or_404(profesor_id)

            db.session.delete(profesor)
            db.session.commit()
            flash('Profesorul a fost șters cu succes!', 'danger')
            return redirect(url_for('admin.profesori'))

    profesori = Profesor.query.all()
    return render_template("admin/profesori.html", profesori=profesori)

@admin.route('/discipline', methods=['GET', 'POST'])
def discipline():
    return render_template("admin/discipline.html")

@admin.route('/absente', methods=['GET', 'POST'])
def absente():
    # Creăm un grafic cu statistici pe discipline
    absente_pe_disciplina = db.session.query(
        Disciplina.nume_disciplina.label('disciplina_nume'),
        func.count(Absenta.id).label('total')
    ).join(Absenta).group_by(Disciplina.nume_disciplina).all()

    discipline = [absenta.disciplina_nume for absenta in absente_pe_disciplina]
    total_abente = [absenta.total for absenta in absente_pe_disciplina]

    # Generare grafic
    fig, ax = plt.subplots()
    ax.bar(discipline, total_abente)
    ax.set_xlabel('Discipline')
    ax.set_ylabel('Număr Absențe')
    ax.set_title('Statistici Absențe pe Discipline')

    # Salvăm graficul într-un obiect BytesIO pentru a-l trimite în base64
    img = io.BytesIO()
    fig.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return render_template('admin/absente.html', img_data=img_base64)

@admin.route('/logout')
def logout():
    session.pop("admin", None)
    return redirect(url_for('admin.login'))

@admin.route('/hashpass', methods=['GET', 'POST'])
def hashpass():
    parola = "admin"
    hash_parola = generate_password_hash(parola)
    return jsonify({"message": "Parolele au fost hashate și actualizate cu succes!",
                    "hashed_password:": hash_parola}), 200

