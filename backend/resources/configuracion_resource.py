from flask_restful import Resource, reqparse
from services.configuracion_service import ConfiguracionService
from schemas.configuracion_schema import ConfiguracionSchema

class ConfiguracionResource(Resource):
    def get(self):
        configuraciones = ConfiguracionService.get_all()
        return [ConfiguracionSchema.object_to_json(c) for c in configuraciones], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('idioma', required=True)
        parser.add_argument('orden', required=True)
        parser.add_argument('usuario_id', required=True, type=int)
        args = parser.parse_args()
        nueva_config = ConfiguracionService.create(args)
        return ConfiguracionSchema.object_to_json(nueva_config), 201

class ConfiguracionDetailResource(Resource):
    def get(self, configuracion_id):
        config = ConfiguracionService.get_by_id(configuracion_id)
        if config:
            return ConfiguracionSchema.object_to_json(config), 200
        return {"message": "Configuración no encontrada"}, 404

    def put(self, configuracion_id):
        parser = reqparse.RequestParser()
        parser.add_argument('idioma', required=True)
        parser.add_argument('orden', required=True)
        parser.add_argument('usuario_id', required=True, type=int)
        args = parser.parse_args()
        actualizado = ConfiguracionService.update(configuracion_id, args)
        if actualizado:
            return ConfiguracionSchema.object_to_json(actualizado), 200
        return {"message": "Configuración no encontrada"}, 404

    def delete(self, configuracion_id):
        eliminado = ConfiguracionService.delete(configuracion_id)
        if eliminado:
            return {"message": "Configuración eliminada"}, 200
        return {"message": "Configuración no encontrada"}, 404
