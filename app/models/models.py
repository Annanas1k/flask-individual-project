from app import db

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(20), nullable=False)
    prenume = db.Column(db.String(20), nullable=False)
    patronimic = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    specialitate = db.Column(db.String(80), nullable=False)
    grupa = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<Student {self.nume} {self.prenume}>'

class Profesor(db.Model):
    __tablename__ = 'profesori'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(20), nullable=False)
    prenume = db.Column(db.String(20), nullable=False)
    login = db.Column(db.String(20), nullable=False, unique=True)
    parola = db.Column(db.String(255), nullable=False)
    disciplina = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Profesor {self.nume} {self.prenume}>'

class Disciplina(db.Model):
    __tablename__ = 'discipline'
    id = db.Column(db.Integer, primary_key=True)
    nume_disciplina = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f'<Disciplina {self.nume_disciplina}>'


class Absenta(db.Model):
    __tablename__ = 'absente'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesori.id'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('discipline.id'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    motivat = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Absenta {self.student_id} {self.profesor_id}>'


