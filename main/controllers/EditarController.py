from django.shortcuts import render
from django.views import View

from django.http import JsonResponse

from django.contrib.auth import authenticate, login, logout

from main.models.Cliente import Cliente
from main.services.ClienteService import ClienteService
from main.services.EstadosService import EstadosService
from main.services.MunicipiosService import MunicipiosService
from main.validators.ClienteValidator import ClienteValidator

class EditarController(View):

    def get(self, request, *args, **kwargs):
        '''
        Renderiza a home.
        :param request: requisão HTTP GET.
        :return: render(request, 'editar.html').
        '''
        estados_service = EstadosService()
        estados = estados_service.busca_siglas_estados()
        return render(request, 'editar.html', {'estados': estados});

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
        celular_atual = self.session.get('_auth_user_id');

        buscar_usario = ClienteService.busca(self, celular=celular_atual)
        
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
        estados_service = EstadosService()
        municipios_service = MunicipiosService()

        cliente_validator = ClienteValidator(
            cliente, cliente_service, estados_service, municipios_service)
        resposta_validacao = cliente_validator.valida()
        if(not resposta_validacao['status']):
            return JsonResponse(resposta_validacao)

        ClienteService.atualiza(cliente, celular_atual=celular_atual)

        if(not cliente_service.atualiza()):
            return JsonResponse({"status": False, 'msg': "Erro de atualização, por favor tente mais tarde!"})

        # Se tudo ok, retorna mensagem de sucesso
        if self.method == 'POST':
            celular = self.POST['celular']
            senha = self.POST['senha']

            user = authenticate(self, celular=celular, senha=senha)
            if user is not None:
                login(self, user)
                self.session['_auth_user_id'] = celular
                return render(self, 'dashboard.html')


        


          
