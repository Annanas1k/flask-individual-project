from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

import psycopg2

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://radu.pavlovschi:dodik54@localhost:5432/radu_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Dezactivează modificările de urmărire
db = SQLAlchemy(app)

from models import *

@app.route('/test')
def test_db_connection():
    try:
        result = db.session.execute(text('SELECT * FROM students'))

        return f'Rezultatul interogării este: {result.scalar()}'
    except Exception as e:
        return f'Eroare la conectarea la baza de date: {str(e)}'


@app.route('/')
def login():
    return render_template('student_login.html')


if __name__ == '__main__':
    app.run(debug=True)

