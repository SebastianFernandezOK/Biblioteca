from flask_restful import Resource, reqparse
from services.usuario_service import UsuarioService
from schemas.usuario_schema import UsuarioSchema
from flask import request
import os
from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import UsuarioSchema

class UsuarioResource(Resource):
    def get(self):
        # Obtener parámetros de paginación y filtro
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        nombre = request.args.get('nombre', None)
        usuarios_query = UsuarioService.listar_usuarios_query(nombre=nombre)
        paginated = usuarios_query.paginate(page=page, per_page=per_page, error_out=False)
        usuarios = [UsuarioSchema.object_to_json(u) for u in paginated.items]
        return {
            'usuarios': usuarios,
            'total': paginated.total,
            'page': page,
            'per_page': per_page
        }, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usuario_nombre', required=True)
        parser.add_argument('usuario_apellido', required=True)
        parser.add_argument('usuario_contraseña', required=True)
        parser.add_argument('usuario_email', required=True)
        parser.add_argument('usuario_telefono', required=True, type=int)
        parser.add_argument('rol', required=False, )
        args = parser.parse_args()
        nuevo_usuario = UsuarioService.crear_usuario(args)
        return UsuarioSchema.object_to_json(nuevo_usuario), 201

class UsuarioDetailResource(Resource):
    def get(self, usuario_id):
        usuario = UsuarioService.obtener_usuario(usuario_id)
        if usuario:
            return UsuarioSchema.object_to_json(usuario), 200
        return {"message": "Usuario no encontrado"}, 404

    def delete(self, usuario_id):
        usuario = UsuarioService.obtener_usuario(usuario_id)
        if usuario:
            UsuarioService.eliminar_usuario(usuario)
            return {"message": "Usuario eliminado"}, 200
        return {"message": "Usuario no encontrado"}, 404

    def patch(self, usuario_id):
        usuario = UsuarioService.obtener_usuario(usuario_id)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404
        # Detecta si viene como multipart/form-data (FormData)
        if request.content_type and request.content_type.startswith('multipart/form-data'):
            form = request.form
            usuario_nombre = form.get('usuario_nombre')
            usuario_apellido = form.get('usuario_apellido')
            usuario_email = form.get('usuario_email')
            usuario_telefono = form.get('usuario_telefono')
            rol = form.get('rol')
        else:
            data = request.get_json(force=True, silent=True) or {}
            usuario_nombre = data.get('usuario_nombre')
            usuario_apellido = data.get('usuario_apellido')
            usuario_email = data.get('usuario_email')
            usuario_telefono = data.get('usuario_telefono')
            rol = data.get('rol')
        if usuario_nombre is not None:
            usuario.usuario_nombre = usuario_nombre
        if usuario_apellido is not None:
            usuario.usuario_apellido = usuario_apellido
        if usuario_email is not None:
            usuario.usuario_email = usuario_email
        if usuario_telefono is not None:
            usuario.usuario_telefono = usuario_telefono
        if rol is not None:
            usuario.rol = rol
        # Manejo de imagen de perfil
        upload_folder = os.getenv('UPLOAD_USERS_PATH', os.path.join(os.getcwd(), 'backend', 'upload', 'users'))
        if 'image' in request.files:
            image_file = request.files['image']
            if image_file.filename:
                os.makedirs(upload_folder, exist_ok=True)
                filename = f"user_{usuario_id}_{image_file.filename}"
                filepath = os.path.join(upload_folder, filename)
                image_file.save(filepath)
                usuario.image = filename  # Solo el nombre del archivo
        UsuarioRepository.update(usuario)
        return UsuarioSchema.object_to_json(usuario), 200
