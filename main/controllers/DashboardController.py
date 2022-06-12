from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class DashboarController(View):

    def get(self, request):
        '''
        Renderiza a dashboard.
        :param request: requisão HTTP GET.
        :return: render(request, 'dashboard.html').
        '''
        if "_auth_user_id" in request.session:
            return render(request, 'dashboard.html')
        else:
            return HttpResponse('Não logado!')