from abc import ABC, abstractmethod
from typing import List, Tuple

class IEstrategiaBusca(ABC):
    @abstractmethod
    def calcular_rota(self, inicio: Tuple[int, int], destino: Tuple[int, int], memoria_obstaculos: set, largura_mapa: int, altura_mapa: int) -> List[Tuple[int, int]]:
        pass
