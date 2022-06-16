from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from main.controllers.RequisicoesController import RequisicoesController
from main.services.ClienteService import ClienteService
from main.services.MunicipiosService import MunicipiosService
from main.services.EstadosService import EstadosService
from main.services.CondicoesTempoService import CondicoesTempoService
import json

class DashboardController(View):

    def get(self, request):
        '''
        Renderiza a dashboard.
        :param request: requisão HTTP GET.
        :return: render(request, 'dashboard.html').
        '''
        if not self.esta_logado(request):
            return HttpResponse('Não logado!')
        
        return render(request, 'dashboard.html')
    

    def post(self, request):
        
        if not self.esta_logado(request):
            return HttpResponse('Não logado!')

        path_name = request.resolver_match.url_name
        if(path_name == 'loadPrevisao'):
            return self.loadPrevisao(request)
    
    def loadPrevisao(self, request):
        
        #Retorna dados do banco
        celular = request.session['_auth_user_id']
        cliente_service = ClienteService()
        cliente = cliente_service.busca(celular)

        municipio_service = MunicipiosService()
        municipio = municipio_service.busca_municipio_by_id(cliente['municipio_id'])

        estado_service = EstadosService()
        estado = estado_service.busca_estado_by_id(cliente['estado_id'])

        #--- Faz array com dados do usuário

        if(municipio['litoranea'] == "sim"): litoraneo = True
        else: litoraneo = False

        usuario = {'nome': cliente['nome'],
                    'municipio': municipio['nome'],
                    'municipio-litoraneo': litoraneo,
                    'estado': estado['nome'],
                    'estado-sigla': estado['sigla']}

        #----Busca Id da cidade do cliente
        
        id_cidade = RequisicoesController.req_id_cidade(municipio['nome'], 
                                                        municipio['nome_formatado'], 
                                                        estado['sigla'])
        msg_falha = 'Falha na Requisição. Por favor, tente novamente mais tarde'
        if(id_cidade == None): return JsonResponse({'status': False,
                                                    'msg': msg_falha})
        
        #----Busca dados de chuva e iuv-----
        chuvas_iuv = RequisicoesController.req_chuvas_iuv(id_cidade)
        if chuvas_iuv != None:
            #organiza
            chuvas_iuv_dict = vars(chuvas_iuv)
            lista_previsao_dict = [vars(l) for l in chuvas_iuv.lista_previsao]
            chuvas_iuv_dict['lista_previsao'] = lista_previsao_dict

            #Busca descrição das condições do tempo
            condicoes_tempo_service = CondicoesTempoService()
            condicoes_tempo = condicoes_tempo_service.busca()

            #Adiciona descrição aos dados de chuva
            for chave in range(len(chuvas_iuv_dict['lista_previsao'])):
                tempo_sigla = chuvas_iuv_dict['lista_previsao'][chave]['tempo']
                for condicao in condicoes_tempo:
                    if(condicao['sigla'] == tempo_sigla):
                        chuvas_iuv_dict['lista_previsao'][chave].update({'tempo_descricao': condicao['descricao'],
                                                                        'categoria': condicao['categoria']})
                        condicoes_tempo.rewind()
                        break
        
        #Ondas
        if municipio['litoranea'] == 'nao':
            ondas = None
        else:
            #Pode retornar nulo, caso haja erro
            ondas = RequisicoesController.req_ondas(id_cidade)
            #organiza
            ondas_dict = vars(ondas)
            ondas_dict['manha'] = vars(ondas_dict['manha'])
            ondas_dict['tarde'] = vars(ondas_dict['tarde'])
            ondas_dict['noite'] = vars(ondas_dict['noite'])
        
        
        return JsonResponse({'status': True,
                                'chuvas_iuv': chuvas_iuv_dict, 
                                'ondas': ondas_dict,
                                'usuario': usuario})

    def esta_logado(self, request):
        if "_auth_user_id" not in request.session:
            return False
        return True