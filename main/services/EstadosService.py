from main.utils import dbEstados


class EstadosService:

    def busca_siglas_estados(self):
        return dbEstados.find(projection={'_id': False, 'nome': False})

    def estado_id_existe(self, estado_id):
        return dbEstados.count_documents({"id": estado_id})
    
    def busca_estado_by_id(self, id):
        return dbEstados.find_one({'id': id}, projection={'_id': False})
