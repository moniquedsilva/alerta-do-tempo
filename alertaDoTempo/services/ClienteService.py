from alertaDoTempo.utils import collection

class ClienteService:

    def __init__(self, nome, cel, password, municipio, estado):
        self.nome = nome
        self.cel = cel
        self.password = password
        self.municipio = municipio
        self.estado = estado

    def cadastra(self):
        cliente = self.toJson()
        insert_result = collection.insert_one(cliente)
        return insert_result.acknowledged

    def toJson(self):
        cliente = {
            "nome" : self.nome,
            "celular" : self.cel,
            "password" : self.password,
            "municipio" : self.municipio,
            "estado": self.estado   
        }
        return cliente
