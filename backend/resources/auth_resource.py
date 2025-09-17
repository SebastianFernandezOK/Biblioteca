from flask_restful import Resource
from flask import request, current_app
from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from mail.mail import init_mail
from werkzeug.security import check_password_hash

class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('usuario_email')
        password = data.get('usuario_contraseña')
        usuario = UsuarioRepository.get_by_email(email)
        if not usuario:
            return {'message': 'Usuario no encontrado'}, 404
        # Si las contraseñas están hasheadas, usar check_password_hash
        
        if not check_password_hash(usuario.usuario_contraseña, password):
            return {'message': 'Contraseña incorrecta'}, 401
        access_token = create_access_token(identity=str(usuario.usuarioID))  # identity debe ser string
        return {
            'usuarioID': usuario.usuarioID,
            'usuario_email': usuario.usuario_email,
            'rol': usuario.rol,
            'access_token': access_token
        }, 200

class ForgotPasswordResource(Resource):
    def post(self):
        email = request.json.get('email')
        usuario = UsuarioRepository.get_by_email(email)
        if not usuario:
            return {"message": "Email no registrado"}, 404
        s = URLSafeTimedSerializer('super-secret-key')  # Usa tu SECRET_KEY
        token = s.dumps(email, salt='password-reset-salt')
        reset_url = f"http://localhost:4200/reset-password?token={token}"
        mail = init_mail(current_app)
        msg = Message("Recuperar contraseña",
                      sender=current_app.config['FLASKY_MAIL_SENDER'],
                      recipients=[email])
        msg.body = f"Para restablecer tu contraseña, haz clic en el siguiente enlace: {reset_url}"
        mail.send(msg)
        return {"message": "Se envió el mail para recuperar la contraseña"}, 200

class ResetPasswordResource(Resource):
    def post(self):
        token = request.json.get('token')
        new_password = request.json.get('new_password')
        s = URLSafeTimedSerializer('super-secret-key')  # Usa tu SECRET_KEY
        try:
            email = s.loads(token, salt='password-reset-salt', max_age=3600)
        except Exception:
            return {"message": "Token inválido o expirado"}, 400
        usuario = UsuarioRepository.get_by_email(email)
        if not usuario:
            return {"message": "Usuario no encontrado"}, 404
        usuario.usuario_contraseña = generate_password_hash(new_password)
        UsuarioRepository.update(usuario)
        return {"message": "Contraseña actualizada correctamente"}, 200
