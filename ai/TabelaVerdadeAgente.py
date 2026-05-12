class TabelaVerdadeAgente:
    def avaliar_tabela_verdade(self, barco):
        
        no_porto = (barco.posicao == (0, 0))
        
        tem_peixe = (barco.carga_atual > 0)
        carga_cheia = (barco.carga_atual >= barco.carga_maxima)
        
        tem_dinheiro_pra_gasolina = (barco.dinheiro >= 20)
        
        x, y = barco.posicao
        custo_para_voltar = (x + y) * 5
        gasolina_critica = (barco.gasolina <= custo_para_voltar + 10)
        
        celula_atual = barco.tabuleiro.celulas[y][x]
        tem_peixe_na_agua = (len(celula_atual.peixes) > 0)


        if no_porto and tem_peixe:
            return 'vender'
            

        elif no_porto and gasolina_critica and tem_dinheiro_pra_gasolina:
            return 'reabastecer'
            
        elif not no_porto and gasolina_critica:
            return 'voltar_porto'
            
        elif carga_cheia and not no_porto:
            return 'soltar'
            
        elif tem_peixe_na_agua and not carga_cheia:
            return 'pescar'
            

        else:
            return 'mover'