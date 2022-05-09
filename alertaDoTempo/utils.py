from dotenv import load_dotenv
import pymongo
import os

load_dotenv()

STR_CONEXAO_DB = os.getenv('STR_CONEXAO_DB')
NOME_DATABASE = os.getenv('NOME_DATABASE')

client = pymongo.MongoClient(STR_CONEXAO_DB)
db = client[NOME_DATABASE]
collection = db["Clientes"]