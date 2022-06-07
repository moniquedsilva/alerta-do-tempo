from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View


class LoginController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a página de login.
        :param request: requisão HTTP GET.
        :return: render(request, 'login.html').
        '''
        return render(request, 'login.html')

    def login_user(self):
        '''
        Realiza login no sistema.
        :param request: requisião HTTP POST.
        :param celular: string.
        :param senha: string.
        :return: render(request, 'dashboard.html') ou HttpResponse('Não funcionou').
        '''
        if self.method == 'POST':
            celular = self.POST['celular']
            senha = self.POST['senha']

            user = authenticate(self, celular=celular, senha=senha)
            if user is not None:
                login(self, user)
                self.session['_auth_user_id'] = celular
                return render(self, 'dashboard.html')
            else:
                return HttpResponse('Não funcionou')

    def logout_user(self):
        '''
        Realiza logout do usuário.
        :param request: requisião HTTP.
        :return: redirect('homeIndex')
        '''
        logout(self)
        messages.info(self, "You have successfully logged out.")
        return redirect('homeIndex')
