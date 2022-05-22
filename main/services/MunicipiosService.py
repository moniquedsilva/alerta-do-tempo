import pymongo
from main.utils import dbMunicipios
class MunicipiosService:

    def __init__(self):
        pass
    
    def buscaCidadesByEstado(self, jsonQuery):
        return dbMunicipios.find(jsonQuery, {'_id':False, 'estado_id': False, 'nome_formatado':False, 'litoranea': False}).sort("nome_formatado", pymongo.ASCENDING)
    
    def municipioIdExiste(self, municipio_id):
        return dbMunicipios.count_documents({"id": municipio_id})
    


        