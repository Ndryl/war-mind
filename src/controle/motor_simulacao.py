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
        self.ultimos_avisos = [] 
        self.historico = historico_boats 

    def executar(self):
        t = 0
        pausado = False
        desenhou_pausa = False
        velocidade = 0.05 

        ExibicaoTerminal.console.clear() 

        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)

        try:
            tty.setcbreak(fd)

            while t < self.limite_turnos:
                if select.select([sys.stdin], [], [], 0.0)[0]:
                    tecla = sys.stdin.read(1).lower()
                    if tecla == 'p':
                        pausado = not pausado
                        desenhou_pausa = False
                    elif tecla == 'q':
                        break 
                    elif tecla == 's' and pausado:
                        self._processar_turno()
                        t += 1
                        self.turno_atual = t
                        desenhou_pausa = False 
                    elif tecla == '+':
                        velocidade = max(0.01, velocidade - 0.02)
                    elif tecla == '-':
                        velocidade += 0.02

                if pausado:
                    if not desenhou_pausa:
                        ExibicaoTerminal.limpar_tela()
                        ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
                        ExibicaoTerminal.exibir_relatorio(self.barcos, titulo="Relatório Parcial (PAUSADO)")
                        
                        if self.ultimos_avisos:
                            print("\r")
                            for aviso in self.ultimos_avisos:
                                ExibicaoTerminal.console.print(aviso)
                        
                        print("\r\n[ 'P' Play/Pause | 'S' Passo-a-Passo | 'Q' Sair | '+' e '-' Velocidade ]\r")
                        sys.stdout.flush()
                        desenhou_pausa = True
                        
                    time.sleep(0.1)
                    continue

                self.turno_atual = t + 1
                ExibicaoTerminal.limpar_tela()
                ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
                self._processar_turno()
                
                for _ in range(10):
                    if select.select([sys.stdin], [], [], 0.0)[0]:
                        tecla = sys.stdin.read(1).lower()
                        if tecla == 'p':
                            pausado = True
                            desenhou_pausa = False
                            break
                        elif tecla == 'q':
                            t = self.limite_turnos 
                            break
                    time.sleep(velocidade)
                
                t += 1

        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

        ExibicaoTerminal.limpar_tela()
        ExibicaoTerminal.desenhar_mapa(self.mapa, self.barcos, self.turno_atual)
        ExibicaoTerminal.exibir_relatorio(self.barcos, titulo="Relatório Final")

    def _obter_peixe_mais_proximo(self, barco) -> PontoPesca:
        """Busca o peixe ativo mais próximo do barco usando Distância de Manhattan"""
        peixes_ativos = [p for p in self.pontos_pesca if not getattr(p, 'em_cooldown', False)]
        if not peixes_ativos:
            return None
        return min(peixes_ativos, key=lambda p: abs(barco.x - p.x) + abs(barco.y - p.y))

    def _processar_turno(self):
        # 1. Atualiza cooldowns dos peixes
        for ponto in self.pontos_pesca:
            if hasattr(ponto, 'atualizar_cooldown'):
                ponto.atualizar_cooldown()

        self.ultimos_avisos = []

        # 2. Movimentação e ação inteligente de cada barco
        for barco in self.barcos:
            # Checa se o barco já começa o turno em cima de um peixe ativo
            self._checar_e_processar_pesca(barco)

            # Localiza o peixe alvo ativo mais próximo
            alvo = self._obter_peixe_mais_proximo(barco)
            if alvo is None:
                continue

            # Retira temporariamente o peixe alvo da lista de obstáculos para a IA conseguir traçar a rota 🧭
            obstaculos_ajustados = set(getattr(barco, 'memoria_navegacao', set()))
            if (alvo.x, alvo.y) in obstaculos_ajustados:
                obstaculos_ajustados.remove((alvo.x, alvo.y))

            # Invoca a inteligência pura (A*, BFS ou DFS) guardada no barco 🧠
            estrategia = getattr(barco, 'estrategia', None)
            novo_x, novo_y = barco.x, barco.y

            if estrategia:
                # CHAMADA LIMPA: Apenas com as variáveis puras do seu algoritmo, sem kwargs! ✨
                rota = estrategia.calcular_rota(
                    inicio=(barco.x, barco.y),
                    destino=(alvo.x, alvo.y),
                    memoria_obstaculos=obstaculos_ajustados,
                    largura_mapa=self.mapa.largura,
                    altura_mapa=self.mapa.altura
                )
                if rota:
                    # Dá APENAS um passo (o primeiro quadrante da rota calculada)
                    novo_x, novo_y = rota[0]

            # Verificação de Limites do Mapa
            if not self.mapa.posicao_valida(novo_x, novo_y):
                continue

            celula = self.mapa.obter_celula(novo_x, novo_y)

            # Verifica se bateu em um obstáculo real (paredes, pedras)
            is_obstaculo_real = not celula.navegavel and (celula.conteudo is None or "Obstaculo" in celula.conteudo.__class__.__name__)
            if is_obstaculo_real:
                if hasattr(barco, 'registrar_obstaculo'):
                    barco.registrar_obstaculo(novo_x, novo_y)
                continue

            # Movimento bem-sucedido
            barco.x, barco.y = novo_x, novo_y
            if hasattr(barco, 'registrar_visita'):
                barco.registrar_visita(novo_x, novo_y)

            # Pesca IMEDIATAMENTE após dar o passo 🎣
            self._checar_e_processar_pesca(barco)

            # Registra no histórico para os gráficos de performance
            self.historico.append({
                'turno': self.turno_atual,
                'barco': barco.id_barco,
                'pontuacao': barco.pontuacao
            })

        # 3. Imprime os avisos acumulados
        if self.ultimos_avisos:
            print("\r")
            for aviso in self.ultimos_avisos:
                ExibicaoTerminal.console.print(aviso)
            sys.stdout.flush()

    def _checar_e_processar_pesca(self, barco):
        """Colhe o peixe no passo atual, pontua e mover o cardume para resetar os alvos"""
        celula_atual = self.mapa.obter_celula(barco.x, barco.y)
        
        if celula_atual.conteudo and isinstance(celula_atual.conteudo, PontoPesca):
            ponto = celula_atual.conteudo
            
            if not getattr(ponto, 'em_cooldown', False):
                ponto.em_cooldown = True
                
                # CORRIGIDO AQUI: Passando o argumento exigido pela sua classe PontoPesca ✨
                if hasattr(ponto, 'pescar'):
                    ponto.pescar(5) 
                
                # Adiciona pontuação estável
                pts = random.randint(15, 25)
                barco.adicionar_pontuacao(pts)
                barco.carga += 1
                
                # Libera a célula antiga nativamente usando a sua classe Celula
                if hasattr(celula_atual, 'desocupar'):
                    celula_atual.desocupar()
                else:
                    celula_atual.conteudo = None
                    celula_atual.navegavel = True
                
                # Sorteia uma nova coordenada no mapa para simular o movimento do cardume 🔄
                nova_x = random.randint(1, self.mapa.largura - 2)
                nova_y = random.randint(1, self.mapa.altura - 2)
                celula_nova = self.mapa.obter_celula(nova_x, nova_y)
                
                tentativas = 0
                while (not celula_nova.navegavel or celula_nova.conteudo is not None) and tentativas < 30:
                    nova_x = random.randint(1, self.mapa.largura - 2)
                    nova_y = random.randint(1, self.mapa.altura - 2)
                    celula_nova = self.mapa.obter_celula(nova_x, nova_y)
                    tentativas += 1
                
                # Realoca o peixe de forma navegável para a IA localizá-lo no próximo passo
                ponto.x = nova_x
                ponto.y = nova_y
                ponto.em_cooldown = False 
                celula_nova.conteudo = ponto
                celula_nova.navegavel = True
                
                self.ultimos_avisos.append(f"🐟 [bold green]Barco {barco.id_barco}[/bold green] pescou em ({barco.x}, {barco.y})! Cardume moveu-se para ({nova_x}, {nova_y}). (+{pts} pts)")