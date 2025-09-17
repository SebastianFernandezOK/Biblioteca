from models.autor_model import Autor
from database.connection import db  # Asegúrate de que tu instancia de SQLAlchemy se llame 'db'

class AutorRepository:
    @staticmethod
    def get_all():
        return Autor.query.all()

    @staticmethod
    def get_by_id(autor_id):
        return Autor.query.get(autor_id)

    @staticmethod
    def create(autor):
        db.session.add(autor)
        db.session.commit()
        return autor

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(autor):
        db.session.delete(autor)
        db.session.commit()