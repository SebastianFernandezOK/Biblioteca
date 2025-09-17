import time
from flask import Flask
from mail.mail import init_mail
from mail.email_notifier import notificar_prestamos_proximos_vencimiento
from database.connection import db
import os

# Importa tu modelo y configuración de app
from models.prestamo_model import Prestamo
from models.usuario_model import Usuario

# Crea la app Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///../database/biblioteca.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
mail = init_mail(app)
db.init_app(app)

with app.app_context():
    while True:
        print("Buscando préstamos próximos a vencer...")
        notificar_prestamos_proximos_vencimiento(mail)
        print("Esperando 60 segundos...")
        time.sleep(60)
