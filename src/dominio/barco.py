class Barco:
    def __init__(self, id_barco: int, porto_origem):
        self.id_barco = id_barco
        self.porto_origem = porto_origem
        self.x = porto_origem.x
        self.y = porto_origem.y
        self.pontuacao = 0
        self.carga = 0
        self.memoria_navegacao = set()  # Coordenadas de obstáculos descobertos
    
    def mover(self, x: int, y: int):
        self.x = x
        self.y = y

    def adicionar_pontuacao(self, pontos: int):
        self.pontuacao += pontos

    def registrar_obstaculo(self, x: int, y: int):
        self.memoria_navegacao.add((x, y))
