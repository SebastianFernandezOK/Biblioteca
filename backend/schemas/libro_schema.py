from models.libro_model import Libro

class LibroSchema:
    @staticmethod
    def object_to_json(libro, promedio_valoracion=None):
        # Permitir que 'libro' sea una tupla (Libro, promedio_valoracion)
        if isinstance(libro, tuple):
            libro, promedio_valoracion = libro
        data = {
            "libroID": libro.libroID,
            "titulo": libro.titulo,
            "cantidad": libro.cantidad,
            "editorial": libro.editorial,
            "generoID": libro.generoID,
            "genero_nombre": libro.genero.nombre if libro.genero else None,
            "image": libro.image,
            "autor": libro.autor
        }
        if promedio_valoracion is not None:
            data["promedio_valoracion"] = round(promedio_valoracion, 2)
        return data

    @staticmethod
    def json_to_object(data):
        return Libro(
            libroID=data.get("libroID"),
            titulo=data.get("titulo"),
            cantidad=data.get("cantidad"),
            editorial=data.get("editorial"),
            generoID=data.get("generoID"),
            image=data.get("image"),
            autor=data.get("autor")
        )
