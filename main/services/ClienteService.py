from django.contrib.auth.hashers import make_password

from main.models.Cliente import Cliente
from main.utils import dbClientes, status_conexao


class ClienteService:

    def __init__(self, cliente: Cliente = None):
        self.cliente = cliente

    # ---------------- Funções de interação com o banco ------------------#
    def cadastra(self):
        # hash senha, usar--> check_password(password, encoded) para checar no login
        self.cliente.senha = make_password(self.cliente.senha)
        # insere cliente
        cliente_dict = self.cliente.__dict__
        insert_result = dbClientes.insert_one(cliente_dict)
        return insert_result.acknowledged

    def busca(self, id = None):
        """Consulta clientes"""
        if(id == None):
            return dbClientes.find(projection={'_id': False})
        else:
            return dbClientes.find({'id': id},projection={'_id': False})

    def atualiza(self):
        """Update clientes"""
        pass

    def deleta(self):
        """Deleta clientes"""
        pass

    def celular_existe(self):
        celular = self.cliente.celular
        return dbClientes.count_documents({"celular": celular})

    # -------------------- Funções de organização de dados ------------------------#
    def agrupa_clientes_by_municipio_id(self, all_clientes):
        clientes_by_municipio_id = {}
        for cliente in all_clientes:
            key = cliente['municipio_id']
            cliente_dados = {'nome': cliente['nome'], 
                            'ddi': cliente['ddi'],
                            'ddd': cliente['ddd'],
                            'celular': cliente['celular'],
                            'estado_id': cliente['estado_id']
                            }
            if  key in clientes_by_municipio_id.keys():
                clientes_by_municipio_id[cliente['municipio_id']].append(cliente_dados)
            else:
                clientes_by_municipio_id[cliente['municipio_id']] = [cliente_dados]
        return clientes_by_municipio_id