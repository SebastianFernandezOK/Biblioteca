from models.prestamo_model import Prestamo
from models.usuario_model import Usuario
from models.libro_model import Libro
from models.estado_model import Estado
from datetime import datetime

class PrestamoSchema:
    @staticmethod
    def object_to_json(prestamo):
        def to_iso(val):
            if isinstance(val, datetime):
                return val.isoformat()
            return val
        # Obtener usuario, libro y estado
        usuario = Usuario.query.get(prestamo.usuarioID)
        libro = Libro.query.get(prestamo.libroID)
        estado = Estado.query.get(prestamo.estadoID)
        return {
            "prestamoID": prestamo.prestamoID,
            "usuarioID": prestamo.usuarioID,
            "usuario_nombre": usuario.usuario_nombre if usuario else None,
            "usuario_apellido": usuario.usuario_apellido if usuario else None,
            "libroID": prestamo.libroID,
            "libro_titulo": libro.titulo if libro else None,
            "fecha_entrega": to_iso(prestamo.fecha_entrega),
            "fecha_devolucion": to_iso(prestamo.fecha_devolucion),
            "fecha_devuelta": to_iso(getattr(prestamo, 'fecha_devuelta', None)),
            "estadoID": prestamo.estadoID,
            "estado_nombre": estado.nombre if estado else None
        }

    @staticmethod
    def json_to_object(data):
        
        return Prestamo(
            prestamoID=data.get("prestamoID"),
            usuarioID=data.get("usuarioID"),
            libroID=data.get("libroID"),
            fecha_entrega=data.get("fecha_entrega"),
            fecha_devolucion=data.get("fecha_devolucion"),
            estadoID=data.get("estadoID")
        )
