from datetime import timedelta

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from werkzeug.security import generate_password_hash

load_dotenv()
db = SQLAlchemy()



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['SESSION_PERMANENT'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models.models import Students
    from .student_routes import student
    app.register_blueprint(student)

    from .models.models import Profesor
    from .profesor_routes import profesor
    app.register_blueprint(profesor)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template("404.html"), 404


    @app.route('/cc')
    def cc():
        profesori = Profesor.query.all()

        for profesor in profesori:
            if profesor.parola:
                # Hash-uiește parola folosind generate_password_hash (care folosește PBKDF2 cu salt)
                hashed_password = generate_password_hash(profesor.parola)

                # Actualizează parola în baza de date cu hash-ul generat
                profesor.parola = hashed_password
                db.session.commit()

        return jsonify({"message": "Parolele au fost hashate și actualizate cu succes!"}), 200


    return app




