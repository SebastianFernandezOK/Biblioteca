from database.connection import db

class Autor(db.Model):
    __tablename__ = 'autores'

    autorID = db.Column(db.Integer, primary_key=True)
    autor_nombre = db.Column(db.String(100), nullable=False)
    autor_apellido = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Autor {self.autorID}: {self.autor_nombre} {self.autor_apellido}>"
