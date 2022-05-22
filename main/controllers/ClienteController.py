import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from main.services.MunicipiosService import MunicipiosService
from main.services.EstadosService import EstadosService
from main.services.ClienteService import ClienteService
from django.views import View
from main.models.Cliente import Cliente
from main.validators.ClienteValidator import ClienteValidator

class ClienteController(View):

    def get(self, request, *args, **kwargs):
        estadosService = EstadosService()
        estados = estadosService.buscaSiglasEstados()
        return render(request,'cliente/index.html', {'estados': estados})
    
    #Cadastro via POST
    def cadastra(request):

        #Recebe dados
        nome = request.POST['nome']
        ddi = request.POST['ddi']
        ddd = request.POST['ddd']
        celular = request.POST['celular']
        senha = request.POST['senha']
        municipio_id = request.POST['municipio']
        estado_id = request.POST['estado']

        #Cria uma instância de Cliente
        cliente = Cliente(nome, ddi, ddd, celular, senha, municipio_id, estado_id)
        #Cria serviço
        clienteService = ClienteService(cliente)
        estadosService = EstadosService()
        municipiosService = MunicipiosService() 
        
        #Validação
        clienteValidator = ClienteValidator(cliente, clienteService, estadosService, municipiosService)
        resposta_validacao = clienteValidator.valida()
        if(not resposta_validacao['status']): return JsonResponse(resposta_validacao)

        #Cadastro
        if(not clienteService.cadastra()): return JsonResponse({"status": False, 'msg': "Erro de cadastro, por favor tente mais tarde!"})
        
        #Se tudo ok, retorna mensagem de sucesso
        return JsonResponse({"status": True, 'msg': "Cadastro realizado com sucesso!"})

    @csrf_exempt
    def loadCidadesByEstado(request):
        stringIdEstado = str(request.body, 'utf-8')
        jsonIdEstado = json.loads(stringIdEstado)
        
        municipiosService = MunicipiosService()
        municipios = municipiosService.buscaCidadesByEstado(jsonIdEstado)
        municipiosJson = [{m['id']: m['nome']} for m in municipios]

        return JsonResponse({'municipios': municipiosJson})


