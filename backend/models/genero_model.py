from database.connection import db

class Genero(db.Model):
    __tablename__ = 'generos'
    generosID = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Genero {self.nombre}>'
