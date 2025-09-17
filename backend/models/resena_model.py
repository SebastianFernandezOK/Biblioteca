from database.connection import db

class Resena(db.Model):
    __tablename__ = 'resenas'

    resenaID = db.Column(db.Integer, primary_key=True)
    valoracion = db.Column(db.Integer)
    comentario = db.Column(db.String(100))
    usuarioID = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'), nullable=False)
    libroID = db.Column(db.Integer, db.ForeignKey('libros.libroID'), nullable=False)

    def __repr__(self):
        return f"<Resena {self.resenaID}: Usuario {self.usuarioID} - Libro {self.libroID}>"
