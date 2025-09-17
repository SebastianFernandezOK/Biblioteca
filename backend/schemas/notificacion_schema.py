from models.notificacion_model import Notificacion

class NotificacionSchema:
    @staticmethod
    def object_to_json(notificacion):
        return {
            "notificacionID": notificacion.notificacionID,
            "comentario": notificacion.comentario,
            "usuarioID": notificacion.usuarioID
        }

    @staticmethod
    def json_to_object(data):
        
        return Notificacion(
            notificacionID=data.get("notificacionID"),
            comentario=data.get("comentario"),
            usuarioID=data.get("usuarioID")
        )
