
from main.api.RequisicoesAPI import RequisicoesAPI
import xml.etree.ElementTree as ET

from main.models.Requisicao import Ondas, OndasInfo

class RequisicaoOndas(RequisicoesAPI):

    def __init__(self, url):
        super().__init__(url)
    
    def trata_dados(self) -> bool:
        root = ET.fromstring(self.data)
        possui_data = False
        dados = {}
        lista_previsao = []
        for elem in root:
            possui_data = True
            if elem.tag != "previsao":
                dados.update({elem.tag: elem.text})
            else:
                dados_previsao = {e.tag: e.text for e in elem}
                lista_previsao.append({elem.tag: OndasInfo(dados_previsao['dia'],
                                                        dados_previsao['agitacao'],
                                                        dados_previsao['altura'],
                                                        dados_previsao['direcao'],
                                                        dados_previsao['vento'],
                                                        dados_previsao['vento_dir'])})
                
        self.pv_ondas = Ondas(dados['nome'], 
                                dados['uf'], 
                                dados['atualizacao'], 
                                lista_previsao)
        return possui_data