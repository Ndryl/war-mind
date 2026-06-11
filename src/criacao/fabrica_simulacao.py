import random
from src.dominio import Mapa, Porto, PontoPesca, ObstaculoVisivel, ObstaculoOculto, Barco

class FabricaSimulacao:
    """
    Utiliza uma lógica Data-Driven (baseada no dicionário de config)
    para instanciar o grid (mapa), portos, barcos, pontos de pesca e obstáculos.
    """
    def __init__(self, config: dict):
        self.config = config

    def criar_mapa_e_elementos(self):
        largura = self.config['mapa']['largura']
        altura = self.config['mapa']['altura']
        mapa = Mapa(largura, altura)

        # Configurar bordas não navegáveis (primeira/última coluna, última linha)
        for y in range(altura):
            mapa.obter_celula(0, y).navegavel = False
            mapa.obter_celula(largura - 1, y).navegavel = False
        for x in range(largura):
            mapa.obter_celula(x, altura - 1).navegavel = False

        # Criar Portos na primeira linha (y=0) e os barcos
        qtd_barcos = self.config['simulacao']['quantidade_barcos']
        portos = []
        barcos = []
        espacamento = (largura - 2) // qtd_barcos
        for i in range(qtd_barcos):
            x = 1 + i * espacamento + espacamento // 2
            porto = Porto(id_porto=i+1, x=x, y=0)
            portos.append(porto)
            mapa.obter_celula(x, 0).ocupar(porto)
            
            barco = Barco(id_barco=i+1, porto_origem=porto)
            barcos.append(barco)

        # Áreas livres para spawn: x entre 1 e largura-2, y entre 1 e altura-2
        celulas_livres = [(x, y) for x in range(1, largura - 1) for y in range(1, altura - 1)]
        random.shuffle(celulas_livres)

        # Distribuir pontos de pesca
        qtd_pesca = self.config['pesca']['quantidade_pontos']
        pontos_pesca = []
        for _ in range(qtd_pesca):
            if not celulas_livres: break
            x, y = celulas_livres.pop()
            ponto = PontoPesca(x, y)
            pontos_pesca.append(ponto)
            mapa.obter_celula(x, y).ocupar(ponto)

        # Distribuir obstáculos
        obs_config = self.config['obstaculos']
        obstaculos = []
        for chave, prop in obs_config.items():
            qtd = prop['quantidade']
            penalidade = prop['penalidade_turnos']
            visivel = prop['visivel']
            for _ in range(qtd):
                if not celulas_livres: break
                x, y = celulas_livres.pop()
                if visivel:
                    obs = ObstaculoVisivel(chave, penalidade)
                else:
                    obs = ObstaculoOculto(chave, penalidade)
                obstaculos.append(obs)
                mapa.obter_celula(x, y).ocupar(obs)

        return mapa, portos, barcos, pontos_pesca, obstaculos
