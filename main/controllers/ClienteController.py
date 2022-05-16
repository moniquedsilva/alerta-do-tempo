import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from main.services.MunicipiosService import MunicipiosService
from main.services.ClienteService import ClienteService
from django.views import View

class ClienteController(View):

    def get(self, request, *args, **kwargs):
        estados = MunicipiosService.buscaSiglasEstados()
        estados_formatados = []
        for e in estados:
            estados_formatados.append({'id': str(e['_id']), 'sigla': e['sigla']})
        return render(request,'cliente/index.html', {'estados': estados_formatados})
    
    #Cadastro via POST
    def cadastra(request):

        #Recebe dados
        nome = request.POST['nome']
        celular = request.POST['celular']
        senha = request.POST['senha']
        estado = request.POST['estado']
        municipio = request.POST['municipio']

        #Cria um objeto do tipo ClienteService
        cliente = ClienteService(nome, celular, senha, municipio, estado)

        resultado = cliente.cadastra()
        response = {"sucesso": resultado}

        return JsonResponse(response)

    @csrf_exempt
    def loadCidadesByEstado(request):
        dadosString = str(request.body, 'utf-8')
        dadosJson = json.loads(dadosString)
        municipios = MunicipiosService.buscaCidadesByEstado(dadosJson)
        municipiosDict = {}
        for m in municipios:
            municipiosDict.update({str(m['_id']): m['nome']})
            
        return JsonResponse(municipiosDict)


