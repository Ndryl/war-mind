import heapq
from typing import List, Tuple
from .interface_estrategia import IEstrategiaBusca

class EstrategiaAStar(IEstrategiaBusca):
    def _heuristica(self, atual: Tuple[int, int], destino: Tuple[int, int]) -> int:
        """
        Calcula a Distância de Manhattan entre dois pontos.
        """
        return abs(atual[0] - destino[0]) + abs(atual[1] - destino[1])

    def calcular_rota(self, inicio: Tuple[int, int], destino: Tuple[int, int], memoria_obstaculos: set, largura_mapa: int, altura_mapa: int) -> List[Tuple[int, int]]:
        # Fila de prioridade guarda apenas: (f_score, nó_atual)
        open_set = []
        heapq.heappush(open_set, (self._heuristica(inicio, destino), inicio))
        
        # Guarda de onde cada nó veio para reconstruir o caminho no final
        veio_de = {}
        
        # Custo do início até o nó atual
        g_scores = {inicio: 0}
        
        movimentos = [(0, 1), (1, 0), (0, -1), (-1, 0)] # Cima, Direita, Baixo, Esquerda

        while open_set:
            # Pega o nó com menor f_score
            _, atual = heapq.heappop(open_set)

            # Se chegou ao destino, reconstrói o caminho de trás para frente! 🏁
            if atual == destino:
                caminho = []
                while atual in veio_de:
                    caminho.append(atual)
                    atual = veio_de[atual]
                caminho.reverse() # Inverte para ficar do início ao fim
                return caminho

            for mx, my in movimentos:
                nx, ny = atual[0] + mx, atual[1] + my
                
                if 0 <= nx < largura_mapa and 0 <= ny < altura_mapa:
                    vizinho = (nx, ny)
                    
                    if vizinho in memoria_obstaculos:
                        continue
                        
                    custo_tentativo_g = g_scores[atual] + 1
                    
                    if vizinho not in g_scores or custo_tentativo_g < g_scores[vizinho]:
                        # Registra o mapa de navegação
                        veio_de[vizinho] = atual
                        g_scores[vizinho] = custo_tentativo_g
                        f_score = custo_tentativo_g + self._heuristica(vizinho, destino)
                        
                        heapq.heappush(open_set, (f_score, vizinho))
        
        return [] # Caminho não encontrado ❌