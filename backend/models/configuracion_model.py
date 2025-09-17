from database.connection import db

class Configuracion(db.Model):
    __tablename__ = 'configuraciones'

    configuracionID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    idioma = db.Column(db.String, nullable=False)
    orden = db.Column(db.String, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.usuarioID'))

    def __repr__(self):
        return f"<Configuracion {self.configuracionID}: Usuario {self.usuario_id}>"
