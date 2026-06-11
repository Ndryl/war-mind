from typing import List, Tuple
from collections import deque
from .interface_estrategia import IEstrategiaBusca

class EstrategiaBFS(IEstrategiaBusca):
    def calcular_rota(self, inicio: Tuple[int, int], destino: Tuple[int, int], memoria_obstaculos: set, largura_mapa: int, altura_mapa: int) -> List[Tuple[int, int]]:
        # Fila armazenando o caminho atual: list de tuplas (x, y)
        fila = deque([[inicio]])
        visitados = set()
        visitados.add(inicio)

        movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Cima, Direita, Baixo, Esquerda

        while fila:
            caminho = fila.popleft()
            atual = caminho[-1]

            if atual == destino:
                return caminho[1:] # Retorna a rota sem o ponto de início

            for mx, my in movimentos:
                nx, ny = atual[0] + mx, atual[1] + my
                
                # Regras de borda (básicas, bordas fechadas na criação)
                if 0 <= nx < largura_mapa and 0 <= ny < altura_mapa:
                    if (nx, ny) not in visitados and (nx, ny) not in memoria_obstaculos:
                        # Considera que as bordas são tratadas como obstáculo na memória ou por colisão,
                        # Para tornar mais inteligente, deveríamos também passar ao BFS o que sabemos ser fixamente inacessível.
                        visitados.add((nx, ny))
                        novo_caminho = list(caminho)
                        novo_caminho.append((nx, ny))
                        fila.append(novo_caminho)
        
        return [] # Caminho não encontrado
