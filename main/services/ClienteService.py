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

    def busca(self, celular = None):
        if(celular == None):
            return dbClientes.find(projection={'_id': False})
        else:    
            return dbClientes.find_one({'celular':  celular}, projection={'_id': False})

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