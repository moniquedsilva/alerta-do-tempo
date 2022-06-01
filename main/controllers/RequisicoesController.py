import logging
import urllib.parse
from django.views import View
from django.shortcuts import render
from datetime import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from main.models.Requisicao import Ondas, PrevisaoChuvas
from main.services.ClienteService import ClienteService, status_conexao
from main.services.MunicipiosService import MunicipiosService
from main.services.EstadosService import EstadosService
from main.api.RequisicaoIdCidade import RequisicaoIdCidade
from main.api.RequisicaoChuvasIuv import RequisicaoChuvasIuv
from main.api.RequisicaoOndas import RequisicaoOndas


class RequisicoesController(View):

    def get(self, request):
        #cria logfile
        self.cria_log_file()
        logging.debug("Arquivo log criado.\n")
        print("teste")
        #init requisições
        self.init_requisicoes()


        log_data = self.ler_log_file()
        return render(request, 'requisicao_log.html', {'log_data': log_data}, content_type='text/plain')

    def cria_log_file(self):
        #Pega data de agora
        data_hora_agora = datetime.now()
        data_hora_agora_formatada = data_hora_agora.strftime("%d-%m-%Y_%H-%M-%S")
        #coloca data no nome do logfile
        filename_log = "main/logs/requisicao_" + data_hora_agora_formatada + ".log"
        self.path_log_file = default_storage.save(filename_log, 
                                                ContentFile("Log Requisição - " + data_hora_agora_formatada + "\n")) 
        #cria log file
        logging.basicConfig(filename=self.path_log_file,
                            format='%(asctime)s - %(levelname)s:%(message)s', 
                            datefmt='%d/%m/%Y %I:%M:%S %p',
                            level=logging.DEBUG)
        return
    
    def ler_log_file(self):
        with open(self.path_log_file, encoding="utf-8") as f:
            data = f.read()
        return data
    
    def init_requisicoes(self):
        
        #Passo 1 - Busca todos os clientes no banco agrupado por cidade
        #Passo 2 - Para cada cidade distinta
            # Faz requisição para buscar id da cidade na api da INPE
            # Se id encontrado, faz requisições de chuvas e iuv (são juntas)
            # Se cidade litoranea, faz requisicoes de ondas
            # Se houver alguma condição perigosa para essa cidade envia sms para clientes
            # Retorna ao passo 2 para a próxima cidade
        
        #Passo 1 - Busca todos os clientes e formata dados
        cliente_service = ClienteService()

        #se conexão com banco falhar retorna erro
        if(not status_conexao):
            logging.error("Erro de conexão com o banco de dados!")
            return
        
        todos_clientes = cliente_service.busca()
        clientes_by_municipio_id = cliente_service.agrupa_clientes_by_municipio_id(todos_clientes)
        logging.info("Dados dos clientes resgatados do banco")

        municipios_service = MunicipiosService()
        estados_service = EstadosService()

        #Passo 2
        logging.info(str(len(clientes_by_municipio_id)) + " municípios distintos encontrados\n" )
        for key_municipio_id in clientes_by_municipio_id:
            municipio = municipios_service.busca_municipio_by_id(key_municipio_id)
            estado = estados_service.busca_estado_by_id(municipio['estado_id'])
            logging.debug("\nFazendo requisições para " + municipio['nome'] + " - " + estado['sigla'])
            
            nome_cidade_formatado = urllib.parse.quote(municipio['nome_formatado'])
            
            resposta = self.executa_requisicoes(municipio['nome'], 
                                                    nome_cidade_formatado, 
                                                    municipio['litoranea'], 
                                                    estado['sigla'])
            
            if(resposta == None):
                logging.warning("Falha na Requisição\n")
                continue 
            
            if(resposta['chuvas_iuv'] != None): 
                logging.info("Requisições chuvas e iuv realizadas com sucesso. Verificar se há dados perigosos\n")
            if(resposta['ondas'] != None): 
                logging.info("Requisições ondas realizada com sucesso. Verificar se há dados perigosos\n")
        
        return
        

    def executa_requisicoes(self, nome_cidade, nome_cidade_formatado, cidade_litoranea, estado_sigla) -> dict:
    
        resposta = dict() 

        #Busca id da cidade na api INPE
        id_cidade = self.req_id_cidade(nome_cidade, nome_cidade_formatado, estado_sigla)
        if(id_cidade == None): return None
        resposta['id_cidade'] = id_cidade

        #Chuvas e Iuv
        chuvas_iuv = self.req_chuvas_iuv(id_cidade)
        if(chuvas_iuv == None):
            resposta['chuvas_iuv'] = None
        else:
            resposta['chuvas_iuv'] = chuvas_iuv

        #Ondas
        if(not cidade_litoranea): 
            resposta['ondas'] = None
            logging.info("Cidade não é litorânea, não é necessário requisição de ondas.")
            return resposta
        
        ondas = self.req_ondas(id_cidade)
        if(ondas == None): 
            resposta['ondas'] = None
            return resposta
        
        resposta['ondas'] = ondas
        
        return resposta
    
    def req_id_cidade(self, cidade, nome_cidade_formatado, sigla_estado) -> str:
        """Requsição do id cidade na api da INPE"""
        url_find_id = "http://servicos.cptec.inpe.br/XML/listaCidades?city=" + nome_cidade_formatado
        req_id_cidade = RequisicaoIdCidade(url_find_id)
        # requisita dados da api
        if(not req_id_cidade.executa_requisicao()): return None
        logging.info("Requisição do id cidade realizada")

        #requisição ok, transforma dados em objeto
        if(not req_id_cidade.trata_dados()): 
            logging.error("Dados vazios retornados pela requisicao de url: " + url_find_id)
            return None
        logging.info("Dados tratados")
        
        #procura match com id da cidade desejada
        id_cidade = req_id_cidade.find_id_cidade(cidade, sigla_estado)    
        if(id_cidade == None): 
            logging.error("Dentre dados retornados, cidade não encontrada") 
            return None 
        logging.info("Id da cidade encontrado")

        return id_cidade
    
    def req_chuvas_iuv(self, id_cidade) -> PrevisaoChuvas :
        """ Realiza requisição e tratamento dos dados de chuvas e iuv"""
        #Se id ok, faz requisição dos dados da cidade
        url_chuvas_iuv = "http://servicos.cptec.inpe.br/XML/cidade/" + id_cidade + "/previsao.xml"
        req_chuvas_iuv = RequisicaoChuvasIuv(url_chuvas_iuv)
        if(not req_chuvas_iuv.executa_requisicao()): return None
        logging.info("Requisição de chuvas e iuv realizada")
        #Checa se há dado na requisição e converte para objeto
        if(not req_chuvas_iuv.trata_dados()): 
            logging.error("Dados retornados estão vazios, requisicao de url: " + url_chuvas_iuv)
            return None
        logging.info("Dados de chuvas/iuv transformados em objeto")

        return req_chuvas_iuv.pv_chuvas_iuv
    
    def req_ondas(self, id_cidade) -> Ondas:
        """ Realiza requisição e tratamento dos dados de ondas"""
        url_ondas = "http://servicos.cptec.inpe.br/XML/cidade/" + id_cidade + "/dia/0/ondas.xml"
        req_ondas = RequisicaoOndas(url_ondas)
        if(not req_ondas.executa_requisicao()): return None
        logging.info("Requisição de ondas realizada")
        
        if(not req_ondas.trata_dados()): 
            logging.error("Dados retornados estão vazios, requisicao de url: " + url_ondas)
            return None
        logging.info("Dados de ondas transformado em objetos")

        return req_ondas.pv_ondas



    
        