from flask_restful import Resource
from flask import send_from_directory
import os

class UploadResource(Resource):
    def get(self, folder, filename):
        # No es necesario cargar dotenv aquí, ya se carga en app.py
        if folder == 'users':
            upload_folder = os.getenv('UPLOAD_USERS_PATH', os.path.join(os.getcwd(), 'backend', 'upload', 'users'))
        elif folder == 'libros':
            upload_folder = os.getenv('UPLOAD_LIBROS_PATH', os.path.join(os.getcwd(), 'backend', 'upload', 'libros'))
        else:
            return {"message": "Carpeta no permitida"}, 404
        return send_from_directory(upload_folder, filename)

