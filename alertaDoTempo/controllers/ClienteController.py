from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from alertaDoTempo.services.ClienteService import ClienteService

#Página Inicial
def index(request):
    return render(request,'alertaDoTempo/index.html')

#Cadastro via POST
def cadastra(request):

    #Recebe dados
    nome = request.POST['nome']
    celular = request.POST['celular']
    password = request.POST['senha']
    estado = request.POST['estado']
    municipio = request.POST['municipio']

    #Cria um objeto do tipo ClienteService
    cliente = ClienteService(nome, celular, password, municipio, estado)

    resultado = cliente.cadastra()
    response = {"sucesso": resultado}


    return JsonResponse(response)

