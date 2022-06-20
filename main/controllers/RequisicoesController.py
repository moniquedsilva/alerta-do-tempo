import datetime as dt
import logging
import math
import string
import urllib.parse
from datetime import datetime
from typing import Union

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views import View

from main.api.RequisicaoChuvasIuv import RequisicaoChuvasIuv
from main.api.RequisicaoIdCidade import RequisicaoIdCidade
from main.api.RequisicaoOndas import RequisicaoOndas
from main.models.Requisicao import Ondas, PrevisaoChuvas
from main.services.ClienteService import ClienteService, status_conexao
from main.services.CondicoesTempoService import CondicoesTempoService
from main.services.EstadosService import EstadosService
from main.services.MunicipiosService import MunicipiosService


class RequisicoesController(View):

    def get(self, request):
        # cria logfile
        self.cria_log_file()
        logging.debug("Arquivo log criado.\n")
        # init requisições
        self.init_requisicoes()

        log_data = self.ler_log_file()
        return render(request, 'requisicao_log.html', {'log_data': log_data}, content_type='text/plain')

    def cria_log_file(self):
        # Pega data de agora
        data_hora_agora = datetime.now()
        data_hora_agora_formatada = data_hora_agora.strftime(
            "%d-%m-%Y_%H-%M-%S")
        # coloca data no nome do logfile
        filename_log = "main/logs/requisicao_" + data_hora_agora_formatada + ".log"
        self.path_log_file = default_storage.save(filename_log,
                                                  ContentFile("Log Requisição - " + data_hora_agora_formatada + "\n"))
        # sobrescreve log file
        logging.basicConfig(filename=self.path_log_file,
                            format='%(asctime)s - %(levelname)s:%(message)s',
                            datefmt='%d/%m/%Y %I:%M:%S %p',
                            level=logging.DEBUG)

    def ler_log_file(self):
        with open(self.path_log_file, encoding="utf-8") as f:
            data = f.read()
        return data

    def init_requisicoes(self):

        # Passo 1 - Busca todos os clientes no banco agrupado por cidade
        # Passo 2 - Para cada cidade distinta
        # Faz requisição para buscar id da cidade na api da INPE
        # Se id encontrado, faz requisições de chuvas e iuv (são juntas)
        # Se cidade litoranea, faz requisicoes de ondas
        # Se houver alguma condição perigosa para essa cidade envia sms para clientes
        # Retorna ao passo 2 para a próxima cidade

        # Passo 1 - Busca todos os clientes e formata dados
        cliente_service = ClienteService()
        municipios_service = MunicipiosService()
        estados_service = EstadosService()
        condicoes_tempo_service = CondicoesTempoService()

        # se conexão com banco falhar retorna erro
        if(not status_conexao):
            logging.error("Erro de conexão com o banco de dados!")
            return

        todos_clientes = cliente_service.busca()
        clientes_by_municipio_id = cliente_service.agrupa_clientes_by_municipio_id(
            todos_clientes)
        logging.info("Dados dos clientes resgatados do banco")

        # Passo 2
        logging.info(str(len(clientes_by_municipio_id)) +
                     " municípios distintos encontrados\n")
        for key_municipio_id in clientes_by_municipio_id:
            # Consulta e organiza dados
            municipio = municipios_service.busca_municipio_by_id(
                key_municipio_id)
            estado = estados_service.busca_estado_by_id(municipio['estado_id'])
            logging.debug("Fazendo requisições para " +
                          municipio['nome'] + " - " + estado['sigla'])

            nome_cidade_formatado = urllib.parse.quote(
                municipio['nome_formatado'])

            # Requisições para api
            resposta = self.executa_requisicoes(municipio['nome'],
                                                nome_cidade_formatado,
                                                municipio['litoranea'],
                                                estado['sigla'])

            if(resposta == None):
                logging.warning("Falha na Requisição\n")
                continue

            logging.info("--------Verifica se há dados perigosos-------")
            # Verificação se dados são perigosos
            condicoes_tempo = condicoes_tempo_service.busca()
            resposta = self.verifica_condicoes_perigosas(resposta['chuvas_iuv'],
                                                         resposta['ondas'],
                                                         condicoes_tempo)

            clientes = clientes_by_municipio_id[key_municipio_id]
            # Decide quais alertas à serem enviados
            logging.info("--------SMS-------")
            self.verifica_dados_sms(resposta, clientes)

            logging.debug("\n")

    def executa_requisicoes(self, nome_cidade, nome_cidade_formatado, cidade_litoranea, estado_sigla) -> Union[dict, None]:

        resposta = dict()

        # Busca id da cidade na api INPE
        logging.info("--------Buscando Id da cidade-------")
        id_cidade = RequisicoesController.req_id_cidade(
            nome_cidade, nome_cidade_formatado, estado_sigla)
        if(id_cidade == None):
            return None
        resposta['id_cidade'] = id_cidade

        # Chuvas e Iuv
        logging.info("--------Buscando dados de chuvas e iuv-------")
        chuvas_iuv = RequisicoesController.req_chuvas_iuv(id_cidade)
        if(chuvas_iuv == None):
            resposta['chuvas_iuv'] = None
        else:
            resposta['chuvas_iuv'] = chuvas_iuv

        # Ondas
        logging.info("--------Buscando dados de ondas-------")
        if(cidade_litoranea == 'nao'):
            resposta['ondas'] = None
            logging.info(
                "Cidade não é litorânea, não é necessário requisição de ondas.")
            return resposta

        ondas = RequisicoesController.req_ondas(id_cidade)
        if(ondas == None):
            resposta['ondas'] = None
            return resposta

        resposta['ondas'] = ondas

        return resposta

    @classmethod
    def req_id_cidade(cls, cidade, nome_cidade_formatado, sigla_estado) -> Union[str, None]:
        """Requsição do id cidade na api da INPE"""
        url_find_id = "http://servicos.cptec.inpe.br/XML/listaCidades?city=" + \
            nome_cidade_formatado
        req_id_cidade = RequisicaoIdCidade(url_find_id)
        # requisita dados da api
        if(not req_id_cidade.executa_requisicao()):
            return None
        logging.info("Requisição do id cidade realizada")

        # requisição ok, transforma dados em objeto
        if(not req_id_cidade.trata_dados()):
            logging.error(
                "Dados vazios retornados pela requisicao de url: " + url_find_id)
            return None
        logging.info("Dados tratados")

        # procura match com id da cidade desejada
        id_cidade = req_id_cidade.find_id_cidade(cidade, sigla_estado)
        if(id_cidade == None):
            logging.error("Dentre dados retornados, cidade não encontrada")
            return None
        logging.info("Id da cidade encontrado")

        return id_cidade

    @classmethod
    def req_chuvas_iuv(cls, id_cidade) -> PrevisaoChuvas:
        """ Realiza requisição e tratamento dos dados de chuvas e iuv"""
        # Se id ok, faz requisição dos dados da cidade
        url_chuvas_iuv = "http://servicos.cptec.inpe.br/XML/cidade/" + \
            id_cidade + "/previsao.xml"
        req_chuvas_iuv = RequisicaoChuvasIuv(url_chuvas_iuv)
        if(not req_chuvas_iuv.executa_requisicao()):
            return None
        logging.info("Requisição de chuvas e iuv realizada")
        # Checa se há dado na requisição e converte para objeto
        if(not req_chuvas_iuv.trata_dados()):
            logging.error(
                "Dados retornados estão vazios, requisicao de url: " + url_chuvas_iuv)
            return None
        logging.info("Dados de chuvas/iuv transformados em objeto")

        return req_chuvas_iuv.pv_chuvas_iuv

    @classmethod
    def req_ondas(cls, id_cidade) -> Ondas:
        """ Realiza requisição e tratamento dos dados de ondas"""
        url_ondas = "http://servicos.cptec.inpe.br/XML/cidade/" + \
            id_cidade + "/dia/1/ondas.xml"
        req_ondas = RequisicaoOndas(url_ondas)
        if(not req_ondas.executa_requisicao()):
            return None
        logging.info("Requisição de ondas realizada")

        if(not req_ondas.trata_dados()):
            logging.error(
                "Dados retornados estão vazios, requisicao de url: " + url_ondas)
            return None
        logging.info("Dados de ondas transformado em objetos")

        return req_ondas.pv_ondas

    def verifica_condicoes_perigosas(self, chuvas_iuv, ondas, condicoes_tempo) -> dict:

        resposta = {}
        resposta['chuvas'] = None
        resposta['iuv'] = None
        resposta['ondas'] = None

        """ Cada uma dessas três posições do dicionário resposta pode conter os seguintes conteúdos:
            None -> Indica existência de algum erro, falta de dado, data não congruente. Ver log
                    para ter uma noção melhor
            Dicionário -> com posição 'envia_sms', se 'envia_sms' for verdadeiro existe também a posição
                            'descricao_condição_perigosa com informações sobre a previsão', caso
                            'envia_sms' for falso não há descrição
            """

        if(self.existe_dados(chuvas_iuv)):
            resposta['chuvas'] = self.verifica_chuvas(
                chuvas_iuv, condicoes_tempo)
            resposta['iuv'] = self.verifica_iuv(chuvas_iuv)
        else:
            logging.warning(
                "Não há dados de chuvas nem iuv, não é possível verificar se são perigosos!")

        if(self.existe_dados(ondas)):
            resposta['ondas'] = self.verifica_ondas(ondas)
        else:
            resposta['ondas'] = {'manha': None, 'tarde': None, 'noite': None}
            logging.info(
                "Não há dados de ondas, não é possível verificar se são perigosos")

        return resposta

    def verifica_chuvas(self, chuvas_iuv, condicoes_tempo) -> Union[dict, None]:

        # Pega apenas previsão do primeiro dia(pode ser o dia de hoje, ou pode ser o dia de amanhã)
        previsao = chuvas_iuv.lista_previsao[0]

        # Checa se data da previsão é igual a de hoje
        """Provavelmente o scheduler terá de disparar a função no periodo da manhã
        pois a api, a partir de um certo momento do dia muda a data da primeiro previsão fornecida,
        por exemplo: consultando a api pela manhã ela fornece a previsão a partir desse mesmo dia, mas
        consultando a api no período da tarde/noite ela fornece as previsões a partir do dia seguinte
        """
        resposta = {}
        resposta['tipo'] = 'chuvas'
        if(not self.verifica_data(previsao.dia)):
            logging.info(
                "Não foi encontrada previsão de chuvas para o dia de amanhã. Previsão mais próxima para: " + previsao.dia)
            return None

        descricao = ''
        for condicao in condicoes_tempo:
            if(previsao.tempo == condicao['sigla']):
                descricao = condicao['descricao']
                if(condicao['perigoso'] == "sim"):
                    logging.info("Condição perigosa de chuvas encontrada: " +
                                 condicao['descricao'])
                    resposta['envia_sms'] = True
                    resposta['descricao_condicao_perigosa'] = condicao['descricao']
                    return resposta

        logging.info(
            "Nenhuma condição perigosa de chuvas encontrada. Previsão: " + descricao)
        resposta['envia_sms'] = False
        return resposta

    def verifica_iuv(self, chuvas_iuv):

        # 1 a 2 - baixo, 3 a 5 - moderado, 6 a 7 - alto
        # 8 a 10 - muito alto, a partir de 11 - extremo
        CONDICAO_ALTA_IUV = 6
        CONDICAO_MUITO_ALTA_IUV = 8
        CONDICAO_EXTREMA_IUV = 11

        # Pega apenas previsão do primeiro dia(pode o dia de hoje, ou pode ser o dia de amanhã)
        previsao = chuvas_iuv.lista_previsao[0]

        # checa data
        if(not self.verifica_data(previsao.dia)):
            logging.info(
                "Não foi encontrada previsão de iuv para o dia de amanhã. Previsão mais próxima para: " + previsao.dia)
            return None

        msg = ""
        resposta = {}
        resposta['tipo'] = 'iuv'

        previsao_iuv = math.floor(float(previsao.iuv))
        if(previsao_iuv >= CONDICAO_ALTA_IUV and previsao_iuv < CONDICAO_MUITO_ALTA_IUV):
            msg = "Previsão de índice ultra-violeta alto nesta área. iuv: " + previsao.iuv
        elif(previsao_iuv >= CONDICAO_MUITO_ALTA_IUV and previsao_iuv < CONDICAO_EXTREMA_IUV):
            msg = "Previsão de índice ultra-violeta muito alto nesta área. iuv: " + previsao.iuv
        elif(previsao_iuv >= CONDICAO_EXTREMA_IUV):
            msg = "Previsão de índice ultra-violeta extremo nesta área. iuv: " + previsao.iuv
        else:
            resposta['envia_sms'] = False
            logging.info(
                "Nenhuma previsão perigosa de índices ultra-violeta. iuv: " + previsao.iuv)
            return resposta

        logging.info(msg)
        resposta['envia_sms'] = True
        resposta['descricao_condicao_perigosa'] = msg
        return resposta

    def verifica_ondas(self, ondas):

        resposta = {}
        resposta['manha'] = self.verifica_ondas_turno(ondas.manha, 'manha')
        resposta['tarde'] = self.verifica_ondas_turno(ondas.tarde, 'tarde')
        resposta['noite'] = self.verifica_ondas_turno(ondas.noite, 'noite')

        return resposta

    def verifica_ondas_turno(self, ondas, turno):

        logging.info("Verificando perigo de ondas. Turno: " + turno)
        data_previsao = str.split(ondas.dia, ' ')[0]
        data_previsao_formatada = dt.datetime.strptime(
            data_previsao, "%d-%m-%Y").strftime("%Y-%m-%d")
        if(not self.verifica_data(data_previsao_formatada)):
            logging.info("A previsão de ondas não corresponde a data de amanhã." +
                         "Previsão para: " + data_previsao_formatada)
            return None

        resposta = {}
        resposta['tipo'] = 'ondas ' + turno
        if(ondas.agitacao == "Fraco" or ondas.agitacao == "Moderado"):
            logging.info(
                "Sem necessidade de enviar alerta, mar: " + ondas.agitacao)
            resposta['envia_sms'] = False
        elif(ondas.agitacao == "Forte"):
            logging.info(
                "Condição perigosa de ondas encontrada, mar: " + ondas.agitacao)
            resposta['envia_sms'] = True
            resposta['descricao_condicao_perigosa'] = ondas.agitacao
        else:
            logging.warning(
                "Não foi possível detectar previsão da agitação das ondas")
            resposta['envia_sms'] = False

        return resposta

    def verifica_dados_sms(self, dados, clientes):

        dict_sms = {}
        dict_sms = self.buffer_sms(dados['chuvas'], 'chuvas', dict_sms)
        dict_sms = self.buffer_sms(dados['iuv'], 'iuv', dict_sms)
        dict_sms = self.buffer_sms(
            dados['ondas']['manha'], 'ondas-manha', dict_sms)
        dict_sms = self.buffer_sms(
            dados['ondas']['tarde'], 'ondas-tarde', dict_sms)
        dict_sms = self.buffer_sms(
            dados['ondas']['noite'], 'ondas-noite', dict_sms)

        if(len(dict_sms) > 0):
            for d in dict_sms:
                logging.info("Iniciando envio de alerta sms: " + d)
            self.envia_sms(clientes, dict_sms)


    def buffer_sms(self, dado, tipo, dict_sms):
        if(dado != None):
            dict_sms = self.checa_se_envia_sms(dict_sms, dado, tipo)
        else:
            logging.info("Dados de " + tipo +
                         " não obtidos, não haverá envio de sms")

        return dict_sms

    def checa_se_envia_sms(self, dict_sms: dict, dados, tipo):
        if(dados['envia_sms']):
            dict_sms.update({tipo: dados['descricao_condicao_perigosa']})
        else:
            logging.info("Sem necessidade de envio de sms: " + dados['tipo'])

        return dict_sms

    def existe_dados(self, dados):
        if(dados == None):
            return False
        return True

    def verifica_data(self, dia):
        data_hora_amanha = datetime.now() - dt.timedelta(hours=3) + dt.timedelta(days=1)
        data_amanha_formatada = data_hora_amanha.strftime("%Y-%m-%d")
        if(dia != data_amanha_formatada):
            return False
        return True

    def envia_sms(self, clientes, dict_sms):
        print(clientes)
        print(dict_sms)
        print('\n')
