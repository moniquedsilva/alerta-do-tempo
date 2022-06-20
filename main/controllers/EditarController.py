from django.shortcuts import render
from django.views import View

from main.services.EstadosService import EstadosService

class EditarController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a home.
        :param request: requisão HTTP GET.
        :return: render(request, 'editar.html').
        '''
        estados_service = EstadosService()
        estados = estados_service.busca_siglas_estados()
        return render(request, 'editar.html', {'estados': estados})
          
