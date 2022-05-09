import pymongo
client = pymongo.MongoClient('')
db = client['AlertaDoTempo']
collection = db["Clientes"]
