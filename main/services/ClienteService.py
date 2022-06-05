import json

from django.contrib.auth.hashers import make_password

from main.models.Cliente import Cliente
from main.utils import dbClientes


class ClienteService:

    def __init__(self, cliente: Cliente):
        self.cliente = cliente

    def cadastra(self):
        # hash senha, usar--> check_password(password, encoded) para checar no login
        self.cliente.senha = make_password(self.cliente.senha)
        # insere cliente
        clienteDict = self.cliente.__dict__
        insert_result = dbClientes.insert_one(clienteDict)
        return insert_result.acknowledged

    def busca(self):
        return dbClientes.find({"nome": self.cliente.nome, "celular":  self.cliente.celular})

    def atualiza(self):
        pass

    def deleta(self):
        pass

    def celularJaExiste(self):
        celular = self.cliente.celular
        return dbClientes.count_documents({"celular": celular})
