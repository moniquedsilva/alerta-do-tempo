from django.shortcuts import render
from django.views import View


class HomeController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a home.
        :param request: requisão HTTP GET.
        :return: render(request, 'home.html').
        '''
        return render(request, 'home.html')
