from model.Celula import Celula

class Tabuleiro:
    def __init__(self, largura, altura, peixes):
        self.largura = largura
        self.altura = altura
        self.celulas = [[Celula(x, y) for x in range(largura)] for y in range(altura)]
        self.peixes = peixes