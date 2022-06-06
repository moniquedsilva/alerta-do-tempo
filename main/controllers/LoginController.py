from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from main.services.ClienteService import ClienteService


class LoginController(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def login_user(request):
        if request.method == 'POST':
            celular = request.POST['celular']
            senha = request.POST['senha']

            user = authenticate(request, celular=celular, senha=senha)
            if user is not None:
                login(request, user)
                return render(request, 'dashboard.html')
            else:
                return HttpResponse('Não funcionou')

    def logout_user(request):
        if(request.session['_auth_user_id'] == 'None'):
            request.session['_auth_user_id'] = None
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('homeIndex')
