from django.shortcuts import render
from django.views import View


class OndasController(View):

    def get(self, request):
        '''
        Renderiza a página de ondas.
        :param request: requisão HTTP GET.
        :return: render(request, 'ondas.html').
        '''
        if not self.esta_logado(request):
            return render(request, 'errors/401.html')

        return render(request, 'ondas.html')

    def esta_logado(self, request):
        if "_auth_user_id" not in request.session:
            return False
        return True
