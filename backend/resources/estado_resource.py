from flask_restful import Resource
from services.estado_service import EstadoService
from flask import request

class EstadoResource(Resource):
    def get(self):
        estados = EstadoService.listar_estados()
        return [{'estadoID': e.estadoID, 'nombre': e.nombre, 'usuarioID': e.usuarioID} for e in estados], 200

    def post(self):
        data = request.get_json()
        nombre = data.get('nombre')
        usuarioID = data.get('usuarioID')
        if not nombre:
            return {'message': 'Nombre requerido'}, 400
        estado = EstadoService.crear_estado(nombre, usuarioID)
        return {'estadoID': estado.estadoID, 'nombre': estado.nombre, 'usuarioID': estado.usuarioID}, 201

class EstadoDetailResource(Resource):
    def get(self, estadoID):
        estado = EstadoService.obtener_estado(estadoID)
        if estado:
            return {'estadoID': estado.estadoID, 'nombre': estado.nombre, 'usuarioID': estado.usuarioID}, 200
        return {'message': 'Estado no encontrado'}, 404

    def put(self, estadoID):
        data = request.get_json()
        nombre = data.get('nombre')
        usuarioID = data.get('usuarioID')
        estado = EstadoService.actualizar_estado(estadoID, nombre, usuarioID)
        if estado:
            return {'estadoID': estado.estadoID, 'nombre': estado.nombre, 'usuarioID': estado.usuarioID}, 200
        return {'message': 'Estado no encontrado'}, 404

    def delete(self, estadoID):
        eliminado = EstadoService.eliminar_estado(estadoID)
        if eliminado:
            return {'message': 'Estado eliminado'}, 200
        return {'message': 'Estado no encontrado'}, 404
