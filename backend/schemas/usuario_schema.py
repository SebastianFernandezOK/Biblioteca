from models.usuario_model import Usuario

class UsuarioSchema:
    @staticmethod
    def object_to_json(usuario):
        return {
            "usuarioID": usuario.usuarioID,
            "usuario_nombre": usuario.usuario_nombre,
            "usuario_apellido": usuario.usuario_apellido,
            "usuario_contraseña": usuario.usuario_contraseña,
            "usuario_email": usuario.usuario_email,
            "usuario_telefono": usuario.usuario_telefono,
            "rol": usuario.rol,
            "image": usuario.image  # Agregado campo imagen
        }

    @staticmethod
    def json_to_object(data):
        return Usuario(
            usuario_nombre=data.get("usuario_nombre"),
            usuario_apellido=data.get("usuario_apellido"),
            usuario_contraseña=data.get("usuario_contraseña"),
            usuario_email=data.get("usuario_email"),
            usuario_telefono=data.get("usuario_telefono"),
            rol=data.get("rol", None)  # Cambiado a None por defecto
        )
