from flask_restful import Resource, reqparse
from services.notificacion_service import NotificacionService
from schemas.notificacion_schema import NotificacionSchema

class NotificacionResource(Resource):
    def get(self):
        notificaciones = NotificacionService.get_all()
        return [NotificacionSchema.object_to_json(n) for n in notificaciones], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('comentario', required=True)
        parser.add_argument('usuarioID', required=True, type=int)
        args = parser.parse_args()
        nueva = NotificacionService.create(args)
        return NotificacionSchema.object_to_json(nueva), 201

class NotificacionDetailResource(Resource):
    def get(self, notificacion_id):
        notificacion = NotificacionService.get_by_id(notificacion_id)
        if notificacion:
            return NotificacionSchema.object_to_json(notificacion), 200
        return {"message": "Notificación no encontrada"}, 404

    def put(self, notificacion_id):
        parser = reqparse.RequestParser()
        parser.add_argument('comentario', required=True)
        parser.add_argument('usuarioID', required=True, type=int)
        args = parser.parse_args()
        actualizado = NotificacionService.update(notificacion_id, args)
        if actualizado:
            return NotificacionSchema.object_to_json(actualizado), 200
        return {"message": "Notificación no encontrada"}, 404

    def delete(self, notificacion_id):
        eliminado = NotificacionService.delete(notificacion_id)
        if eliminado:
            return {"message": "Notificación eliminada"}, 200
        return {"message": "Notificación no encontrada"}, 404
