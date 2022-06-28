from django.contrib.auth.hashers import make_password

from main.models.Cliente import Cliente
from main.utils import dbClientes, status_conexao


class ClienteService():

    def __init__(self, cliente: Cliente = None):
        self.cliente = cliente

    # ---------------- Funções de interação com o banco ------------------#
    def cadastra(self):
        # hash senha, usar--> check_password(password, encoded) para checar no login
        self.cliente.senha = make_password(self.cliente.senha)
        # insere cliente
        cliente_dict = {'nome': self.cliente.nome,
                        'ddi': self.cliente.ddi,
                        'ddd': self.cliente.ddd,
                        'celular': self.cliente.celular,
                        'senha': self.cliente.senha,
                        'municipio_id': self.cliente.municipio_id,
                        'estado_id': self.cliente.estado_id}
        insert_result = dbClientes.insert_one(cliente_dict)
        return insert_result.acknowledged

    def busca(self, celular=None):
        if(celular == None):
            return dbClientes.find(projection={'_id': False})
        else:
            return dbClientes.find_one({'celular':  celular}, projection={'_id': False})

    def atualiza(self, celular_atual):
        '''
        Update clientes
        '''

        self.cliente.senha = make_password(self.cliente.senha)
        print(self.cliente_to_dict())

        alteracao = dbClientes.update_one({'celular':  celular_atual},
                                          {"$set": self.cliente_to_dict()})
        return alteracao

    def deleta(self):
        """Deleta clientes"""
        pass

    def celular_existe(self):
        celular = self.cliente.celular
        return dbClientes.count_documents({"celular": celular})

    def cliente_to_dict(self):
        cliente_dict = {'nome': self.cliente.nome,
                        'ddi': self.cliente.ddi,
                        'ddd': self.cliente.ddd,
                        'celular': self.cliente.celular,
                        'senha': self.cliente.senha,
                        'municipio_id': self.cliente.municipio_id,
                        'estado_id': self.cliente.estado_id}
        return cliente_dict
