class Celula:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.peixes = []
        self.tamanho_cardume = sum(len(peixe.peso) for peixe in self.peixes)