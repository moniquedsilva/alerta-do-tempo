import pymongo

from main.utils import dbCondicoesTempo

class CondicoesTempoService:

    def busca(self):
        return dbCondicoesTempo.find(projection={'_id': False})
