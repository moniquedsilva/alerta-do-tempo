from django.shortcuts import render
from django.views import View


class EditarController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a home.
        :param request: requisão HTTP GET.
        :return: render(request, 'editar.html').
        '''
        return render(request, 'editar.html')
