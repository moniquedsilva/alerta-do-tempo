from main.utils import dbClientes

class ClienteService:

    def __init__(self, nome, cel, senha, municipio, estado):
        self.nome = nome
        self.cel = cel
        self.senha = senha
        self.municipio = municipio
        self.estado = estado

    def cadastra(self):
        cliente = self.toJson()
        insert_result = dbClientes.insert_one(cliente)
        return insert_result.acknowledged

    def toJson(self):
        cliente = {
            "nome" : self.nome,
            "celular" : self.cel,
            "senha" : self.senha,
            "municipio" : self.municipio,
            "estado": self.estado   
        }
        return cliente
