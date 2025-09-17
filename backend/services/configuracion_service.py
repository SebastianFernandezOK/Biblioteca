from repositories.configuracion_repository import ConfiguracionRepository

class ConfiguracionService:
    @staticmethod
    def listar_configuraciones():
        return ConfiguracionRepository.get_all()

    @staticmethod
    def obtener_configuracion(configuracion_id):
        return ConfiguracionRepository.get_by_id(configuracion_id)

    @staticmethod
    def crear_configuracion(configuracion):
        # Aquí podrías agregar validaciones o lógica extra
        return ConfiguracionRepository.create(configuracion)

    @staticmethod
    def actualizar_configuracion():
        ConfiguracionRepository.update()

    @staticmethod
    def eliminar_configuracion(configuracion):
        ConfiguracionRepository.delete(configuracion)