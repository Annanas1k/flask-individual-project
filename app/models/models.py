from app import db

class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    nume = db.Column(db.String(20), nullable=False)
    prenume = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    specialitate = db.Column(db.String(80), nullable=False)
    grupa = db.Column(db.String(10), nullable=False)
    nr_absentes = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Student {self.nume} {self.prenume}>'