from repositories.estado_repository import EstadoRepository

class EstadoService:
    @staticmethod
    def listar_estados():
        return EstadoRepository.get_all()

    @staticmethod
    def crear_estado(nombre, usuarioID=None):
        return EstadoRepository.create(nombre, usuarioID)

    @staticmethod
    def actualizar_estado(estadoID, nombre, usuarioID=None):
        return EstadoRepository.update(estadoID, nombre, usuarioID)

    @staticmethod
    def eliminar_estado(estadoID):
        return EstadoRepository.delete(estadoID)

    @staticmethod
    def obtener_estado(estadoID):
        return EstadoRepository.get_by_id(estadoID)
