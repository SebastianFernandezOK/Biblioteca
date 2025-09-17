from models.configuracion_model import Configuracion

class ConfiguracionSchema:
    @staticmethod
    def object_to_json(configuracion):
        return {
            "configuracionID": configuracion.configuracionID,
            "idioma": configuracion.idioma,
            "orden": configuracion.orden,
            "usuario_id": configuracion.usuario_id
        }

    @staticmethod
    def json_to_object(data):
        
        return Configuracion(
            configuracionID=data.get("configuracionID"),
            idioma=data.get("idioma"),
            orden=data.get("orden"),
            usuario_id=data.get("usuario_id")
        )
