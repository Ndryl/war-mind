class Celula:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.navegavel = True
        self.conteudo = None

    def ocupar(self, conteudo):
        self.conteudo = conteudo
        self.navegavel = False

    def desocupar(self):
        self.conteudo = None
        self.navegavel = True
