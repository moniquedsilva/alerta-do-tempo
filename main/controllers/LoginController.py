from django.shortcuts import render
from django.views import View

from django.http import HttpResponse, JsonResponse
from main.services.ClienteService import ClienteService

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class LoginController(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


    def login(request):
        nome = request.POST['nome'];
        senha = request.POST['senha'];
