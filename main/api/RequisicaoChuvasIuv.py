import xml.etree.ElementTree as ET

from main.api.RequisicoesAPI import RequisicoesAPI
from main.models.Requisicao import Previsao, PrevisaoChuvas


class RequisicaoChuvasIuv(RequisicoesAPI):

    def __init__(self, url):
        super().__init__(url)

    def trata_dados(self):
        root = ET.fromstring(self.data)
        dados = {}
        lista_previsao = []
        possui_data = False
        for elem in root:
            possui_data = True
            if(elem.tag != "previsao"):
                dados.update({elem.tag: elem.text})
            else:
                dados_previsao = {e.tag: e.text for e in elem}
              
                p = Previsao(dados_previsao['dia'], 
                                dados_previsao['tempo'], 
                                dados_previsao['maxima'], 
                                dados_previsao['minima'], 
                                dados_previsao['iuv'])
                lista_previsao.append(p)
        
        self.pv_chuvas_iuv = PrevisaoChuvas(
            dados['nome'], dados['uf'], dados['atualizacao'], lista_previsao)

        return possui_data
