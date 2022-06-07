import pymongo

from main.utils import dbMunicipios


class MunicipiosService:

    def busca_cidades_by_estado(self, json_query):
        return dbMunicipios.find(json_query, {'_id': False, 'estado_id': False, 'nome_formatado': False, 'litoranea': False}).sort("nome_formatado", pymongo.ASCENDING)

    def municipio_id_existe(self, municipio_id):
        return dbMunicipios.count_documents({"id": municipio_id})
