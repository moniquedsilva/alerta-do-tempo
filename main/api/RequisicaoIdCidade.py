from main.api.RequisicoesAPI import RequisicoesAPI
from main.models.Requisicao import Cidade
import xml.etree.ElementTree as ET
import logging

class RequisicaoIdCidade(RequisicoesAPI):

    def __init__(self, url):
        super().__init__(url)
    
    def trata_dados(self) -> bool:
        root = ET.fromstring(self.data)
        lista = []
        #Parei aqui, verificar quando elemento retorna vazio
        possui_data = False
        for elem in root:
            possui_data = True
            for el in elem:
                if el.tag == "nome": nome = el.text
                if el.tag == "uf": uf = el.text
                if el.tag == "id": id = el.text
            c = Cidade(nome, uf, id)
            lista.append(c)
        self.data_object_list = lista
            
        return possui_data

    def find_id_cidade(self, cidade: str, sigla_estado: str) -> str:
        id = None
        cidade = cidade.replace('-', ' ')
        cidade = cidade.replace('\'', '')
        for c in self.data_object_list:
            if(c.nome == cidade and c.uf == sigla_estado): 
                id = c.id
                break
        
        return id