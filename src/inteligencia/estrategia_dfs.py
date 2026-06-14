from typing import List, Tuple
from .interface_estrategia import IEstrategiaBusca

class EstrategiaDFS(IEstrategiaBusca):
    def calcular_rota(self, inicio: Tuple[int, int], destino: Tuple[int, int], memoria_obstaculos: set, largura_mapa: int, altura_mapa: int) -> List[Tuple[int, int]]:
        if inicio == destino:
            return []

        pilha = [inicio]
        
        visitados = set()
        visitados.add(inicio)
        
        veio_de = {}

        
        movimentos_base = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        
        
        movimentos = sorted(
            movimentos_base,
            key=lambda m: abs((inicio[0] + m[0]) - destino[0]) + abs((inicio[1] + m[1]) - destino[1]),
            reverse=True 
        )

        while pilha:
            atual = pilha.pop()

            if atual == destino:
                caminho = []
                while atual in veio_de:
                    caminho.append(atual)
                    atual = veio_de[atual]
                caminho.reverse()
                return caminho

            for mx, my in movimentos:
                nx, ny = atual[0] + mx, atual[1] + my
                
                if 0 <= nx < largura_mapa and 0 <= ny < altura_mapa:
                    vizinho = (nx, ny)
                    
                    if vizinho not in visitados and vizinho not in memoria_obstaculos:
                        visitados.add(vizinho)
                        veio_de[vizinho] = atual
                        pilha.append(vizinho)

        return [] # Caminho não encontrado ❌