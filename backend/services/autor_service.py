from repositories.autor_repository import AutorRepository

class AutorService:
    @staticmethod
    def listar_autores():
        return AutorRepository.get_all()

    @staticmethod
    def obtener_autor(autor_id):
        return AutorRepository.get_by_id(autor_id)

    @staticmethod
    def crear_autor(autor):
        # Aquí podrías agregar validaciones o lógica extra
        return AutorRepository.create(autor)

    @staticmethod
    def actualizar_autor():
        AutorRepository.update()

    @staticmethod
    def eliminar_autor(autor):
        AutorRepository.delete(autor)