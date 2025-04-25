from app import db

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    patronimic = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    specialitate = db.Column(db.String(100), nullable=False)
    grupa = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Students %r>' % self.id


class Profesor(db.Model):
    __tablename__ = 'profesori'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(50), nullable=False)
    prenume = db.Column(db.String(50), nullable=False)
    login = db.Column(db.String(100), unique=True, nullable=False)
    parola = db.Column(db.String(200), nullable=False)
    disciplina = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Profesor %r>' % self.id




class Disciplina(db.Model):
    __tablename__ = 'discipline'
    id = db.Column(db.Integer, primary_key=True)
    nume_disciplina = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return '<Disciplina %r>' % self.id

class Absenta(db.Model):
    __tablename__ = 'absente'
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False)
    profesor_id = db.Column(db.Integer, db.ForeignKey('profesori.id', ondelete='CASCADE'), nullable=False)
    disciplina_id = db.Column(db.Integer, db.ForeignKey('discipline.id', ondelete='CASCADE'), nullable=False)
    data = db.Column(db.Date, nullable=False)
    motivat = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Absenta %r>' % self.id

    # Relații cu backref
    student = db.relationship('Students', backref=db.backref('absente', cascade='all, delete-orphan'))
    profesor = db.relationship('Profesor', backref=db.backref('absente', cascade='all, delete-orphan'))
    disciplina = db.relationship('Disciplina', backref=db.backref('absente', cascade='all, delete-orphan'))
