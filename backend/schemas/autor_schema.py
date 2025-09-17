from models.autor_model import Autor

class AutorSchema:
    @staticmethod
    def object_to_json(autor):
        return {
            "autorID": autor.autorID,
            "autor_nombre": autor.autor_nombre,
            "autor_apellido": autor.autor_apellido
        }

    @staticmethod
    def json_to_object(data):
        
        return Autor(
            autorID=data.get("autorID"),
            autor_nombre=data.get("autor_nombre"),
            autor_apellido=data.get("autor_apellido")
        )
