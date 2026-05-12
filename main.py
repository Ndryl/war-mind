import time
import random

# Importando os Models
from model.Peixe import Peixe
from model.Tabuleiro import Tabuleiro
from model.Navegador import Navegador

# Importando os Controllers
from controller.TabuleiroController import TabuleiroController
from controller.NavegadorController import NavegadorController

def main():
    print("=== INICIANDO O AMBIENTE DE SIMULAÇÃO ===")

    # 1. PREPARANDO OS DADOS INICIAIS (MODELS)
    lista_de_peixes = [Peixe("Sardinha", "Sardinha", 1, 10) for _ in range(50)]
    lista_de_peixes.extend([Peixe("Atum", "Atum", 5, 50) for _ in range(20)])
    lista_de_peixes.extend([Peixe("Tubarão", "Tubarão", 20, 200) for _ in range(5)])

    # Instanciamos o Tabuleiro e o Barco
    meu_tabuleiro = Tabuleiro(largura=10, altura=8, peixes=lista_de_peixes)
    meu_barco = Navegador(tabuleiro=meu_tabuleiro, carga_maxima=40)

    # 2. INSTANCIANDO OS CONTROLLERS
    tab_controller = TabuleiroController()
    navegadores_controller = NavegadorController()

    # 3. INICIALIZANDO O AMBIENTE
    tab_controller.gerar_peixes(meu_tabuleiro)
    
    # Esconde a Carpa Dourada e passa a classe Peixe como parâmetro
    tab_controller.esconder_carpa_dourada(meu_tabuleiro, Peixe)

    # 4. LOOP PRINCIPAL DA SIMULAÇÃO
    jogando = True
    turnos = 0
    max_turnos = 200 # Aumentei para a IA ter tempo de achar a carpa

    while jogando and turnos < max_turnos: 
        turnos += 1
        
        # A. Desenha o mapa para você visualizar
        tab_controller.exibir_no_terminal(meu_tabuleiro, meu_barco.posicao[0], meu_barco.posicao[1])

        # B. O "CÉREBRO" DA IA TOMA UMA DECISÃO
        acoes_possiveis = [
            'cima', 'baixo', 'esquerda', 'direita', 
            'pescar', 'observar', 'soltar', 'vender', 'reabastecer'
        ]
        acao_escolhida = random.choice(acoes_possiveis) 

        print(f"\n[Turno {turnos}] IA escolheu a ação: {acao_escolhida.upper()}")

        # C. O CONTROLLER DE REGRAS EXECUTA A AÇÃO E DEVOLVE O RESULTADO
        if acao_escolhida == 'pescar':
            resultado = navegadores_controller.realizar_pesca(meu_barco)
            print(f"Resultado: {resultado['mensagem']}")
            
        elif acao_escolhida == 'vender':
            resultado = navegadores_controller.vender_peixes(meu_barco)
            print(f"Resultado: {resultado['mensagem']}")
            
        elif acao_escolhida == 'reabastecer':
            resultado = navegadores_controller.reabastecer_gasolina(meu_barco)
            print(f"Resultado: {resultado['mensagem']}")
            
        elif acao_escolhida == 'soltar':
            resultado = navegadores_controller.soltar_peixes(meu_barco)
            print(f"Resultado: {resultado['mensagem']}")
            
        elif acao_escolhida == 'observar':
            # Observar retorna um booleano, então montamos um dicionário de resultado falso para padronizar
            tem_peixe = navegadores_controller.observar_peixe(meu_barco)
            msg = "Há peixes nesta célula!" if tem_peixe else "A água está vazia aqui."
            resultado = {"sucesso": True, "mensagem": msg}
            print(f"Resultado: {msg}")
            
        else:
            # Ação de movimento (cima, baixo, esquerda, direita)
            resultado = navegadores_controller.mover_barco(meu_barco, acao_escolhida)
            print(f"Resultado: {resultado['mensagem']}")

        # Mostra o Status (HUD) do Barco para a tela
        print(f"Status -> Carga: {meu_barco.carga_atual}kg/{meu_barco.carga_maxima}kg | Gasolina: {meu_barco.gasolina}L | Dinheiro: ${meu_barco.dinheiro}")

        # D. VERIFICA AS CONDIÇÕES DE TÉRMINO DA PARTIDA
        if resultado.get("ganhou"):
            print("\n🎉 FIM DE SIMULAÇÃO: O Agente encontrou e pescou a Carpa Dourada!")
            jogando = False
            
        elif resultado.get("afundou"):
            print("\n💥 FIM DE SIMULAÇÃO: O barco afundou por excesso de peso!")
            jogando = False
            
        elif resultado.get("perdeu"):
            print("\n⛽ FIM DE SIMULAÇÃO: O barco ficou sem gasolina e à deriva no oceano!")
            jogando = False
        
        # Pausa para acompanhamento (diminui um pouco para o jogo andar mais rápido)
        time.sleep(1.0) 

    # Se saiu do loop porque acabou o tempo (turnos)
    if jogando and turnos >= max_turnos:
        print(f"\n⏳ FIM DE SIMULAÇÃO: O tempo acabou! O barco sobreviveu, mas não encontrou a Carpa Dourada.")

if __name__ == "__main__":
    main()