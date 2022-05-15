from main.utils import dbEstados

class EstadosService:

    def __init__(self):
        pass

    def buscaSiglasEstados(self):
        return dbEstados.find(projection = {'_id': False, 'nome': False})
    
    def estadoIdExiste(self, estado_id):
        return dbEstados.count_documents({"id": estado_id})