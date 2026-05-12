# 🐟 Busca pela Carpa Dourada: Agente Autônomo com Busca em Profundidade

Este projeto é uma simulação desenvolvida para a disciplina de Inteligência Artificial. O objetivo é implementar um **Agente Autônomo** capaz de navegar por um oceano simulado em grid, gerenciando recursos finitos (gasolina, peso e dinheiro) enquanto busca por um objetivo final: encontrar a lendária Carpa Dourada.

## 🎯 Objetivo do Agente
O agente controla um barco de pesca e precisa tomar decisões lógicas a cada turno. Ele deve equilibrar a exploração do mapa com a necessidade de sobrevivência (não afundar por excesso de peso e não ficar à deriva por falta de gasolina).

A condição de vitória é encontrar e pescar a **Carpa Dourada (🏆)**.

## 🧠 A Inteligência Artificial

O cérebro do agente foi modelado utilizando duas abordagens clássicas de IA:

### 1. Sistema Baseado em Regras (Tabela Verdade)
A tomada de decisão do agente é regida por uma Tabela Verdade que converte a percepção do mundo (estado do barco e do tabuleiro) em variáveis booleanas. O agente avalia axiomas lógicos em ordem de prioridade:
1. **Sobrevivência:** Se a gasolina for exata para a distância de volta (Distância de Manhattan), o agente aborta a exploração e retorna ao porto.
2. **Economia:** Se estiver no porto com carga, vende. Se estiver sem gasolina e com dinheiro, reabastece.
3. **Gerenciamento de Carga:** Se estiver muito pesado para continuar pescando, o agente solta peixes comuns para dar espaço à Carpa Dourada.
4. **Exploração:** Se houver peixe na célula e espaço no barco, ele pesca.

### 2. Busca em Profundidade (DFS - Depth-First Search)
Quando não há ações críticas de sobrevivência a serem tomadas, o agente utiliza o algoritmo de Busca em Profundidade para navegar. Ele explora o máximo possível uma rota e utiliza *Backtracking* (lembrando os caminhos inversos) quando fica encurralado, garantindo que todo o oceano será vasculhado de forma sistemática.

## 🏗️ Arquitetura do Projeto

O código foi construído utilizando forte separação de responsabilidades, inspirada no padrão MVC (Model-View-Controller), para isolar a inteligência das regras de negócio:

* **`/model`**: Estruturas de dados passivas. Contém a representação física do mundo.
  * `Tabuleiro.py`, `Navegador.py`, `Peixe.py`, `Celula.py`
* **`/controller`**: As "leis da física" do mundo. Aplica limites de movimento, calcula pesos, deduz gasolina e gera probabilidades matemáticas de cardumes.
  * `NavegadorController.py`, `TabuleiroController.py`
* **`/ai`**: O "cérebro" do agente, isolado do mundo físico.
  * `TabelaVerdadeAgente.py`
* **`main.py`**: O motor da simulação (Engine). Instancia o mundo, o agente e gerencia o loop de tempo (turnos).

## ⚙️ Como Executar

**Pré-requisitos:**
* Python 3.x instalado.
* Nenhuma biblioteca externa é necessária (projeto construído com módulos built-in do Python como `random` e `time`).

**Passo a passo:**
1. Clone este repositório.
2. Navegue até a pasta raiz do projeto.
3. Execute o motor principal:
   ```bash
   python main.py
