import random

# Assumindo que o import do Peixe está correto baseado na estrutura do projeto
# from model.Peixe import Peixe 

class TabuleiroController:
    def __init__(self):
        pass

    def gerar_peixes(self, tabuleiro):
        """Aplica a regra de probabilidade e popula o tabuleiro com cardumes."""
        # Nota: Mantive a sua lógica matemática original, mas lembre-se da 
        # observação sobre 'j/ultimo_j' vs 'ultimo_j/j' nas conversas anteriores 
        # para garantir a distribuição correta.
        ultimo_j = tabuleiro.altura - 1 if tabuleiro.altura > 1 else 1
        
        for x in range(tabuleiro.largura):
            for j in range(tabuleiro.altura):
                
                if tabuleiro.peixes:
                    if j == 0:
                        chance = 0
                    else:
                        # Usando a lógica que conversamos anteriormente para o degradê correto
                        progresso = ultimo_j / j 
                        chance = 1.0 - (0.3 * progresso)
                    
                    if random.random() < chance:
                        tamanho_cardume = random.randint(1, 3)
                        
                        for _ in range(tamanho_cardume):
                            tabuleiro.celulas[j][x].peixes.append(random.choice(tabuleiro.peixes))

    def exibir_no_terminal(self, tabuleiro, barco_x, barco_y):
        """Varrer o Model e exibe o estado atual na tela, incluindo o troféu."""
        print("\n=== MAPA DO OCEANO ===")
        
        # AJUSTE DE ALINHAMENTO: Como o emoji ocupa 2 espaços, e os outros ocupam 1,
        # vamos usar 2 espaços para todos para manter a grade reta.
        # A borda agora precisa ser um pouco maior (largura * 3 espaços + 1)
        print("-" * (tabuleiro.largura * 3 + 1))
        
        for y in range(tabuleiro.altura):
            linha_texto = "|"
            for x in range(tabuleiro.largura):
                celula = tabuleiro.celulas[y][x]
                
                # 1ª PRIORIDADE: O Barco (para não sumir se estiver sobre a carpa)
                if x == barco_x and y == barco_y:
                    # Usamos "x " (letra + espaço) para ocupar 2 espaços
                    linha_texto += "x |"
                
                # 2ª PRIORIDADE: Verificar se a Carpa Dourada está nesta célula
                # Usamos 'any' para buscar na lista de peixes da célula
                elif any(peixe.nome == "Carpa Dourada" for peixe in celula.peixes):
                    # O emoji já ocupa os 2 espaços visualmente no terminal
                    linha_texto += "🏆|"
                
                # 3ª PRIORIDADE: Outros peixes
                elif len(celula.peixes) > 0:
                    # Usamos "* " (asterisco + espaço) para ocupar 2 espaços
                    linha_texto += "* |"
                
                # 4ª PRIORIDADE: Água vazia
                else:
                    # Dois espaços vazios
                    linha_texto += "  |"
            
            print(linha_texto)
            print("-" * (tabuleiro.largura * 3 + 1))

    def esconder_carpa_dourada(self, tabuleiro, peixe_model):
        """
        Esconde uma única Carpa Dourada em um local aleatório do mapa.
        Adicionei 'peixe_model' como parâmetro para garantir acesso à classe Peixe.
        """
        # Cria a carpa lendária usando a classe passada por parâmetro
        carpa = peixe_model(nome="Carpa Dourada", especie="Lendária", peso=3, preco=5000)
        
        # Sorteia coordenadas aleatórias até achar uma que não seja a origem (0,0) onde está o porto/barco
        while True:
            x_aleatorio = random.randint(0, tabuleiro.largura - 1)
            y_aleatorio = random.randint(0, tabuleiro.altura - 1)
            if (x_aleatorio, y_aleatorio) != (0, 0):
                break
        
        tabuleiro.celulas[y_aleatorio][x_aleatorio].peixes.append(carpa)
        # print(f"DEBUG: Carpa escondida em ({x_aleatorio}, {y_aleatorio})") # Descomente para testar