from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.decorators.http import require_POST


class LoginController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a página de login.
        :param request: requisão HTTP GET.
        :return: render(request, 'login.html').
        '''
        return render(request, 'login.html')

    @require_POST
    def login_user(self, request):
        '''
        Realiza login no sistema.
        :param request: requisião HTTP POST.
        :param celular: string.
        :param senha: string.
        :return: render(request, 'dashboard.html') ou HttpResponse('Não funcionou').
        '''
        if request.method == 'POST':
            celular = request.POST['celular']
            senha = request.POST['senha']

            user = authenticate(request, celular=celular, senha=senha)
            if user is not None:
                login(request, user)
                request.session['_auth_user_id'] = celular
                return redirect('dashboard')
            else:
                return HttpResponse('Não funcionou')

    @require_POST
    def logout_user(self, request):
        '''
        Realiza logout do usuário.
        :param request: requisião HTTP.
        :return: redirect('homeIndex')
        '''
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect('homeIndex')
