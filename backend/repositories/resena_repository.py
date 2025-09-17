from database.connection import db
from models.resena_model import Resena

class ResenaRepository:
    @staticmethod
    def get_all():
        return Resena.query.all()

    @staticmethod
    def get_by_id(resena_id):
        return Resena.query.get(resena_id)

    @staticmethod
    def create(data):
        resena = Resena(**data)
        db.session.add(resena)
        db.session.commit()
        return resena

    @staticmethod
    def update(resena_id, data):
        resena = Resena.query.get(resena_id)
        if not resena:
            return None
        for key, value in data.items():
            setattr(resena, key, value)
        db.session.commit()
        return resena

    @staticmethod
    def delete(resena_id):
        resena = Resena.query.get(resena_id)
        if not resena:
            return False
        db.session.delete(resena)
        db.session.commit()
        return True

    @staticmethod
    def get_by_libro(libro_id):
        return Resena.query.filter_by(libroID=libro_id).all()