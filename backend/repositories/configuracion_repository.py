from database.connection import db
from models.configuracion_model import Configuracion

class ConfiguracionRepository:
    @staticmethod
    def get_all():
        return Configuracion.query.all()

    @staticmethod
    def get_by_id(configuracion_id):
        return Configuracion.query.get(configuracion_id)

    @staticmethod
    def create(data):
        configuracion = Configuracion(**data)
        db.session.add(configuracion)
        db.session.commit()
        return configuracion

    @staticmethod
    def update(configuracion_id, data):
        configuracion = Configuracion.query.get(configuracion_id)
        if not configuracion:
            return None
        for key, value in data.items():
            setattr(configuracion, key, value)
        db.session.commit()
        return configuracion

    @staticmethod
    def delete(configuracion_id):
        configuracion = Configuracion.query.get(configuracion_id)
        if not configuracion:
            return False
        db.session.delete(configuracion)
        db.session.commit()
        return True
