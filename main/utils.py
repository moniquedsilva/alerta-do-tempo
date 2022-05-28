import os

import pymongo
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

STR_CONEXAO_DB = os.getenv('STR_CONEXAO_DB')
NOME_DATABASE = os.getenv('NOME_DATABASE')

client: MongoClient = pymongo.MongoClient(STR_CONEXAO_DB)
db = client[NOME_DATABASE]  # type: ignore
dbClientes = db["Clientes"]
dbMunicipios = db["Municipios"]
dbEstados = db["Estados"]
