import os
from src.criacao import LeitorConfig, FabricaSimulacao
from src.inteligencia import EstrategiaBFS
from src.controle import MotorSimulacao

def main():
    print("Iniciando o Simulador Competitivo de Barcos de Pesca...")
    config_path = os.path.join("config", "parametros.json")
    config = LeitorConfig.ler(config_path)

    fabrica = FabricaSimulacao(config)
    mapa, portos, barcos, pontos_pesca, obstaculos = fabrica.criar_mapa_e_elementos()

    estrategia_bfs = EstrategiaBFS()

    motor = MotorSimulacao(config, mapa, barcos, estrategia_bfs, pontos_pesca)
    motor.executar()

if __name__ == "__main__":
    main()
