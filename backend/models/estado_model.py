from database.connection import db

class Estado(db.Model):
    __tablename__ = 'estados'
    estadoID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(20), unique=True, nullable=False)
    usuarioID = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f'<Estado {self.nombre}>'
