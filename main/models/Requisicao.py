class Cidade:
    def __init__(self, nome, uf, id) -> None:
        self.nome = nome
        self.uf = uf
        self.id = id

class PrevisaoChuvas:
    def __init__(self, nome, uf, atualizacao, lista_previsao) -> None:
        self.nome = nome
        self.uf = uf
        self.atualizacao = atualizacao
        self.lista_previsao = lista_previsao
        
class Previsao:
    def __init__(self, dia, tempo, maxima, minima, iuv) -> None:
        self.dia = dia
        self.tempo = tempo
        self.maxima = maxima
        self.minima = minima
        self.iuv = iuv

class Ondas:
    def __init__(self, nome, uf, atualizacao, manha, tarde, noite) -> None:
        self.nome = nome
        self.uf = uf
        self.atualizacao = atualizacao
        self.manha = manha
        self.tarde = tarde
        self.noite = noite
        
#Estrura para dados dentro das tags manha, tarde e noite
class OndasInfo:
    def __init__(self, dia, agitacao, altura, direcao, vento, vento_dir) -> None:
        self.dia = dia
        self.agitacao = agitacao
        self.altura = altura
        self.direcao = direcao
        self.vento = vento
        self.vento_dir = vento_dir