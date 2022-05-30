from django.shortcuts import render, redirect
from django.views import View

from django.http import HttpResponse, JsonResponse
from main.services.ClienteService import ClienteService

from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType

class LoginController(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')


    def login_user(self, request):
        if request.method == 'POST':
            nome = request.POST['nome'];
            celular = request.POST['celular'];
            user = authenticate(request, username=nome, celular=celular)
        if user is not None:
            login(request, user)
            return redirect('')
            # Redirect to a success page.
        else:
            messages.error(request, 'Error')
            return redirect('login')


    def logout_user(request):
        logout(request)
        messages.info(request, "You have successfully logged out.") 
        return redirect('')
