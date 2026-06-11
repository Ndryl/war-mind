import os
from src.dominio import Mapa, Porto, PontoPesca, Barco, ObstaculoVisivel, ObstaculoOculto, Obstaculo

class ExibicaoTerminal:
    SIMBOLOS = {
        'agua_livre': '~',
        'borda': '#',
        'porto': 'P',
        'barco': 'B',
        'ponto_pesca': 'F',
        'ponto_pesca_cooldown': 'f',
        'obstaculo_visivel': 'R',  # Recife
        'tubarao': 'T',
        'redemoinho': 'W',
        'banco_areia': 'S',
        'oculto_desconhecido': '~'
    }

    @staticmethod
    def limpar_tela():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def desenhar_mapa(mapa: Mapa, barcos: list, turno_atual: int):
        print(f"--- TURNO {turno_atual} ---")
        largura, altura = mapa.largura, mapa.altura

        # Preparar posições dos barcos para sobrescrever as células temporariamente visualizadas
        pos_barcos = { (b.x, b.y): b.id_barco for b in barcos }

        for y in range(altura):
            linha_str = ""
            for x in range(largura):
                if (x, y) in pos_barcos:
                    # Mostrar o ID do barco ou B (se vários, mostramos B)
                    linha_str += "B "
                    continue

                celula = mapa.obter_celula(x, y)
                if not celula.navegavel and celula.conteudo is None:
                    # Borda
                    linha_str += ExibicaoTerminal.SIMBOLOS['borda'] + " "
                elif celula.conteudo is not None:
                    conteudo = celula.conteudo
                    if isinstance(conteudo, Porto):
                        linha_str += ExibicaoTerminal.SIMBOLOS['porto'] + " "
                    elif isinstance(conteudo, PontoPesca):
                        if conteudo.em_cooldown:
                            linha_str += ExibicaoTerminal.SIMBOLOS['ponto_pesca_cooldown'] + " "
                        else:
                            linha_str += ExibicaoTerminal.SIMBOLOS['ponto_pesca'] + " "
                    elif isinstance(conteudo, ObstaculoVisivel):
                        linha_str += ExibicaoTerminal.SIMBOLOS['obstaculo_visivel'] + " "
                    elif isinstance(conteudo, ObstaculoOculto):
                        # Só desenha o obstáculo oculto verdadeiro se a simulação quiser debugar.
                        # Para o jogo normal, mostramos água.
                        linha_str += ExibicaoTerminal.SIMBOLOS['agua_livre'] + " "
                    else:
                        linha_str += "? "
                else:
                    linha_str += ExibicaoTerminal.SIMBOLOS['agua_livre'] + " "
            print(linha_str)
        print("-" * (largura * 2))

    @staticmethod
    def exibir_relatorio(barcos: list):
        print("\n=== RELATÓRIO FINAL ===")
        barcos_ordenados = sorted(barcos, key=lambda b: b.pontuacao, reverse=True)
        for i, barco in enumerate(barcos_ordenados):
            print(f"{i+1}º Lugar - Barco {barco.id_barco} | Pontos: {barco.pontuacao} | Carga de peixes: {barco.carga}")
        print("=======================\n")
