from django.contrib.auth.models import AbstractUser


class Cliente(AbstractUser):
    '''
    main\models\Cliente.
    table: Clientes.
    '''

    def __init__(self, nome, ddi, ddd, celular, senha, municipio_id, estado_id):
        '''
        :property: nome.
        :property: ddi.
        :property: ddd.
        :property: celular.
        :property: senha.
        :property: municipio_id.
        :property: estado_id.
        '''
        super().__init__()
        self.nome = nome
        self.ddi = ddi
        self.ddd = ddd
        self.celular = celular
        self.senha = senha
        self.municipio_id = municipio_id
        self.estado_id = estado_id

    def save(self, *args, **kwargs):
        '''
        main\models\Cliente.
        pass fuction
        '''
        pass

    def groups(self):
        '''
        main\models\Cliente.
        pass fuction
        '''
        pass

    def user_permissions(self):
        '''
        main\models\Cliente.
        pass fuction
        '''
        pass
