from database.connection import db

class Libro(db.Model):
    __tablename__ = 'libros'

    libroID = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    editorial = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String, nullable=False)
    generoID = db.Column(db.String(20), db.ForeignKey('generos.generosID'))
    genero = db.relationship('Genero', backref='libros')
    autor = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Libro {self.libroID}: {self.titulo}>"
