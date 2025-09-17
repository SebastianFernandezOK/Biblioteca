from repositories.notificacion_repository import NotificacionRepository

class NotificacionService:
    @staticmethod
    def listar_notificaciones():
        return NotificacionRepository.get_all()

    @staticmethod
    def obtener_notificacion(notificacion_id):
        return NotificacionRepository.get_by_id(notificacion_id)

    @staticmethod
    def crear_notificacion(notificacion):
        # Aquí podrías agregar validaciones o lógica extra
        return NotificacionRepository.create(notificacion)

    @staticmethod
    def actualizar_notificacion():
        NotificacionRepository.update()

    @staticmethod
    def eliminar_notificacion(notificacion):
        NotificacionRepository.delete(notificacion)