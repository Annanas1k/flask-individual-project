from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
    app.config['SESSION_PERMANENT'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models.models import Students
    from .student_routes import student
    app.register_blueprint(student)


    return app




