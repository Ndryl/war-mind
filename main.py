import os
from src.criacao import LeitorConfig, FabricaSimulacao
from src.inteligencia import EstrategiaBFS
from src.controle import MotorSimulacao
from src.graficos import PerformanceTracker
def main():
    print("Iniciando o Simulador Competitivo de Barcos de Pesca...")
    config_path = os.path.join("config", "parametros.json")
    config = LeitorConfig.ler(config_path)

    fabrica = FabricaSimulacao(config)
    mapa, portos, barcos, pontos_pesca, obstaculos = fabrica.criar_mapa_e_elementos()

    estrategia_bfs = EstrategiaBFS()
    historico_boats = []
    motor = MotorSimulacao(config, mapa, barcos, estrategia_bfs, pontos_pesca, historico_boats)
    motor.executar()


    performance = PerformanceTracker()
    performance.load_history_from_engine(motor.historico)
    performance.plot_performance()


if __name__ == "__main__":
    main()
