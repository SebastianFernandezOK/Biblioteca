from flask_restful import Resource, reqparse
from services.resena_service import ResenaService
from schemas.resena_schema import ResenaSchema
from models.prestamo_model import Prestamo

class ResenaResource(Resource):
    def get(self):
        resenas = ResenaService.get_all()
        return [ResenaSchema.object_to_json(r) for r in resenas], 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('valoracion', required=True, type=int)
        parser.add_argument('comentario', required=True)
        parser.add_argument('usuarioID', required=True, type=int)
        parser.add_argument('libroID', required=True, type=int)
        args = parser.parse_args()
        # Validar que el usuario haya tenido un préstamo de este libro
        prestamo = Prestamo.query.filter_by(usuarioID=args['usuarioID'], libroID=args['libroID']).first()
        if not prestamo:
            return {'message': 'Debes haber tenido un préstamo de este libro para dejar una reseña.'}, 403
        nueva_resena = ResenaService.create(args)
        return ResenaSchema.object_to_json(nueva_resena), 201

class ResenaDetailResource(Resource):
    def get(self, resena_id):
        resena = ResenaService.get_by_id(resena_id)
        if resena:
            return ResenaSchema.object_to_json(resena), 200
        return {"message": "Resena no encontrada"}, 404

    def put(self, resena_id):
        parser = reqparse.RequestParser()
        parser.add_argument('valoracion', required=True, type=int)
        parser.add_argument('comentario', required=True)
        parser.add_argument('usuarioID', required=True, type=int)
        parser.add_argument('libroID', required=True, type=int)
        args = parser.parse_args()
        actualizado = ResenaService.update(resena_id, args)
        if actualizado:
            return ResenaSchema.object_to_json(actualizado), 200
        return {"message": "Resena no encontrada"}, 404

    def delete(self, resena_id):
        eliminado = ResenaService.delete(resena_id)
        if eliminado:
            return {"message": "Resena eliminada"}, 200
        return {"message": "Resena no encontrada"}, 404

class ResenasPorLibroResource(Resource):
    def get(self, libro_id):
        resenas = ResenaService.get_by_libro(libro_id)
        return [ResenaSchema.object_to_json(r) for r in resenas], 200
