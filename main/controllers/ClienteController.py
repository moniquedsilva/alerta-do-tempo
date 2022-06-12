import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from main.models.Cliente import Cliente
from main.services.ClienteService import ClienteService
from main.services.EstadosService import EstadosService
from main.services.MunicipiosService import MunicipiosService
from main.validators.ClienteValidator import ClienteValidator


class ClienteController(View):

    def get(self, request):
        '''
        Cadastra um usuário no sistema.
        :param request: requisão HTTP GET.
        :return: render(request, 'cadastro.html', {'estados': estados})
        '''
        estados_service = EstadosService()
        estados = estados_service.busca_siglas_estados()
        return render(request, 'cadastro.html', {'estados': estados})

    def post(self, request):
        '''
        Recebe a requisição e encaminha para serem cadastradas
        :param request: requisão HTTP POST.
        :param path_name: loadCidadesByEstado or cadastrar.
        :return: Direciona para loadCidadesByEstado se path_name for 'loadCidadesByEstado' ou cadastrar se path_name for 'cadastrar'.
        '''
        path_name = request.resolver_match.url_name
        if(path_name == 'loadCidadesByEstado'):
            return self.loadCidadesByEstado(request)
        if(path_name == 'cadastrar'):
            return self.cadastra(request)

    def cadastra(self, request):
        '''
        Cadastra novo usuario
        :param request: requisão HTTP POST.
        :param nome: string.
        :param ddi: string.
        :param ddd: string.
        :param celular: string.
        :param senha: string.
        :param municipio_id: string.
        :param estado_id: string.
        :return: JsonResponse com status.
        '''
        nome = request.POST['nome']
        ddi = request.POST['ddi']
        ddd = request.POST['ddd']
        celular = request.POST['celular']
        senha = request.POST['senha']
        municipio_id = request.POST['municipio']
        estado_id = request.POST['estado']

        # Cria uma instância de Cliente
        cliente = Cliente(nome, ddi, ddd, celular,
                          senha, municipio_id, estado_id)
        # Cria serviço
        cliente_service = ClienteService(cliente)
        estados_service = EstadosService()
        municipios_service = MunicipiosService()

        # Validação
        cliente_validator = ClienteValidator(
            cliente, cliente_service, estados_service, municipios_service)
        resposta_validacao = cliente_validator.valida()
        if(not resposta_validacao['status']):
            return JsonResponse(resposta_validacao)

        # Cadastro
        if(not cliente_service.cadastra()):
            return JsonResponse({"status": False, 'msg': "Erro de cadastro, por favor tente mais tarde!"})

        # Se tudo ok, retorna mensagem de sucesso
        return JsonResponse({"status": True, 'msg': "Cadastro realizado com sucesso!"})

    def loadCidadesByEstado(self, request):
        '''
        Carrega drop-down de cidades
        :param request: requisão HTTP POST.
        :param estado_id: string.
        :return: JsonResponse({'municipios': municipios_json})
        '''
        estado_id = request.POST['estado_id']
        municipios_service = MunicipiosService()
        municipios = municipios_service.busca_cidades_by_estado(
            {"estado_id": estado_id})
        municipios_json = [{m['id']: m['nome']} for m in municipios]

        return JsonResponse({'municipios': municipios_json})
