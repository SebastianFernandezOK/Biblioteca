from flask_restful import Resource, reqparse
from services.genero_service import GeneroService
from flask import request

class GeneroResource(Resource):
    def get(self):
        generos = GeneroService.listar_generos()
        return [{'generosID': g.generosID, 'nombre': g.nombre} for g in generos], 200

    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        if not nombre:
            return {'message': 'Nombre requerido'}, 400
        genero = GeneroService.crear_genero(nombre)
        return {'generosID': genero.generosID, 'nombre': genero.nombre}, 201

class GeneroDetailResource(Resource):
    def get(self, generosID):
        genero = GeneroService.obtener_genero(generosID)
        if genero:
            return {'generosID': genero.generosID, 'nombre': genero.nombre}, 200
        return {'message': 'Género no encontrado'}, 404

    def put(self, generosID):
        data = request.get_json()
        nombre = data.get('nombre')
        genero = GeneroService.actualizar_genero(generosID, nombre)
        if genero:
            return {'generosID': genero.generosID, 'nombre': genero.nombre}, 200
        return {'message': 'Género no encontrado'}, 404

    def delete(self, generosID):
        eliminado = GeneroService.eliminar_genero(generosID)
        if eliminado:
            return {'message': 'Género eliminado'}, 200
        return {'message': 'Género no encontrado'}, 404
