from django.contrib.auth.hashers import make_password

from main.models.Cliente import Cliente
from main.utils import dbClientes


class ClienteService():

    def __init__(self, cliente: Cliente = None):
        self.cliente = cliente

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

    def busca(self, celular):
        return dbClientes.find_one({'celular':  celular}, projection={'_id': False})

    def atualiza(self, celular_atual):
        '''
        Update clientes
        '''

        self.cliente.senha = make_password(self.cliente.senha)

        cliente_atualiza = {'nome': self.cliente.nome,
                        'ddi': self.cliente.ddi,
                        'ddd': self.cliente.ddd,
                        'celular': self.cliente.celular,
                        'senha': self.cliente.senha,
                        'municipio_id': self.cliente.municipio_id,
                        'estado_id': self.cliente.estado_id}

        alteracao =  dbClientes.update_one({'celular':  celular_atual} ,
            {
                "$set":{cliente_atualiza},
            }
            )
        return alteracao


    def deleta(self):
        """Deleta clientes"""
        pass

    def celular_existe(self):
        celular = self.cliente.celular
        return dbClientes.count_documents({"celular": celular})
