class PontoPesca:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.em_cooldown = False
        self.turnos_cooldown_restantes = 0
    
    def pescar(self, tempo_cooldown: int):
        self.em_cooldown = True
        self.turnos_cooldown_restantes = tempo_cooldown

    def atualizar_cooldown(self):
        if self.em_cooldown:
            self.turnos_cooldown_restantes -= 1
            if self.turnos_cooldown_restantes <= 0:
                self.em_cooldown = False
                self.turnos_cooldown_restantes = 0
