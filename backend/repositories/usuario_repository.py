from models.usuario_model import Usuario
from database.connection import db  # Importa la instancia de SQLAlchemy correctamente
from sqlalchemy import or_

class UsuarioRepository:
    @staticmethod
    def get_all():
        return Usuario.query.all()

    @staticmethod
    def get_query(nombre=None):
        query = Usuario.query
        if nombre:
            query = query.filter(Usuario.usuario_nombre.ilike(f"%{nombre}%"))
        return query

    @staticmethod
    def get_by_id(usuario_id):
        return Usuario.query.get(usuario_id)

    @staticmethod
    def get_by_email(email):
        return Usuario.query.filter_by(usuario_email=email).first()

    @staticmethod
    def create(usuario):
        db.session.add(usuario)
        db.session.commit()
        return usuario

    @staticmethod
    def update(usuario):
        db.session.merge(usuario)
        db.session.commit()

    @staticmethod
    def delete(usuario):
        db.session.delete(usuario)
        db.session.commit()