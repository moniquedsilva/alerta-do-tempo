from django.shortcuts import render, redirect
from django.views import View
from django.contrib.sessions.backends.db import SessionStore as DBStore

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout

from main.models.Cliente import Cliente
from main.services.ClienteService import ClienteService
from main.services.EstadosService import EstadosService
from main.services.MunicipiosService import MunicipiosService
from main.validators.ClienteValidator import ClienteValidator

class EditarController(View, DBStore):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a home.
        :param request: requisão HTTP GET.
        :return: render(request, 'editar.html').
        '''
        if not self.esta_logado(request):
            return render(request, 'errors/401.html')

        estados_service = EstadosService()
        estados = estados_service.busca_siglas_estados()
        return render(request, 'editar.html', {'estados': estados})

    def post(self, request):
        '''
        Recebe a requisição e encaminha para serem cadastradas
        :param request: requisão HTTP POST.
        :param path_name: loadCidadesByEstado or cadastrar.
        :return: Direciona para loadCidadesByEstado se path_name for 'loadCidadesByEstado' ou editar se path_name for 'editar'.
        '''
        path_name = request.resolver_match.url_name
        if(path_name == 'loadCidadesByEstado'):
            return self.loadCidadesByEstado(request)
        if(path_name == 'editar'):
            return self.editar(request)

    def editar(self, request):
        '''
        Edita um usuario cadastrado
        :param request: requisão HTTP POST.
        :param nome: string.
        :param ddi: string.
        :param ddd: string.
        :param celular: string.
        :param senha: string.
        :param municipio_id: string.
        :param estado_id: string.
        :return: JsonResponse com status.
        '''

        celular_atual = request.session['_auth_user_id']

        nome = request.POST['nome']
        ddi = request.POST['ddi']
        ddd = request.POST['ddd']
        celular = request.POST['celular']
        senha = request.POST['senha']
        municipio_id = request.POST['municipio']
        estado_id = request.POST['estado']

        cliente = Cliente(nome, ddi, ddd, celular,
                        senha, municipio_id, estado_id)
        
        cliente_service = ClienteService(cliente)

        if(not cliente_service.atualiza(celular_atual)):
            return JsonResponse({"status": False, 'msg': "Erro de atualização, por favor tente mais tarde!"})

        # Se tudo ok, retorna mensagem de sucesso
        logout(request)
        user = authenticate(self, celular=celular, senha=senha)
        if user is not None:
            login(request, user)
            request.session['_auth_user_id'] = celular
            return JsonResponse({'status': True})
    
    def loadCidadesByEstado(self, request):
        '''
        Carrega drop-down de cidades
        :param request: requisão HTTP POST.
        :param estado_id: string.
        :return: JsonResponse({'municipios': municipios_json})
        '''
        estado_id = request.POST['estado_id']
        municipios_service = MunicipiosService()
        municipios = municipios_service.busca_cidades_by_estado(
            {"estado_id": estado_id})
        municipios_json = [{m['id']: m['nome']} for m in municipios]

        return JsonResponse({'municipios': municipios_json})
    
    def esta_logado(self, request):
        if "_auth_user_id" not in request.session:
            return False
        return True


        


          
