import os
import json
import csv
import pickle
from typing import Iterable, Mapping, Any

import matplotlib.pyplot as plt

class PerformanceTracker:
    def __init__(self):
        self._history = {}  # name -> list of (turn, score)
        self._max_turn = -1

    def load_history_from_engine(self, dados_historico: list):
        """Carrega os dados de histórico recebidos diretamente do motor."""
        
        # Percorre cada registro da lista gerada pelo motor
        for registro in dados_historico:
            turno = registro.get('turno')
            barco_id = registro.get('barco')
            pontuacao = registro.get('pontuacao')

            # Se o barco ainda não existe no dicionário, cria uma lista para ele
            if barco_id not in self._history:
                self._history[barco_id] = []

            # Adiciona a tupla (turno, pontuacao) na lista do barco
            self._history[barco_id].append((turno, pontuacao))

            # Atualiza o controle do turno máximo
            if turno > self._max_turn:
                self._max_turn = turno


    def plot_performance(self):
        """Gera um gráfico de linha mostrando a evolução"""
        plt.figure(figsize=(10, 6))
        for barco_id, dados in self._history.items():
            turnos, pontuacoes = zip(*dados) 
            plt.plot(turnos, pontuacoes, marker='o', label=f'barco {'AStar' if barco_id == 1 else 'BFS' if barco_id == 2 else 'DFS' if barco_id == 3 else f'Barco {barco_id}'}')

        plt.title('Evolucao da pontuacao dos barcos ao longo dos turnos')
        plt.xlabel('Turno')
        plt.ylabel('Pontuacao')
        plt.xticks(range(0, self._max_turn + 1, 10))
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        
        plt.savefig('desempenho_total.png')
        
        plt.show()

    def plot_performance_individual(self):
        """Gera um gráfico de linha em janelas separadas para cada barco"""
        
        for barco_id, dados in self._history.items():
            # Define o nome do barco com base no ID
            if barco_id == 1:
                nome_barco = 'AStar'
            elif barco_id == 2:
                nome_barco = 'BFS'
            elif barco_id == 3:
                nome_barco = 'DFS'
            else:
                nome_barco = f'Barco {barco_id}'

            # Separa os turnos e as pontuações
            turnos, pontuacoes = zip(*dados) 

            # Cria uma NOVA figura para este barco específico
            plt.figure(figsize=(8, 5))
            
            # Plota os dados
            plt.plot(turnos, pontuacoes, marker='o', label=nome_barco)

            # Configurações visuais do gráfico
            plt.title(f'Evolução da pontuação - {nome_barco}')
            plt.xlabel('Turno')
            plt.ylabel('Pontuação')
            plt.xticks(range(0, self._max_turn + 1, 10))
            plt.grid(True)
            plt.legend()
            plt.tight_layout()

            nome_arquivo = f'desempenho_{nome_barco}.png'
            plt.savefig(nome_arquivo)

            # Exibe o gráfico atual antes de ir para o próximo barco do loop
            plt.show()