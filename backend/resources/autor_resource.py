from flask_restful import Resource, reqparse
from services.autor_service import AutorService
from schemas.autor_schema import AutorSchema

class AutorResource(Resource):
    def get(self):
        autores = AutorService.get_all()
        return [AutorSchema.object_to_json(a) for a in autores], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('autor_nombre', required=True, help="El nombre es obligatorio")
        parser.add_argument('autor_apellido', required=True, help="El apellido es obligatorio")
        args = parser.parse_args()
        nuevo_autor = AutorService.create(args)
        return AutorSchema.object_to_json(nuevo_autor), 201

class AutorDetailResource(Resource):
    def get(self, autor_id):
        autor = AutorService.get_by_id(autor_id)
        if autor:
            return AutorSchema.object_to_json(autor), 200
        return {"message": "Autor no encontrado"}, 404

    def put(self, autor_id):
        parser = reqparse.RequestParser()
        parser.add_argument('autor_nombre', required=True)
        parser.add_argument('autor_apellido', required=True)
        args = parser.parse_args()
        actualizado = AutorService.update(autor_id, args)
        if actualizado:
            return AutorSchema.object_to_json(actualizado), 200
        return {"message": "Autor no encontrado"}, 404

    def delete(self, autor_id):
        eliminado = AutorService.delete(autor_id)
        if eliminado:
            return {"message": "Autor eliminado"}, 200
        return {"message": "Autor no encontrado"}, 404
