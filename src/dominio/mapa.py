from typing import List
from .celula import Celula

class Mapa:
    def __init__(self, largura: int, altura: int):
        self.largura = largura
        self.altura = altura
        self.grid: List[List[Celula]] = []
        self._inicializar_grid()

    def _inicializar_grid(self):
        for y in range(self.altura):
            linha = []
            for x in range(self.largura):
                linha.append(Celula(x, y))
            self.grid.append(linha)

    def obter_celula(self, x: int, y: int) -> Celula:
        if 0 <= x < self.largura and 0 <= y < self.altura:
            return self.grid[y][x]
        return None
