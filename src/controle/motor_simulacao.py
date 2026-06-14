import time
import random
import sys
import select
import termios
import tty
from src.dominio import Mapa, Porto, PontoPesca, Barco, ObstaculoVisivel, ObstaculoOculto
from src.interface import ExibicaoTerminal

class MotorSimulacao:
    """
    Orquestra o laço do jogo, inicializa turnos e coleta placar.
    Coordena as atualizações do grid a cada turno e move os barcos.
    """
    def __init__(self, config: dict, mapa: Mapa, barcos: list, pontos_pesca: list, historico_boats: list):
        self.config = config
        self.mapa = mapa
        self.barcos = barcos
        self.pontos_pesca = pontos_pesca
        self.limite_turnos = config['simulacao']['limite_turnos']
        self.turno_atual = 0
        # Nova variável para lembrar os avisos mesmo quando o jogo estiver pausado 🧠
        self.ultimos_avisos = [] 

        self.historico = historico_boats 

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
                        
                        # --- EXIBE OS AVISOS NA PAUSA AQUI ---
                        if self.ultimos_avisos:
                            print("\r")
                            for aviso in self.ultimos_avisos:
                                ExibicaoTerminal.console.print(aviso)
                        
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

        # Limpa os avisos antigos para começar o novo turno do zero
        self.ultimos_avisos = []

        # Logica de movimentação e colisão de cada barco
        for barco in self.barcos:
            dx, dy = random.choice([(0,1), (0,-1), (1,0), (-1,0), (0,0)])
            
            if dx == 0 and dy == 0:
                continue

            novo_x, novo_y = barco.x + dx, barco.y + dy

            # 1. Verificação de Limites do Mapa
            if not self.mapa.posicao_valida(novo_x, novo_y):
                self.ultimos_avisos.append(f"⚠️  [bold yellow]Barco {barco.id_barco}[/bold yellow] tentou sair dos limites do mapa!")
                continue

            celula = self.mapa.obter_celula(novo_x, novo_y)

            # 2. Verificação de Obstáculos ou Bloqueios
            if not celula.navegavel:
                if celula.conteudo is not None:
                    nome_obstaculo = celula.conteudo.__class__.__name__
                    if "Obstaculo" in nome_obstaculo:
                        nome_obstaculo = "um Obstáculo 🪨"
                    self.ultimos_avisos.append(f"💥 [bold red]Barco {barco.id_barco}[/bold red] bateu em {nome_obstaculo} na posição ({novo_x}, {novo_y})!")
                else:
                    self.ultimos_avisos.append(f"💥 [bold red]Barco {barco.id_barco}[/bold red] colidiu com a costa/borda do mapa!")
                continue

            # 3. Movimento bem-sucedido
            barco.x, barco.y = novo_x, novo_y

            if random.random() > 0.7:
                pts = random.randint(1, 3)
                barco.adicionar_pontuacao(pts)
                barco.carga += random.randint(1, 2)
                self.ultimos_avisos.append(f"🐟 [bold green]Barco {barco.id_barco}[/bold green] pescou com sucesso!")

            atualizacao_historico = {
                'turno': self.turno_atual,
                'barco': barco.id_barco,
                'pontuacao': barco.pontuacao
            }
            self.historico.append(atualizacao_historico)

        # 4. Imprime os avisos acumulados imediatamente no turno normal
        if self.ultimos_avisos:
            print("\r")
            for aviso in self.ultimos_avisos:
                ExibicaoTerminal.console.print(aviso)
            sys.stdout.flush()
