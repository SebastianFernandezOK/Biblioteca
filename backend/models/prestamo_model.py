from database.connection import db
from datetime import datetime
from models.estado_model import Estado

class Prestamo(db.Model):
    __tablename__ = 'prestamos'

    prestamoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuarioID = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'), nullable=False)
    libroID = db.Column(db.Integer, db.ForeignKey('libros.libroID'), nullable=False)
    fecha_entrega = db.Column(db.DateTime, nullable=False)
    fecha_devolucion = db.Column(db.DateTime, nullable=False)
    fecha_devuelta = db.Column(db.DateTime, nullable=True)
    estadoID = db.Column(db.Integer, db.ForeignKey('estados.estadoID'))
    estado = db.relationship('Estado', backref='prestamos')

    def __repr__(self):
        return f"<Prestamo {self.prestamoID}: Usuario {self.usuarioID} - Libro {self.libroID}>"
