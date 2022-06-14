
from main.api.RequisicoesAPI import RequisicoesAPI
import xml.etree.ElementTree as ET

from main.models.Requisicao import Ondas, OndasInfo

class RequisicaoOndas(RequisicoesAPI):

    def __init__(self, url):
        super().__init__(url)
    
    def trata_dados(self) -> bool:
        root = ET.fromstring(self.data)
        possui_data = False
        for elem in root:
            possui_data = True
            if elem.tag == "nome": nome = elem.text
            if elem.tag == "uf": uf = elem.text
            if elem.tag == "atualizacao": atualizacao = elem.text
            if elem.tag == "manha" or elem.tag == "tarde" or elem.tag == "noite":
                for e in elem:
                    if e.tag == "dia": dia = e.text
                    if e.tag == "agitacao": agitacao = e.text
                    if e.tag == "altura": altura = e.text
                    if e.tag == "direcao": direcao = e.text
                    if e.tag == "vento": vento = e.text
                    if e.tag == "vento_dir": vento_dir = e.text
                if elem.tag == "manha": manha = OndasInfo(dia, agitacao, altura, direcao, vento, vento_dir)
                if elem.tag == "tarde": tarde = OndasInfo(dia, agitacao, altura, direcao, vento, vento_dir)
                if elem.tag == "noite": noite = OndasInfo(dia, agitacao, altura, direcao, vento, vento_dir)
        self.pv_ondas = Ondas(nome, uf, atualizacao, manha, tarde, noite)
        return possui_data