from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import UsuarioSchema
from werkzeug.security import generate_password_hash

class UsuarioService:
    @staticmethod
    def listar_usuarios():
        return UsuarioRepository.get_all()

    @staticmethod
    def listar_usuarios_query(nombre=None):
        return UsuarioRepository.get_query(nombre=nombre)

    @staticmethod
    def obtener_usuario(usuario_id):
        return UsuarioRepository.get_by_id(usuario_id)

    @staticmethod
    def obtener_usuario_por_email(email):
        return UsuarioRepository.get_by_email(email)

    @staticmethod
    def crear_usuario(data):
        # Hashear la contraseña antes de crear el usuario
        if 'usuario_contraseña' in data:
            data['usuario_contraseña'] = generate_password_hash(data['usuario_contraseña'])
        usuario = UsuarioSchema.json_to_object(data)
        return UsuarioRepository.create(usuario)

    @staticmethod
    def actualizar_usuario():
        UsuarioRepository.update()

    @staticmethod
    def eliminar_usuario(usuario):
        UsuarioRepository.delete(usuario)