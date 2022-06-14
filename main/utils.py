import os
from typing import Optional

import pymongo
import pymongo.database
from dotenv import load_dotenv

load_dotenv()

STR_CONEXAO_DB: Optional[str] = os.getenv('STR_CONEXAO_DB')
NOME_DATABASE: Optional[str] = os.getenv('NOME_DATABASE')

try:
    client: pymongo.MongoClient = pymongo.MongoClient(STR_CONEXAO_DB)
    db: pymongo.database.Database = client[str(NOME_DATABASE)]
    dbClientes: pymongo.collection.Collection = db["Clientes"]
    dbMunicipios: pymongo.collection.Collection = db["Municipios"]
    dbEstados: pymongo.collection.Collection = db["Estados"]
    dbCondicoesTempo: pymongo.collection.Collection = db["CondicoesTempo"]
    status_conexao = True
except Exception as e:
    status_conexao = False
