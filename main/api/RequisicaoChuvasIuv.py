import logging
import xml.etree.ElementTree as ET

from main.api.RequisicoesAPI import RequisicoesAPI
from main.models.Requisicao import Previsao, PrevisaoChuvas


class RequisicaoChuvasIuv(RequisicoesAPI):

    def __init__(self, url):
        super().__init__(url)

    def trata_dados(self):
        root = ET.fromstring(self.data)
        ListaPrevisao = []
        possui_data = False
        for elem in root:
            possui_data = True
            if elem.tag == "nome":
                nome = elem.text
            if elem.tag == "uf":
                uf = elem.text
            if elem.tag == "atualizacao":
                atualizacao = elem.text
            if elem.tag == "previsao":
                for e in elem:
                    if e.tag == "dia":
                        dia = e.text
                    if e.tag == "tempo":
                        tempo = e.text
                    if e.tag == "maxima":
                        maxima = e.text
                    if e.tag == "minima":
                        minima = e.text
                    if e.tag == "iuv":
                        iuv = e.text
                p = Previsao(dia, tempo, maxima, minima, iuv)
                ListaPrevisao.append(p)
        self.pv_chuvas_iuv = PrevisaoChuvas(
            nome, uf, atualizacao, ListaPrevisao)

        return possui_data
