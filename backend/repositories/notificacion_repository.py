from models.notificacion_model import Notificacion
from database.connection import db  # Importa la instancia de SQLAlchemy correctamente

class NotificacionRepository:
    @staticmethod
    def get_all():
        return Notificacion.query.all()

    @staticmethod
    def get_by_id(notificacion_id):
        return Notificacion.query.get(notificacion_id)

    @staticmethod
    def create(notificacion):
        db.session.add(notificacion)
        db.session.commit()
        return notificacion

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(notificacion):
        db.session.delete(notificacion)
        db.session.commit()