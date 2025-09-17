from flask_restful import Resource, reqparse
from flask import request
from services.libro_service import LibroService
from schemas.libro_schema import LibroSchema
import os 
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from auth.decorators import role_required


class LibroResource(Resource):
    @role_required(["usuario", "admin", "bibliotecario"])
    def get(self):
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        search = request.args.get('search', None, type=str)
        generoID = request.args.get('generoID', None, type=str)
        pagination = LibroService.get_paginated(page, per_page, search, generoID)
        # Adaptar para manejar Row, tupla o Libro
        libros = []
        for l in pagination.items:
            if hasattr(l, '_fields') and 'libro' in l._fields and 'promedio_valoracion' in l._fields:
                # Es un Row con campos libro y promedio_valoracion
                libros.append(LibroSchema.object_to_json((l.libro, l.promedio_valoracion)))
            elif isinstance(l, tuple) and len(l) == 2:
                libros.append(LibroSchema.object_to_json(l))
            else:
                libros.append(LibroSchema.object_to_json(l))
        return {
            'items': libros,
            'total': pagination.total,
            'page': pagination.page,
            'pages': pagination.pages
        }, 200

    @role_required(["admin", "bibliotecario"])
    def post(self):
        # Usar request.files para recibir la imagen
        
        load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
        titulo = request.form.get('titulo')
        cantidad = request.form.get('cantidad', type=int)
        editorial = request.form.get('editorial')
        genero = request.form.get('genero')
        image_file = request.files.get('image')
        if not (titulo and cantidad is not None and editorial and genero and image_file):
            return {"message": "Faltan datos o imagen"}, 400
        # Guardar la imagen en backend/upload/libros
        upload_folder = os.getenv('UPLOAD_LIBROS_PATH', os.path.join(os.getcwd(), 'backend', 'upload', 'libros'))
        os.makedirs(upload_folder, exist_ok=True)
        filename = f"libro_{titulo}_{image_file.filename}"
        image_path = os.path.join(upload_folder, filename)
        image_file.save(image_path)
        # Guardar solo el nombre del archivo en el campo 'image'
        args = {
            'titulo': titulo,
            'cantidad': cantidad,
            'editorial': editorial,
            'genero': genero,
            'image': filename
        }
        nuevo_libro = LibroService.create(args)
        return LibroSchema.object_to_json(nuevo_libro), 201

class LibroDetailResource(Resource):
    def get(self, libro_id):
        libro, promedio_valoracion = LibroService.get_by_id(libro_id)
        if libro:
            return LibroSchema.object_to_json((libro, promedio_valoracion)), 200
        return {"message": "Libro no encontrado"}, 404

    def put(self, libro_id):
        
        load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
        titulo = request.form.get('titulo')
        cantidad = request.form.get('cantidad', type=int)
        editorial = request.form.get('editorial')
        genero = request.form.get('genero')
        image_file = request.files.get('image')
        # Si se sube una nueva imagen, la guardamos
        if image_file and image_file.filename:
            upload_folder = os.getenv('UPLOAD_LIBROS_PATH', os.path.join(os.getcwd(), 'backend', 'upload', 'libros'))
            os.makedirs(upload_folder, exist_ok=True)
            filename = f"libro_{titulo}_{image_file.filename}"
            image_path = os.path.join(upload_folder, filename)
            image_file.save(image_path)
            image = filename
        else:
            image = request.form.get('image')  # Mantener la imagen actual si no se sube una nueva
        args = {
            'titulo': titulo,
            'cantidad': cantidad,
            'editorial': editorial,
            'genero': genero,
            'image': image
        }
        actualizado = LibroService.update(libro_id, args)
        if actualizado:
            return LibroSchema.object_to_json(actualizado), 200
        return {"message": "Libro no encontrado"}, 404

    def delete(self, libro_id):
        eliminado = LibroService.delete(libro_id)
        if eliminado:
            return {"message": "Libro eliminado"}, 200
        return {"message": "Libro no encontrado"}, 404

    def patch(self, libro_id):
        
        data = request.get_json()
        nueva_cantidad = data.get('cantidad')
        libro = LibroService.get_by_id(libro_id)
        if not libro:
            return {"message": "Libro no encontrado"}, 404
        if nueva_cantidad is None:
            return {"message": "Cantidad requerida"}, 400
        if nueva_cantidad < 0:
            return {"message": "Cantidad inválida"}, 400
        if nueva_cantidad == 0:
            # Eliminar el libro si la cantidad es 0
            eliminado = LibroService.delete(libro_id)
            if eliminado:
                return {"message": "Libro eliminado por cantidad 0"}, 200
            else:
                return {"message": "Error al eliminar libro"}, 500
        # Actualizar la cantidad
        actualizado = LibroService.update(libro_id, {"cantidad": nueva_cantidad})
        if actualizado:
            return LibroSchema.object_to_json(actualizado), 200
        return {"message": "Error al actualizar cantidad"}, 500
