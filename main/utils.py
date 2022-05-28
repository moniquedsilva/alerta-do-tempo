import os
from collections import defaultdict
from typing import Optional

import pymongo
import pymongo.database
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

STR_CONEXAO_DB: Optional[str] = os.getenv('STR_CONEXAO_DB')
NOME_DATABASE: Optional[str] = os.getenv('NOME_DATABASE')

client: pymongo.MongoClient = pymongo.MongoClient(STR_CONEXAO_DB)
db: pymongo.database.Database = client[str(NOME_DATABASE)]
dbClientes: pymongo.collection.Collection = db["Clientes"]
dbMunicipios: pymongo.collection.Collection = db["Municipios"]
dbEstados: pymongo.collection.Collection = db["Estados"]
