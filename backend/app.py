import os
from flask import Flask, send_from_directory
from flask_restful import Api
from flask_jwt_extended import JWTManager
from database.connection import db
from mail.mail import init_mail
from dotenv import load_dotenv
from datetime import timedelta
# Importar y registrar todos los resources
from resources.autor_resource import AutorResource, AutorDetailResource
from resources.libro_resource import LibroResource, LibroDetailResource
from resources.usuario_resource import UsuarioResource, UsuarioDetailResource
from resources.notificacion_resource import NotificacionResource, NotificacionDetailResource
from resources.prestamo_resource import PrestamoResource, PrestamoDetailResource, PrestamoPorUsuarioResource, PrestamoDevolverResource
from resources.resena_resource import ResenaResource, ResenaDetailResource, ResenasPorLibroResource
from resources.configuracion_resource import ConfiguracionResource, ConfiguracionDetailResource
from resources.auth_resource import AuthResource, ForgotPasswordResource, ResetPasswordResource
from resources.genero_resource import GeneroResource, GeneroDetailResource
from resources.estado_resource import EstadoResource, EstadoDetailResource
from resources.upload_resource import UploadResource

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database', 'biblioteca.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'  # Usa una clave segura o toma del entorno
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)

load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))

db.init_app(app)
api = Api(app)
jwt = JWTManager(app)
mail = init_mail(app)

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    from repositories.usuario_repository import UsuarioRepository
    usuario = UsuarioRepository.get_by_id(identity)
    return {
        'rol': usuario.rol if usuario else None,
        'id': usuario.usuarioID if usuario else None,
        'email': usuario.usuario_email if usuario else None
    }





api.add_resource(AutorResource, '/autores')
api.add_resource(AutorDetailResource, '/autores/<int:autor_id>')

api.add_resource(LibroResource, '/api/libros')
api.add_resource(LibroDetailResource, '/api/libros/<int:libro_id>')

api.add_resource(UsuarioResource, '/api/usuarios')
api.add_resource(UsuarioDetailResource, '/api/usuarios/<int:usuario_id>')

api.add_resource(NotificacionResource, '/notificaciones')
api.add_resource(NotificacionDetailResource, '/notificaciones/<int:notificacion_id>')

api.add_resource(PrestamoResource, '/api/prestamos')
api.add_resource(PrestamoDetailResource, '/api/prestamos/<int:prestamo_id>')
api.add_resource(PrestamoPorUsuarioResource, '/api/prestamos/usuario/<int:usuario_id>')
api.add_resource(PrestamoDevolverResource, '/api/prestamos/<int:prestamo_id>/devolver')

api.add_resource(ResenaResource, '/api/resenas')
api.add_resource(ResenaDetailResource, '/api/resenas/<int:resena_id>')
api.add_resource(ResenasPorLibroResource, '/api/resenas/libro/<int:libro_id>')

api.add_resource(ConfiguracionResource, '/configuraciones')
api.add_resource(ConfiguracionDetailResource, '/configuraciones/<int:configuracion_id>')

api.add_resource(AuthResource, '/api/login')
api.add_resource(ForgotPasswordResource, '/api/auth/forgot-password')
api.add_resource(ResetPasswordResource, '/api/auth/reset-password')

api.add_resource(GeneroResource, '/api/generos')
api.add_resource(GeneroDetailResource, '/api/generos/<int:generosID>')

api.add_resource(EstadoResource, '/api/estados')
api.add_resource(EstadoDetailResource, '/api/estados/<int:estadoID>')

api.add_resource(UploadResource, '/api/uploads/<string:folder>/<string:filename>')

if __name__ == '__main__':
    app.run(debug=True)