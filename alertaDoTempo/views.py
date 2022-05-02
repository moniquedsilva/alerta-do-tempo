from django.http import HttpResponse, JsonResponse
from alertaDoTempo.utils import collection
from django.template import loader
from django.shortcuts import render


def index(request):
    return render(request,'alertaDoTempo/index.html')

def cadastro(request):
    
    cliente = {
        "celular" : request.POST['celular'],
        "nome" : request.POST['nome'],
        "senha" : request.POST['senha'],
        "estado": request.POST['estado'],
        "municipio" : request.POST['municipio']
    }
    insert_result = collection.insert_one(cliente)
    resultado = {"sucesso": insert_result.acknowledged}

    return JsonResponse(resultado)



