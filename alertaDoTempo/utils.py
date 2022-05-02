import pymongo
from django.conf import settings
client = pymongo.MongoClient('mongodb+srv://alerta:alerta@cluster0.ngat2.mongodb.net/AlertaDoTempo?retryWrites=true&w=majority')
db = client['AlertaDoTempo']
collection = db["Clientes"]