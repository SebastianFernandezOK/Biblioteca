from repositories.prestamo_repository import PrestamoRepository
from repositories.libro_repository import LibroRepository
from models.prestamo_model import Prestamo
from models.libro_model import Libro
from database.connection import db
from datetime import datetime

class PrestamoService:
    @staticmethod
    def listar_prestamos():
        return PrestamoRepository.get_all()

    @staticmethod
    def obtener_prestamo(prestamo_id):
        return PrestamoRepository.get_by_id(prestamo_id)

    @staticmethod
    def crear_prestamo(data):
        libro = LibroRepository.get_by_id_simple(data['libroID'])
        if not libro or libro.cantidad <= 0:
            return None  # O lanzar una excepción personalizada
        libro.cantidad -= 1
        db.session.add(libro)
        # Convertir fechas string a datetime
        fecha_entrega = datetime.strptime(data['fecha_entrega'], '%Y-%m-%d')
        fecha_devolucion = datetime.strptime(data['fecha_devolucion'], '%Y-%m-%d')
        prestamo = Prestamo(
            usuarioID=data['usuarioID'],
            libroID=data['libroID'],
            fecha_entrega=fecha_entrega,
            fecha_devolucion=fecha_devolucion,
            estadoID=1  # Pendiente
        )
        db.session.add(prestamo)
        db.session.commit()
        return prestamo

    @staticmethod
    def actualizar_prestamo():
        PrestamoRepository.update()

    @staticmethod
    def eliminar_prestamo(prestamo):
        # Si el préstamo está pendiente, devolver la cantidad al libro
        if prestamo.estadoID == 1:  # 1 = Pendiente
            libro = LibroRepository.get_by_id_simple(prestamo.libroID)
            if libro:
                libro.cantidad += 1
                db.session.add(libro)
        PrestamoRepository.delete(prestamo)

    @staticmethod
    def listar_prestamos_por_usuario(usuario_id):
        return PrestamoRepository.get_by_usuario(usuario_id)

    @staticmethod
    def devolver_prestamo(prestamo):
        from models.libro_model import Libro
        from repositories.libro_repository import LibroRepository
        if prestamo.fecha_devuelta is not None:
            return None
        prestamo.fecha_devuelta = datetime.now()
        prestamo.estadoID = 3  # Devuelto
        # Usar get_by_id_simple para obtener solo el objeto Libro
        libro = LibroRepository.get_by_id_simple(prestamo.libroID)
        if libro:
            libro.cantidad += 1
            db.session.add(libro)
        db.session.add(prestamo)
        db.session.commit()
        return prestamo

    @staticmethod
    def get_by_id(prestamo_id):
        return PrestamoRepository.get_by_id(prestamo_id)

    @staticmethod
    def listar_prestamos_paginados(page=1, per_page=10, libro=None):
        return PrestamoRepository.get_paged(page, per_page, libro)

    @staticmethod
    def listar_prestamos_por_usuario_paginados(usuario_id, page=1, per_page=5):
        return PrestamoRepository.get_by_usuario_paged(usuario_id, page, per_page)