from database.connection import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    usuarioID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_nombre = db.Column(db.String(100), nullable=False)
    usuario_apellido = db.Column(db.String(100), nullable=False)
    usuario_contraseña = db.Column(db.String(100), nullable=False)
    usuario_email = db.Column(db.String(100), nullable=False, unique=True)
    usuario_telefono = db.Column(db.Integer, nullable=False)
    rol = db.Column(db.String(10), nullable=True)  # Permite que el campo rol sea NULL
    image = db.Column(db.String, nullable=True)  # Ruta de la imagen de perfil

    def __repr__(self):
        return f"<Usuario {self.usuarioID}: {self.usuario_nombre} {self.usuario_apellido}>"
