from django.contrib.auth.models import AbstractUser

class Cliente(AbstractUser):

    def __init__(self, nome, ddi, ddd, celular, senha, municipio_id, estado_id):
        super().__init__()
        self.nome = nome
        self.ddi = ddi
        self.ddd = ddd
        self.celular = celular
        self.senha = senha
        self.municipio_id = municipio_id
        self.estado_id = estado_id
    
    def save(self, *args, **kwargs):
        pass
    def groups():
        pass
    def user_permissions():
        pass       