import os
from src.criacao import LeitorConfig, FabricaSimulacao
from src.controle import MotorSimulacao

def main():
    print("Iniciando o Simulador Competitivo de Barcos de Pesca...")
    config_path = os.path.join("config", "parametros.json")
    config = LeitorConfig.ler(config_path)

    fabrica = FabricaSimulacao(config)
    mapa, portos, barcos, pontos_pesca, obstaculos = fabrica.criar_mapa_e_elementos()

    motor = MotorSimulacao(config, mapa, barcos, pontos_pesca)
    motor.executar()

if __name__ == "__main__":
    main()