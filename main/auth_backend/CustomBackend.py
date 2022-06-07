from django.contrib.auth.models import User
from django.contrib.auth.backends import BaseBackend
from main.services.ClienteService import ClienteService
from main.models.Cliente import Cliente
from django.contrib.auth.hashers import check_password, make_password

class CustomBackend(BaseBackend):
    def authenticate(self, request, celular=None, senha=None):
        try:
            user = self.get_user(celular)
            password_valid = check_password(senha, user.senha)
            if(password_valid): return user
            else: return None
        except Exception:
            return None
         
        
    def get_user(self, celular):
        cliente_service = ClienteService()
        c = cliente_service.busca(celular)
        if(c == None): return None
        cliente = Cliente(c['nome'], 
                            c['ddi'], 
                            c['celular'],
                            c['celular'],
                            c['senha'],
                            c['municipio_id'],
                            c['estado_id'])
        return cliente