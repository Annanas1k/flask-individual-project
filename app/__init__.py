from datetime import timedelta

from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from werkzeug.security import generate_password_hash

load_dotenv()
db = SQLAlchemy()

def create_app():
    """
    Initializes and configures the Flask application.
    Registers routes and error handlers.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10)
    app.config['SESSION_PERMANENT'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Registering blueprints for admin, student, and profesor routes
    from .admin_routes import admin
    app.register_blueprint(admin)

    from .models.models import Students
    from .student_routes import student
    app.register_blueprint(student)

    from .models.models import Profesor
    from .profesor_routes import profesor
    app.register_blueprint(profesor)

    @app.errorhandler(404)
    def page_not_found(e):
        """
        Handles 404 errors and renders the custom 404 page.
        """
        return render_template("404.html"), 404

    @app.route('/cc')
    def cc():
        """
        Hashes all passwords for professors and updates them in the database.
        """
        profesori = Profesor.query.all()

        for profesor in profesori:
            if profesor.parola:
                # Hashing password using PBKDF2
                hashed_password = generate_password_hash(profesor.parola)

                # Updating password in the database
                profesor.parola = hashed_password
                db.session.commit()

        return jsonify({"message": "Passwords have been successfully hashed and updated!"}), 200

    return app
