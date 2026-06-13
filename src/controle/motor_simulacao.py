import time
import random
import sys
import select
import termios
import tty

from src.dominio import Mapa, Porto, PontoPesca, Barco, ObstaculoVisivel, ObstaculoOculto
from src.inteligencia import IEstrategiaBusca
from src.interface import ExibicaoTerminal

class MotorSimulacao:
    """
    Orquestra o laço do jogo, inicializa turnos e coleta placar.
    Coordena as atualizações do grid a cada turno e move os barcos.
    """
    def __init__(self, config: dict, mapa: Mapa, barcos: list, estrategia_padrao: IEstrategiaBusca, pontos_pesca: list):
        self.config = config
        self.mapa = mapa
        self.barcos = barcos
        self.estrategia = estrategia_padrao
        self.pontos_pesca = pontos_pesca
        self.limite_turnos = config['simulacao']['limite_turnos']
        self.turno_atual = 0


    def executar(self):
        t = 0
        pausado = False
        desenhou_pausa = False
        
        # Variável para controlar o tempo do turno (10 * 0.05 = 0.5 segundos)
        velocidade = 0.05 

        ExibicaoTerminal.console.clear() 

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)

            while t < self.limite_turnos:
                # 1. Verifica se alguma tecla foi pressionada
                if select.select([sys.stdin], [], [], 0.0)[0]:
                    tecla = sys.stdin.read(1).lower()
                    
                    if tecla == 'p':
                        pausado = not pausado
                        desenhou_pausa = False
                    
                    elif tecla == 'q':
                        break # Encerra o jogo e vai direto pro relatório final
                    
                    elif tecla == 's' and pausado:
                        # Processa 1 turno, avança o tempo e manda a tela redesenhar
                        self._processar_turno()
                        t += 1
                        self.turno_atual = t
                        desenhou_pausa = False 
                        
                    elif tecla == '+':
                        # Acelera (diminui o tempo de espera), limite mínimo de 0.01
                        velocidade = max(0.01, velocidade - 0.02)
                        
                    elif tecla == '-':
                        # Desacelera (aumenta o tempo de espera)
                        velocidade += 0.02

                # 2. Lógica de Pausa
                if pausado:
                    if not desenhou_pausa:
                        ExibicaoTerminal.limpar_tela()
                        ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
                        ExibicaoTerminal.exibir_relatorio(self.barcos, titulo="Relatório Parcial (PAUSADO)")
                        
                        # Mostra os controles na tela para você não esquecer
                        print("\r\n[ 'P' Play/Pause | 'S' Passo-a-Passo | 'Q' Sair | '+' e '-' Velocidade ]\r")
                        sys.stdout.flush()
                        desenhou_pausa = True
                        
                    time.sleep(0.1)
                    continue

                # 3. Lógica do Turno Normal
                self.turno_atual = t + 1
                ExibicaoTerminal.limpar_tela()
                ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
                self._processar_turno()
                
                # 4. Espera fracionada (usa a variável de velocidade agora)
                for _ in range(10):
                    if select.select([sys.stdin], [], [], 0.0)[0]:
                        tecla = sys.stdin.read(1).lower()
                        if tecla == 'p':
                            pausado = True
                            desenhou_pausa = False
                            break
                        elif tecla == 'q':
                            t = self.limite_turnos # Força o loop do jogo a acabar
                            break
                    time.sleep(velocidade)
                
                t += 1

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        # Fim da simulação
        ExibicaoTerminal.limpar_tela()
        ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
        ExibicaoTerminal.exibir_relatorio(self.barcos, titulo="Relatório Final")
        
    def _processar_turno(self):
        # Atualiza cooldowns globais
        for ponto in self.pontos_pesca:
            ponto.atualizar_cooldown()

        # Logica simplificada de um turno
        for barco in self.barcos:
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
            novo_x, novo_y = barco.x + dx, barco.y + dy

            if self.mapa.posicao_valida(novo_x, novo_y) and self.mapa.obter_celula(novo_x, novo_y).navegavel:
                barco.x, barco.y = novo_x, novo_y

            if random.random() > 0.5:
                # Simular captura e retorno rápido para dar pontos a eles
                pts = random.randint(1, 3) * random.randint(1, 3)
                barco.adicionar_pontuacao(pts)
                barco.carga += random.randint(1, 3)