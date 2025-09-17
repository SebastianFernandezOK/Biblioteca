from repositories.genero_repository import GeneroRepository

class GeneroService:
    @staticmethod
    def listar_generos():
        return GeneroRepository.get_all()

    @staticmethod
    def crear_genero(nombre):
        return GeneroRepository.create(nombre)

    @staticmethod
    def actualizar_genero(generosID, nombre):
        return GeneroRepository.update(generosID, nombre)

    @staticmethod
    def eliminar_genero(generosID):
        return GeneroRepository.delete(generosID)

    @staticmethod
    def obtener_genero(generosID):
        return GeneroRepository.get_by_id(generosID)
