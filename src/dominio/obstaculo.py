class Obstaculo:
    def __init__(self, nome: str, penalidade_turnos: int):
        self.nome = nome
        self.penalidade_turnos = penalidade_turnos
        self.visivel = False

class ObstaculoVisivel(Obstaculo):
    def __init__(self, nome: str, penalidade_turnos: int):
        super().__init__(nome, penalidade_turnos)
        self.visivel = True

class ObstaculoOculto(Obstaculo):
    def __init__(self, nome: str, penalidade_turnos: int):
        super().__init__(nome, penalidade_turnos)
        self.visivel = False
