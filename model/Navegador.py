class Navegador:
    def __init__(self, tabuleiro, carga_maxima):
        self.tabuleiro = tabuleiro
        self.posicao = (0, 0)
        self.carga_maxima = carga_maxima
        self.carga_atual = 0
        self.peixes_coletados = []
        self.afundado = False
        self.dinheiro = 0
        self.gasolina = 100