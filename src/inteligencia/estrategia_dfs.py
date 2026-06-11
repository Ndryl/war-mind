from typing import List, Tuple
from .interface_estrategia import IEstrategiaBusca

class EstrategiaDFS(IEstrategiaBusca):
    def calcular_rota(self, inicio: Tuple[int, int], destino: Tuple[int, int], memoria_obstaculos: set, largura_mapa: int, altura_mapa: int) -> List[Tuple[int, int]]:
        pilha = [[inicio]]
        visitados = set()

        movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while pilha:
            caminho = pilha.pop()
            atual = caminho[-1]

            if atual == destino:
                return caminho[1:]
            
            if atual not in visitados:
                visitados.add(atual)

                for mx, my in movimentos:
                    nx, ny = atual[0] + mx, atual[1] + my
                    if 0 <= nx < largura_mapa and 0 <= ny < altura_mapa:
                        if (nx, ny) not in visitados and (nx, ny) not in memoria_obstaculos:
                            novo_caminho = list(caminho)
                            novo_caminho.append((nx, ny))
                            pilha.append(novo_caminho)

        return []
