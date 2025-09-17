from models.estado_model import Estado
from database.connection import db

class EstadoRepository:
    @staticmethod
    def get_all():
        return Estado.query.all()

    @staticmethod
    def get_by_id(estadoID):
        return Estado.query.get(estadoID)

    @staticmethod
    def create(nombre, usuarioID=None):
        estado = Estado(nombre=nombre, usuarioID=usuarioID)
        db.session.add(estado)
        db.session.commit()
        return estado

    @staticmethod
    def update(estadoID, nombre, usuarioID=None):
        estado = Estado.query.get(estadoID)
        if estado:
            estado.nombre = nombre
            estado.usuarioID = usuarioID
            db.session.commit()
        return estado

    @staticmethod
    def delete(estadoID):
        estado = Estado.query.get(estadoID)
        if estado:
            db.session.delete(estado)
            db.session.commit()
            return True
        return False
