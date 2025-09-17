from repositories.resena_repository import ResenaRepository

class ResenaService:
    @staticmethod
    def get_all():
        return ResenaRepository.get_all()

    @staticmethod
    def get_by_id(resena_id):
        return ResenaRepository.get_by_id(resena_id)

    @staticmethod
    def create(data):
        return ResenaRepository.create(data)

    @staticmethod
    def update(resena_id, data):
        return ResenaRepository.update(resena_id, data)

    @staticmethod
    def delete(resena_id):
        return ResenaRepository.delete(resena_id)

    @staticmethod
    def get_by_libro(libro_id):
        return ResenaRepository.get_by_libro(libro_id)