from models.genero_model import Genero
from database.connection import db

class GeneroRepository:
    @staticmethod
    def get_all():
        return Genero.query.all()

    @staticmethod
    def get_by_id(generosID):
        return Genero.query.get(generosID)

    @staticmethod
    def create(nombre):
        genero = Genero(nombre=nombre)
        db.session.add(genero)
        db.session.commit()
        return genero

    @staticmethod
    def update(generosID, nombre):
        genero = Genero.query.get(generosID)
        if genero:
            genero.nombre = nombre
            db.session.commit()
        return genero

    @staticmethod
    def delete(generosID):
        genero = Genero.query.get(generosID)
        if genero:
            db.session.delete(genero)
            db.session.commit()
            return True
        return False
