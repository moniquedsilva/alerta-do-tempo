from main.utils import dbMunicipios
from main.utils import dbEstados

class MunicipiosService:

    def __init__(self):
        None
    
    @classmethod
    def buscaSiglasEstados(cls):
        return dbEstados.find(projection = {'nome': False})
    
    @classmethod
    def buscaCidadesByEstado(cls, jsonQuery):
        return dbMunicipios.find(jsonQuery, {'estado_id': False, 'nome_formatado':False, 'litoranea': False}).sort("nome")
        

        