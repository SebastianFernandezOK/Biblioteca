from models.libro_model import Libro
from database.connection import db  # Asegúrate de que tu instancia de SQLAlchemy se llame 'db'

class LibroRepository:
    @staticmethod
    def get_all():
        return Libro.query.all()

    @staticmethod
    def get_paginated(page, per_page, search=None, generoID=None):
        from models.resena_model import Resena
        from sqlalchemy import func
        query = db.session.query(
            Libro,
            func.coalesce(func.avg(Resena.valoracion), 0).label('promedio_valoracion')
        ).outerjoin(Resena, Resena.libroID == Libro.libroID)
        if search:
            query = query.filter(Libro.titulo.ilike(f"%{search}%"))
        if generoID:
            query = query.filter(Libro.generoID == generoID)
        query = query.group_by(Libro.libroID).order_by(func.avg(Resena.valoracion).desc())
        # Paginación manual
        total = query.count()
        items_raw = query.offset((page - 1) * per_page).limit(per_page).all()
        # Convertir Row a tupla (Libro, promedio_valoracion) si es necesario
        items = []
        for item in items_raw:
            if hasattr(item, '_fields') and 'Libro' in item._fields and 'promedio_valoracion' in item._fields:
                items.append((item.Libro, item.promedio_valoracion))
            elif isinstance(item, tuple) and len(item) == 2:
                items.append(item)
            else:
                items.append(item)
        class Pagination:
            def __init__(self, items, total, page, per_page):
                self.items = items
                self.total = total
                self.page = page
                self.pages = (total // per_page) + (1 if total % per_page else 0)
        return Pagination(items, total, page, per_page)

    @staticmethod
    def get_by_id(libro_id):
        from models.resena_model import Resena
        from sqlalchemy import func
        # Obtener el libro
        libro = Libro.query.get(libro_id)
        if not libro:
            return None, None
        # Calcular el promedio de valoración
        promedio = db.session.query(func.coalesce(func.avg(Resena.valoracion), 0)).filter(Resena.libroID == libro_id).scalar()
        return libro, promedio

    @staticmethod
    def create(libro):
        db.session.add(libro)
        db.session.commit()
        return libro

    @staticmethod
    def update():
        db.session.commit()

    @staticmethod
    def delete(libro):
        db.session.delete(libro)
        db.session.commit()

    @staticmethod
    def get_by_id_simple(libro_id):
        return Libro.query.get(libro_id)