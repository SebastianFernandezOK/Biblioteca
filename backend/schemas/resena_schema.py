class ResenaSchema:
    @staticmethod
    def object_to_json(obj):
        # Obtener datos del usuario
        from models.usuario_model import Usuario
        usuario = Usuario.query.get(obj.usuarioID)
        return {
            "resenaID": obj.resenaID,
            "valoracion": obj.valoracion,
            "comentario": obj.comentario,
            "usuarioID": obj.usuarioID,
            "usuario_nombre": usuario.usuario_nombre if usuario else None,
            "image": usuario.image if usuario else None,
            "libroID": obj.libroID
        }

    @staticmethod
    def json_to_object(json_data):
        return {
            "valoracion": json_data.get("valoracion"),
            "comentario": json_data.get("comentario"),
            "usuarioID": json_data.get("usuarioID"),
            "libroID": json_data.get("libroID")
        }
