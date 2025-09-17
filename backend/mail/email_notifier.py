from flask_mail import Message
from flask import current_app
from datetime import datetime, timedelta
from database.connection import db
from models.prestamo_model import Prestamo
from models.usuario_model import Usuario
from models.libro_model import Libro

def notificar_prestamos_proximos_vencimiento(mail):
    ahora = datetime.now()
    en_48h = ahora + timedelta(hours=48)
    prestamos = Prestamo.query.filter(
        Prestamo.fecha_devolucion <= en_48h,
        Prestamo.fecha_devolucion > ahora,
        Prestamo.fecha_devuelta == None
    ).all()
    for prestamo in prestamos:
        usuario = Usuario.query.get(prestamo.usuarioID)
        libro = Libro.query.get(prestamo.libroID)
        libro_titulo = libro.titulo if libro else f"ID {prestamo.libroID}"
        if usuario and usuario.usuario_email:
            msg = Message(
                subject="Recordatorio: Préstamo próximo a vencer",
                sender=current_app.config.get('FLASKY_MAIL_SENDER'),
                recipients=[usuario.usuario_email],
                body=f"Hola {usuario.usuario_nombre}, tu préstamo del libro '{libro_titulo}' vence el {prestamo.fecha_devolucion.strftime('%d/%m/%Y %H:%M')}. Por favor, realiza la devolución a tiempo."
            )
            mail.send(msg)
            print(f"Correo enviado a {usuario.usuario_email} para el libro '{libro_titulo}' (préstamo {prestamo.prestamoID})")
