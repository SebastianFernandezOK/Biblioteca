from models.prestamo_model import Prestamo
from database.connection import db  # Importa la instancia de SQLAlchemy correctamente

class PrestamoRepository:
    @staticmethod
    def get_all():
        return Prestamo.query.all()

    @staticmethod
    def get_by_id(prestamo_id):
        return Prestamo.query.get(prestamo_id)

    @staticmethod
    def create(prestamo):
        db.session.add(prestamo)
        db.session.commit()
        return prestamo

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(prestamo):
        db.session.delete(prestamo)
        db.session.commit()

    @staticmethod
    def get_by_usuario(usuario_id):
        # Devuelve todos los préstamos del usuario, sin filtrar por fecha_devuelta
        return Prestamo.query.filter_by(usuarioID=usuario_id).order_by(Prestamo.prestamoID.desc()).all()

    @staticmethod
    def get_paged(page=1, per_page=10):
        return Prestamo.query.order_by(Prestamo.prestamoID.desc()).paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_by_usuario_paged(usuario_id, page=1, per_page=5):
        return Prestamo.query.filter_by(usuarioID=usuario_id) \
            .order_by(Prestamo.prestamoID.desc()) \
            .paginate(page=page, per_page=per_page, error_out=False)