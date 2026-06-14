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
            plt.plot(turnos, pontuacoes, marker='o', label=f'barco {barco_id}')

        plt.title('Evolucao da pontuacao dos barcos ao longo dos turnos')
        plt.xlabel('Turno')
        plt.ylabel('Pontuacao')
        plt.xticks(range(0, self._max_turn + 1, 10))
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()