import os
from flask_sqlalchemy import SQLAlchemy

# Ruta absoluta al archivo de la base de datos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'biblioteca.db')

db = SQLAlchemy()

# Función para obtener una conexión a la base de datos
def get_connection():
    conn = db.engine.connect()
    return conn
