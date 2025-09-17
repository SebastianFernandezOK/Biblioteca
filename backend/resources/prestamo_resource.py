from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from services.prestamo_service import PrestamoService
from schemas.prestamo_schema import PrestamoSchema
from auth.decorators import role_required
from flask import request
from datetime import datetime
from flask_jwt_extended import get_jwt

class PrestamoResource(Resource):
    @role_required(["usuario", "admin", "bibliotecario"])
    @jwt_required()
    def get(self):
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))
        libro = request.args.get('libro')
        pagination = PrestamoService.listar_prestamos_paginados(page, per_page, libro)
        prestamos = [PrestamoSchema.object_to_json(p) for p in pagination.items]
        return {
            'prestamos': prestamos,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }, 200

    @role_required(["usuario", "admin", "bibliotecario"])
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('usuarioID', required=True, type=int)
        parser.add_argument('libroID', required=True, type=int)
        parser.add_argument('fecha_entrega', required=True)
        parser.add_argument('fecha_devolucion', required=True)
        args = parser.parse_args()
        nuevo_prestamo = PrestamoService.crear_prestamo(args)
        return PrestamoSchema.object_to_json(nuevo_prestamo), 201

class PrestamoDetailResource(Resource):
    @role_required(["usuario", "admin", "bibliotecario"])
    @jwt_required()
    def get(self, prestamo_id):
        prestamo = PrestamoService.get_by_id(prestamo_id)
        if not prestamo:
            return {"message": "Préstamo no encontrado"}, 404
        usuario_actual_id = get_jwt_identity()
        if int(usuario_actual_id) != int(prestamo.usuarioID):
            return {"message": "No tienes permiso para ver este préstamo."}, 403
        return PrestamoSchema.object_to_json(prestamo), 200

    @role_required(["bibliotecario", "admin"])
    @jwt_required()
    def put(self, prestamo_id):
        prestamo = PrestamoService.get_by_id(prestamo_id)
        if not prestamo:
            return {"message": "Préstamo no encontrado"}, 404
        usuario_actual_id = get_jwt_identity() 
        claims = get_jwt() 
        if claims.get("rol") not in ["bibliotecario", "admin"]:
            return {"message": "No tienes permiso para modificar este préstamo."}, 403
        parser = reqparse.RequestParser()
        parser.add_argument('estadoID', required=False, type=int)
        parser.add_argument('fecha_devuelta', required=False)
        parser.add_argument('fecha_entrega', required=False)
        parser.add_argument('fecha_devolucion', required=False)
        args = parser.parse_args()
        actualizado = False
        if args['estadoID'] is not None:
            # Si se rechaza (estadoID=4) y estaba pendiente, devolver la cantidad al libro
            if args['estadoID'] == 4 and prestamo.estadoID == 1:
                from repositories.libro_repository import LibroRepository
                libro = LibroRepository.get_by_id_simple(prestamo.libroID)
                if libro:
                    libro.cantidad += 1
                    from database.connection import db
                    db.session.add(libro)
            prestamo.estadoID = args['estadoID']
            actualizado = True
        if args['fecha_devuelta'] is not None:
            from datetime import datetime
            prestamo.fecha_devuelta = datetime.strptime(args['fecha_devuelta'], '%Y-%m-%dT%H:%M:%S')
            actualizado = True
        if args['fecha_entrega'] is not None:
            from datetime import datetime
            prestamo.fecha_entrega = datetime.strptime(args['fecha_entrega'], '%Y-%m-%d')
            actualizado = True
        if args['fecha_devolucion'] is not None:
            from datetime import datetime
            prestamo.fecha_devolucion = datetime.strptime(args['fecha_devolucion'], '%Y-%m-%d')
            actualizado = True
        if actualizado:
            from repositories.prestamo_repository import PrestamoRepository
            PrestamoRepository.update()
            from schemas.prestamo_schema import PrestamoSchema
            return PrestamoSchema.object_to_json(prestamo), 200
        return {"message": "No se enviaron campos para actualizar"}, 400

    @role_required(["usuario", "admin", "bibliotecario"])
    @jwt_required()
    def delete(self, prestamo_id):
        prestamo = PrestamoService.get_by_id(prestamo_id)
        if not prestamo:
            return {"message": "Préstamo no encontrado"}, 404
        usuario_actual_id = get_jwt_identity()
        if int(usuario_actual_id) != int(prestamo.usuarioID):
            return {"message": "No tienes permiso para eliminar este préstamo."}, 403
        eliminado = PrestamoService.delete(prestamo_id)
        if eliminado:
            return {"message": "Préstamo eliminado"}, 200
        return {"message": "Préstamo no encontrado"}, 404

class PrestamoPorUsuarioResource(Resource):
    @role_required(["usuario", "admin", "bibliotecario"])
    @jwt_required()
    def get(self, usuario_id):
        usuario_actual_id = get_jwt_identity()
        if int(usuario_actual_id) != int(usuario_id):
            return {"message": "No tienes permiso para ver los prestamos de otro usuario."}, 403
        # Soporte de paginación
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 5))
        pagination = PrestamoService.listar_prestamos_por_usuario_paginados(usuario_id, page, per_page)
        prestamos = [PrestamoSchema.object_to_json(p) for p in pagination.items]
        return {
            'prestamos': prestamos,
            'total': pagination.total,
            'page': pagination.page,
            'per_page': pagination.per_page,
            'pages': pagination.pages
        }, 200

class PrestamoDevolverResource(Resource):
    @role_required(["bibliotecario", "admin"])
    @jwt_required()
    def put(self, prestamo_id):
        prestamo = PrestamoService.get_by_id(prestamo_id)
        if not prestamo:
            return {"message": "Préstamo no encontrado"}, 404
        if prestamo.fecha_devuelta is not None:
            return {"message": "El préstamo ya fue devuelto"}, 400
        actualizado = PrestamoService.devolver_prestamo(prestamo)
        if actualizado:
            return PrestamoSchema.object_to_json(actualizado), 200
        return {"message": "Error al devolver el préstamo"}, 500
