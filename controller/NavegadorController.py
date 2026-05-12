class NavegadorController:
    def __init__(self):
        pass

    def mover_barco(self, barco, direcao):
        if barco.afundado:
            return {"sucesso": False, "mensagem": "Barco afundado", "afundou": True}
            
        # BLOQUEIO DE GASOLINA: Só move se tiver combustível
        if barco.gasolina < 5:
            return {"sucesso": False, "mensagem": "Falta de gasolina! Barco à deriva.", "afundou": False, "perdeu": True}

        x, y = barco.posicao
        nova_posicao = barco.posicao

        if direcao == 'cima' and y > 0:
            nova_posicao = (x, y - 1)
        elif direcao == 'baixo' and y < barco.tabuleiro.altura - 1:
            nova_posicao = (x, y + 1)
        elif direcao == 'esquerda' and x > 0:
            nova_posicao = (x - 1, y)
        elif direcao == 'direita' and x < barco.tabuleiro.largura - 1:
            nova_posicao = (x + 1, y)

        if nova_posicao != barco.posicao:
            barco.posicao = nova_posicao
            barco.gasolina -= 5 # Agora sim, desconta a gasolina de forma segura
            return {"sucesso": True, "mensagem": "Moveu com sucesso", "afundou": False}
        else:
            return {"sucesso": False, "mensagem": "Bateu na borda do mapa", "afundou": False}

    def realizar_pesca(self, barco):
        if barco.afundado:
            return {"sucesso": False, "mensagem": "Barco afundado", "peso_pescado": 0, "afundou": True}

        x, y = barco.posicao
        celula_atual = barco.tabuleiro.celulas[y][x]
        
        if not celula_atual.peixes:
            return {"sucesso": True, "mensagem": "Não havia peixes aqui", "peso_pescado": 0, "afundou": False}

        peixes_capturados = celula_atual.peixes[:]
        barco.peixes_coletados.extend(peixes_capturados)
        celula_atual.peixes = [] 
        
        barco.carga_atual = sum(peixe.peso for peixe in barco.peixes_coletados)
        peso_nesta_pesca = sum(peixe.peso for peixe in peixes_capturados)
        
        if barco.carga_atual > barco.carga_maxima:
            barco.afundado = True
            barco.peixes_coletados = []
            barco.carga_atual = 0
            return {
                "sucesso": False, 
                "mensagem": f"Capotou! Peso excedeu a carga máxima de {barco.carga_maxima}kg", 
                "peso_pescado": peso_nesta_pesca,
                "afundou": True
            }
            
        # CHECAGEM DE VITÓRIA (A CARPA DOURADA)
        pescou_carpa = any(peixe.nome == "Carpa Dourada" for peixe in peixes_capturados)
        if pescou_carpa:
            return {
                "sucesso": True, 
                "mensagem": "VITÓRIA! VOCÊ ENCONTROU A CARPA DOURADA!", 
                "peso_pescado": peso_nesta_pesca,
                "afundou": False,
                "ganhou": True
            }
        
        return {
            "sucesso": True, 
            "mensagem": "Pescaria de sucesso", 
            "peso_pescado": peso_nesta_pesca,
            "afundou": False,
            "ganhou": False
        }
    
    def observar_peixe(self, barco):
        x, y = barco.posicao
        celula_atual = barco.tabuleiro.celulas[y][x]
        return len(celula_atual.peixes) > 0
    
    def soltar_peixes(self, barco):
        if barco.afundado:
            return {"sucesso": False, "mensagem": "Barco afundado", "afundou": True}
        if not barco.peixes_coletados:
            return {"sucesso": True, "mensagem": "Não há peixes para soltar", "afundou": False}
        barco.peixes_coletados = []
        barco.carga_atual = 0
        return {"sucesso": True, "mensagem": "Peixes soltos com sucesso", "afundou": False}
    
    def vender_peixes(self, barco):
        # REGRAS DO PORTO (Opcional, mas recomendado para IA)
        if barco.posicao != (0, 0):
            return {"sucesso": False, "mensagem": "Você precisa estar no Porto (0,0) para vender peixes!", "afundou": False}
            
        if not barco.peixes_coletados:
            return {"sucesso": False, "mensagem": "Nenhum peixe para vender", "afundou": False}

        valor_venda = sum(peixe.preco for peixe in barco.peixes_coletados)
        barco.dinheiro += valor_venda
        barco.peixes_coletados = []
        barco.carga_atual = 0
        return {"sucesso": True, "mensagem": f"Peixes vendidos por {valor_venda} moedas", "afundou": False}
    
    def reabastecer_gasolina(self, barco):
        # REGRAS DO PORTO
        if barco.posicao != (0, 0):
            return {"sucesso": False, "mensagem": "Você precisa estar no Porto (0,0) para abastecer!", "afundou": False}
            
        # CHECAGEM DE DINHEIRO
        if barco.dinheiro < 20:
             return {"sucesso": False, "mensagem": "Dinheiro insuficiente! Custa 20 moedas.", "afundou": False}

        barco.gasolina = 100
        barco.dinheiro -= 20
        return {"sucesso": True, "mensagem": "Gasolina reabastecida", "afundou": False}