from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from src.dominio import Mapa, Porto, PontoPesca, Barco, ObstaculoVisivel, ObstaculoOculto
import sys
class ExibicaoTerminal:
    console = Console()

    # Mapeamento de símbolos com estilos do Rich (cores)
    ESTILOS = {
        'agua_livre': ('~', 'blue'),
        'borda': ('#', 'bold white'),
        'porto': ('P', 'bold yellow'),
        'barco': ('B', 'bold green'),
        'ponto_pesca': ('F', 'green'),
        'ponto_pesca_cooldown': ('f', 'red'),
        'obstaculo_visivel': ('R', 'red'),
        'agua_default': ('~', 'blue')
    }

    @classmethod
    def desenhar_mapa(cls, mapa: Mapa, barcos: list, turno_atual: int):
        # Usamos uma tabela sem bordas para desenhar o grid do mapa
        table = Table(show_header=False, box=None, padding=(0, 1))
        
        # Criar colunas para cada coordenada X
        for _ in range(mapa.largura):
            table.add_column(justify="center")

        pos_barcos = { (b.x, b.y): b for b in barcos }

        for y in range(mapa.altura):
            linha = []
            for x in range(mapa.largura):
                if (x, y) in pos_barcos:
                    simbolo, cor = cls.ESTILOS['barco']
                    linha.append(f"[{cor}]{simbolo}[/{cor}]")
                    continue

                celula = mapa.obter_celula(x, y)
                if not celula.navegavel and celula.conteudo is None:
                    simbolo, cor = cls.ESTILOS['borda']
                elif celula.conteudo is not None:
                    conteudo = celula.conteudo
                    if isinstance(conteudo, Porto):
                        simbolo, cor = cls.ESTILOS['porto']
                    elif isinstance(conteudo, PontoPesca):
                        estilo = 'ponto_pesca_cooldown' if conteudo.em_cooldown else 'ponto_pesca'
                        simbolo, cor = cls.ESTILOS[estilo]
                    elif isinstance(conteudo, ObstaculoVisivel):
                        simbolo, cor = cls.ESTILOS['obstaculo_visivel']
                    else:
                        simbolo, cor = ('?', 'white')
                else:
                    simbolo, cor = cls.ESTILOS['agua_livre']
                
                linha.append(f"[{cor}]{simbolo}[/{cor}]")
            
            table.add_row(*linha)

        # Envolve o mapa em um painel estilizado    
        cls.console.print(Panel(table, title=f"[bold white]Turno {turno_atual}[/bold white]", expand=False))

    @classmethod
    def exibir_relatorio(cls, barcos: list, titulo="Relatório Final"):
        table = Table(title=titulo, header_style="bold magenta")
        table.add_column("Posição", justify="center")
        table.add_column("ID Barco", justify="center")
        table.add_column("Pontos", justify="right")
        table.add_column("Carga", justify="right")

        barcos_ordenados = sorted(barcos, key=lambda b: b.pontuacao, reverse=True)
        for i, b in enumerate(barcos_ordenados):
            table.add_row(f"{i+1}º", str(b.id_barco), str(b.pontuacao), str(b.carga))
        
        cls.console.print(table)
    
    @staticmethod
    def limpar_tela():
        # Move o cursor para o topo esquerdo sem piscar a tela
        sys.stdout.write('\033[H\033[0J')
        sys.stdout.flush()