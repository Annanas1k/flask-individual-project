from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://radu.pavlovschi:dodik54@localhost:5432/radu_test'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    from .student_routes import student
    app.register_blueprint(student)


    return app


#
# @app.route('/test')
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
#

