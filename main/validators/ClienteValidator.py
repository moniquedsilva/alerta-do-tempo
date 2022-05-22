from django.utils.regex_helper import _lazy_re_compile
from main.models.Cliente import Cliente
from main.services.ClienteService import ClienteService
from main.services.MunicipiosService import MunicipiosService
from main.services.EstadosService import EstadosService
import re

QTD_MIN_DIG_SENHA = 6
QTD_DIG_DDD = 2
QTD_DIG_CEL = 9
DDI_BRASIL = "55"
DDDS_VALIDOS = ["11","12","13","14","15","16","17","18","19","21","22","24","27","28","31","32","33","34","35","37","38","41","42","43","44","45","46","47","48","49","51","53","54","55","61","62","63","64","65","66","67","68","69","71","73","74","75","77","79","81","82","83","84","85","86","87","88","89","91","92","93","94","95","96","97","98","99"]
PRIMEIRO_DIGITO_CEL = "9"


class ClienteValidator:

    def __init__(self, cliente: Cliente, clienteService: ClienteService, estadosService: EstadosService, municipiosService: MunicipiosService):
        self.cliente = cliente
        self.clienteService = clienteService
        self.municipiosService = municipiosService
        self.estadosService = estadosService
    
    def valida(self):
        #Chama funções de validação para cada campo
        resposta_valida_nome = self.valida_nome()
        if(not resposta_valida_nome['status']): return resposta_valida_nome

        resposta_valida_ddi = self.valida_ddi()
        if(not resposta_valida_ddi['status']): return resposta_valida_ddi

        resposta_valida_ddd = self.valida_ddd()
        if(not resposta_valida_ddd['status']): return resposta_valida_ddd

        resposta_valida_celular = self.valida_celular()
        if(not resposta_valida_celular['status']): return resposta_valida_celular

        resposta_valida_senha = self.valida_senha()
        if(not resposta_valida_senha['status']): return resposta_valida_senha

        resposta_valida_estado_id = self.valida_estado_id()
        if(not resposta_valida_estado_id['status']): return resposta_valida_estado_id
        
        resposta_valida_municipio_id = self.valida_municipio_id()
        if(not resposta_valida_municipio_id['status']): return resposta_valida_municipio_id

        #Se realizou todas validações retorna True
        return {'status': True}
    
    def valida_nome(self):
        nome = self.cliente.nome
        #checa vazio
        if(self.estaVazio(nome)): return {'status': False, 'msg': "Digite um nome!"}
        #caracteres permitidos: letras(incluindo acentuadas), espaço, vírgula, ponto, aspas, hífen
        regex_pattern = _lazy_re_compile(r"^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð ,.'-]+$")
        #cria instância do validador
        match = re.search(regex_pattern, nome)
        if (not match): return {'status': False, 'msg': "Não é permitido números nem caractéres especiais no nome"}
        
        return {'status': True}
    
    def valida_ddi(self):
        ddi = self.cliente.ddi
        #checa vazio
        if(self.estaVazio(ddi)): return {'status': False, 'msg': "Digite um ddi!"}
        #Único valor permitido 55
        if(ddi != DDI_BRASIL): return {'status': False, 'msg': "Apenas permitimos ddi do Brasil. e.g: 55"}
        return {'status': True}

    def valida_ddd(self):
        ddd = self.cliente.ddd
        #checa vazio
        if(self.estaVazio(ddd)): return {'status': False, 'msg': "Digite um ddd!"}
        #checa qtd de dígitos
        if(len(ddd) != QTD_DIG_DDD): return {'status': False, 'msg': "O DDD deve conter " + QTD_DIG_DDD + "!"}
        #checa se ddd válido
        
        if(DDDS_VALIDOS.count(ddd) <= 0): return {'status': False, 'msg': "DDD inválido"}
        
        return {'status': True}
        
    def valida_celular(self):
        celular = self.cliente.celular
        clienteService = self.clienteService
        #checa vazio
        if(self.estaVazio(celular)): return {'status': False, 'msg': "Digite um celular!"}
        #Checa se dígitos são todos numérios
        regex_pattern = _lazy_re_compile(r"^[0-9]+$")
        match = re.search(regex_pattern, celular)
        if (not match): return {'status': False, 'msg': "Apenas dígitos numéricos são permitidos no celular. Ex: 98844332211"}
        
        #primeiro dígito deve ser 9
        if (celular[0] != PRIMEIRO_DIGITO_CEL): return {'status': False, 'msg': "O primeiro dígito do celular deve ser " + PRIMEIRO_DIGITO_CEL}
        
        #tamanho 9 dígitos, modelo: 98844332211, '55' adicionado no back-end
        if(len(celular) != QTD_DIG_CEL ): return {'status': False, 'msg': "O celuar deve conter " + str(QTD_DIG_CEL) + " dígitos"}
        #checa se celular já existe no banco
        if(clienteService.celularJaExiste() > 0): return {'status': False, 'msg': "Celular já cadastrado!"}
        
        return {'status': True}

    def valida_senha(self):
        senha = self.cliente.senha
        #checa vazio
        if(self.estaVazio(senha)): return {'status': False, 'msg': "Digite uma senha!"}
        #checa tamanho mínimo
        if(len(senha) < QTD_MIN_DIG_SENHA): return {'status': False, 'msg': "Digite uma senha com mais de " + str(QTD_MIN_DIG_SENHA) + "!"}
        
        return{'status': True}

    def valida_estado_id(self):
        estado_id = self.cliente.estado_id
        estadosService = self.estadosService
        #checa vazio
        if(self.estaVazio(estado_id)): return {'status': False, 'msg': "Escolha um estado!"}
        #checa se id do estado existe no banco
        if(estadosService.estadoIdExiste(estado_id) <= 0): return {'status': False, 'msg': "Estado Inexistente" }
        
        return {'status': True}

    def valida_municipio_id(self):
        municipio_id = self.cliente.municipio_id
        municipiosService = self.municipiosService
        #checa vazio
        if(self.estaVazio(municipio_id)): return {'status': False, 'msg': "Escolha um município!"}
        #checa se id do município existe no banco
        if(municipiosService.municipioIdExiste(municipio_id) <= 0): return {'status': False, 'msg': 'Município Inexistente'}
        
        return {'status': True}

    def estaVazio(self, campo):
        if(campo == ""): return True
        return False