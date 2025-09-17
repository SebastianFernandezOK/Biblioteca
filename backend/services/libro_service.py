from repositories.libro_repository import LibroRepository
from database.connection import db

class LibroService:
    @staticmethod
    def listar_libros():
        return LibroRepository.get_all()

    @staticmethod
    def get_all():
        return LibroRepository.get_all()

    @staticmethod
    def get_paginated(page, per_page, search=None, generoID=None, autor=None):
        return LibroRepository.get_paginated(page, per_page, search, generoID, autor)

    @staticmethod
    def obtener_libro(libro_id):
        return LibroRepository.get_by_id(libro_id)

    @staticmethod
    def crear_libro(libro):
        # Aquí podrías agregar validaciones o lógica extra
        return LibroRepository.create(libro)

    @staticmethod
    def actualizar_libro():
        # Aquí podrías agregar lógica antes de actualizar
        LibroRepository.update()

    @staticmethod
    def eliminar_libro(libro):
        LibroRepository.delete(libro)

    @staticmethod
    def get_by_id(libro_id):
        return LibroRepository.get_by_id(libro_id)

    @staticmethod
    def update(libro_id, data):
        print(f'PATCH update: libro_id={libro_id}, data={data}')  # Depuración
        libro_obj = LibroRepository.get_by_id(libro_id)
        # Si es una tupla (Libro, promedio), tomar solo el objeto Libro
        if isinstance(libro_obj, tuple):
            libro = libro_obj[0]
        else:
            libro = libro_obj
        if not libro:
            print('Libro no encontrado para actualizar cantidad')
            return None
        try:
            # Si se actualiza el género, buscar la instancia
            if 'genero' in data:
                from models.genero_model import Genero
                genero_obj = Genero.query.get(data['genero'])
                libro.genero = genero_obj
                libro.generoID = data['genero']
                del data['genero']
            for key, value in data.items():
                setattr(libro, key, value)
            db.session.commit()
            print('Libro actualizado correctamente')
            return libro
        except Exception as e:
            print('Error al actualizar libro:', e)
            return None

    @staticmethod
    def delete_by_id(libro_id):
        libro = LibroRepository.get_by_id(libro_id)
        if not libro:
            return False
        db.session.delete(libro)
        db.session.commit()
        return True

    @staticmethod
    def create(args):
        from models.libro_model import Libro
        from models.genero_model import Genero
        print('Datos recibidos para crear libro:', args)  # Log para depuración
        genero_id = args.get('genero')
        genero_obj = Genero.query.get(genero_id)
        if not genero_obj:
            raise ValueError(f"El género con ID {genero_id} no existe")
        nuevo_libro = Libro(
            titulo=args['titulo'],
            cantidad=args['cantidad'],
            editorial=args['editorial'],
            generoID=genero_id,
            genero=genero_obj,
            image=args['image'],
            autor=args.get('autor')
        )
        try:
            libro_guardado = LibroRepository.create(nuevo_libro)
            print('Libro guardado correctamente:', libro_guardado)
            return libro_guardado
        except Exception as e:
            print('Error al guardar libro:', e)
            raise e

    @staticmethod
    def delete(libro_id):
        from models.prestamo_model import Prestamo
        libro_obj = LibroRepository.get_by_id(libro_id)
        # Si es una tupla (Libro, promedio), tomar solo el objeto Libro
        if isinstance(libro_obj, tuple):
            libro = libro_obj[0]
        else:
            libro = libro_obj
        if not libro:
            return False
        # Verificar si hay préstamos pendientes o activos
        prestamos = Prestamo.query.filter(Prestamo.libroID == libro_id, Prestamo.estadoID.in_([1, 2])).all()
        if prestamos:
            # Hay préstamos pendientes o activos, no eliminar
            return False
        db.session.delete(libro)
        db.session.commit()
        return True