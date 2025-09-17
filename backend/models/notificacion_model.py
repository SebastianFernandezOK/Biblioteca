from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Notificacion(db.Model):
    __tablename__ = 'notificaciones'

    notificacionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comentario = db.Column(db.String(100), nullable=False)
    usuarioID = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'), nullable=False)

    def __repr__(self):
        return f"<Notificacion {self.notificacionID}: {self.comentario}>"
