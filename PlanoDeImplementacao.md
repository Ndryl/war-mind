# Documentação do Projeto: Simulador Competitivo de Barcos de Pesca

## 1. Visão Geral do Projeto

O projeto consiste no desenvolvimento de um simulador competitivo de barcos de pesca, no qual diferentes embarcações, atuando como agentes autônomos controlados por algoritmos de Inteligência Artificial, disputarão entre si simultaneamente no mesmo mapa para determinar qual consegue obter a maior pontuação. O objetivo é otimizar as rotas de pesca dentro de uma quantidade limitada de turnos. Cada barco deverá planejar estrategicamente sua movimentação (ida ao ponto de pesca e retorno ao porto) para maximizar seu desempenho durante a competição.

O ambiente do mar será implementado por meio de um grid bidimensional que armazenará as informações sobre o cenário. A primeira linha desta matriz será destinada exclusivamente à alocação dos portos (sendo a quantidade de portos equivalente ao número de barcos participantes). Além disso, a primeira e a última coluna, bem como a última linha do grid, atuarão como bordas estritamente não navegáveis, delimitando e contornando o espaço do mapa. O restante do mar interior conterá áreas livres de navegação, pontos de pesca e diferentes tipos de obstáculos distribuídos de maneira aleatória. 

Os obstáculos serão divididos em duas categorias: **visíveis** e **ocultos**. Obstáculos visíveis, como recifes, poderão ser detectados pelo barco a uma determinada distância, exigindo que a inteligência artificial recalcule a rota preventivamente para realizar o desvio. Já os obstáculos ocultos (neblina de guerra), como tubarões, redemoinhos e bancos de areia, só serão descobertos caso o barco tente navegar pela exata célula em que estão presentes. Ao atingir um obstáculo oculto, a embarcação sofrerá uma penalidade de tempo em sua expedição (ex: 1 turno para tubarões, 2 para redemoinhos e 3 para bancos de areia). Como não há colisão física entre as embarcações, caso dois ou mais barcos coincidam de cair no mesmo obstáculo no exato mesmo turno, a respectiva punição de tempo será aplicada a todos eles integralmente. Após o cumprimento das penalidades, o obstáculo desaparecerá do mapa, deixando aquela célula permanentemente livre e navegável para as próximas viagens.

Para lidar com o desvio dos recifes (obstáculos visíveis), o simulador adotará a abordagem de **Recálculo Dinâmico**. Inicialmente, os barcos traçam a sua rota considerando o mapa desconhecido como "água livre". No entanto, a cada passo executado no grid, o Motor de Simulação atualiza o radar do agente com base no seu raio de detecção visual. Caso um recife entre no campo de visão e intersete o caminho planejado, o barco armazena a localização exata desse obstáculo na sua matriz de memória interna. Imediatamente, a rota antiga é descartada e a inteligência artificial do barco é acionada novamente para recalcular o trajeto a partir da sua posição atual, utilizando o algoritmo de busca (BFS ou DFS) mapeado sobre a sua memória atualizada, contornando o bloqueio de forma inteligente antes mesmo de colidir com ele.

A dinâmica de tempo do jogo será baseada em macro-ações: a ação completa do barco de sair do porto, ir até o ponto de pesca (desviando dos perigos) e voltar ao porto para entregar a carga será contabilizada como exatamente 1 turno regular de expedição. A esse turno serão somadas as eventuais penalidades dos obstáculos ocultos encontrados no caminho.

A pontuação do jogo será pautada em um balanço entre estocasticidade e inteligência de rota. Como os barcos competem simultaneamente na mesma matriz, é possível que suas rotas e alvos se cruzem. Caso duas ou mais embarcações coincidam de pescar na mesma célula no mesmo turno, a captura ocorrerá normalmente para todas, aplicando-se apenas a regra padrão de exaustão: após a ação conjunta, o ponto de pesca entrará em estado de *cooldown* e ficará inutilizado para qualquer barco por um número de turnos. Quando um barco pesca em um cardume, há uma probabilidade na quantidade de peixes capturados. No entanto, o multiplicador de valor de cada peixe (em pontos) será determinístico e baseado na Distância de Manhattan entre o porto e o ponto de pesca, recompensando os algoritmos que conseguirem traçar rotas mais longas e perigosas com sucesso. 

Para garantir uma implementação elegante, testável e escalável, o projeto adotará uma **Arquitetura Orientada a Objetos Baseada em Componentes**, estruturada em quatro camadas principais:

1. **Camada de Domínio (Modelos):** Conterá as entidades base que armazenam os estados, como o mapa em grid, as células físicas, os status dos portos, os pontos de pesca e os atributos brutos dos barcos (pontuação, carga e memória de navegação).
2. **Camada de Criação e Configuração:** O sistema será guiado pelo princípio de *Data-Driven Design*. Contará com um **arquivo de configuração externo** (como `.json` ou `.yaml`) que centralizará **absolutamente todos os parâmetros ajustáveis** da partida, erradicando valores fixos (*hardcoded*) no código-fonte. Este arquivo ditará:
    * As dimensões exatas da matriz do mar;
    * O limite total de turnos da simulação e a quantidade de barcos participantes;
    * O raio de detecção visual dos barcos (em células);
    * A quantidade de pontos de pesca e o tempo de duração de seus *cooldowns*;
    * As probabilidades percentuais de captura (ex: 60% para 1 peixe, 30% para 3 peixes, etc.);
    * Os multiplicadores de pontuação baseados na distância ("águas rasas", "intermediárias" e "profundas") e as distâncias que definem cada uma dessas faixas;
    * A quantidade de obstáculos visíveis e não visíveis (especificando os volumes de recifes, tubarões, redemoinhos e bancos de areia), bem como a exata penalidade de turnos que cada um desses perigos aplicará.
    * A partir da leitura deste arquivo, a camada utilizará o padrão de projeto *Abstract Factory* para instanciar todos os elementos do jogo de forma padronizada e equilibrada antes da simulação iniciar.
3. **Camada de Inteligência:** Aplicará o padrão *Strategy* para desacoplar a lógica matemática de navegação do "casco" do barco. O barco apenas delegará a decisão para uma interface de estratégia. Serão implementados, no mínimo, dois algoritmos de busca nesta camada: Busca em Largura (BFS) e Busca em Profundidade (DFS), permitindo confrontar táticas conservadoras com táticas de longa exploração.
4. **Camada de Controle:** O núcleo do sistema operará através de um Motor de Simulação (*Game Loop*). Esse gerenciador será responsável por iterar os turnos globais, acionar a inteligência de cada barco, processar a movimentação física passo a passo no grid, resolver as colisões com obstáculos e aplicar as regras de captura e pontuação.

A exibição e o acompanhamento dos acontecimentos do simulador serão realizados por meio de uma interface em **Terminal/Console**. A cada turno ou macro-ação processada pelo Motor de Simulação, o estado atual do grid será impresso na tela utilizando caracteres textuais (ASCII) para representar visualmente a água livre, a linha de portos, as bordas fechadas, os pontos de pesca, a posição dos barcos e os obstáculos descobertos. Essa abordagem garante o acompanhamento da evolução do mapa e das decisões tomadas pela Inteligência Artificial ao vivo, mantendo o foco computacional e de desenvolvimento inteiramente na lógica matemática de busca, sem a sobrecarga de bibliotecas gráficas complexas.

Apenas **ao final da execução do limite de turnos de cada barco** — ou seja, estritamente quando todas as embarcações tiverem finalizado **100%** de suas jogadas permitidas —, o motor da simulação encerrará a partida e gerará um relatório de análise de desempenho determinando o barco vencedor. O relatório comparará métricas cruciais de IA: qual algoritmo foi mais eficiente em tempo de processamento das rotas (em milissegundos), quem capturou o maior volume bruto de peixes, quem sofreu menos colisões e, por fim, quem obteve a maior pontuação acumulada entregue no porto.

---

## 2. Plano de Execução e Implementação do Software

A proposta segue os princípios da **Arquitetura Limpa (Clean Architecture)** e **SOLID**, garantindo manutenibilidade, escalabilidade, testabilidade e baixo acoplamento. A implementação será em Python, com controle rigoroso de dependências.
Evite utilizar construções excessivamente "pythônicas" ou sintaxes muito compactas que possam dificultar a compreensão por desenvolvedores iniciantes ou equipes multidisciplinares. Priorize uma escrita explícita, legível, padronizada e de fácil entendimento, mantendo a clareza acima da concisão.

### 2.1. Estrutura de Diretórios Proposta

O projeto utilizará um ambiente virtual (`.venv`) para isolar dependências. A organização reflete a separação de responsabilidades das camadas:

```text
simulador_pesca/
│
├── .venv/                      # Ambiente virtual (gerado localmente, ignorado no Git)
├── config/
│   └── parametros.json         # Arquivo Data-Driven com todas as variáveis do jogo
├── src/
│   ├── dominio/                # Camada 1: Entidades (Grid, Barco, Celula, Obstaculo)
│   ├── criacao/                # Camada 2: Abstract Factory e Leitura de Configurações
│   ├── inteligencia/           # Camada 3: Padrão Strategy (BFS, DFS, Interface)
│   ├── controle/               # Camada 4: Motor de Simulação (Game Loop) e Regras
│   └── interface/              # Camada 5: Exibição no Terminal/Console
│
├── tests/                      # Diretório de testes automatizados (Pytest)
├── main.py                     # Ponto de entrada (Entrypoint) da aplicação
├── requirements.txt            # Lista de dependências (ex: pytest, flake8)
└── README.md                   # Documentação de implantação e uso
```

### 2.2. Fases de Desenvolvimento

#### Fase 1: Fundação e Setup do Projeto
- **Objetivos:** Preparar o ambiente de desenvolvimento, definir padrões de código e criar o esqueleto arquitetural.
- **Entregáveis:** Repositório Git inicializado, ambiente .venv configurado, `requirements.txt` criado, e estrutura de pastas vazias estabelecida.
- **Responsabilidades:** Arquiteto de Software / Líder Técnico.
- **Critérios de Conclusão:** Todos os membros da equipe conseguem clonar o repositório, ativar o .venv e rodar um arquivo `main.py` em branco sem erros.
- **Dependências:** Nenhuma.

#### Fase 2: Camada de Domínio (Modelos Core)
- **Objetivos:** Implementar as entidades puras do jogo sem qualquer lógica complexa de busca. Foco na orientação a objetos pura (Encapsulamento).
- **Entregáveis:** Classes explícitas para Mapa, Celula, Barco, Porto, PontoPesca e Obstaculo (com herança simples para distinguir visíveis de ocultos).
- **Responsabilidades:** Desenvolvedor(es) Backend.
- **Critérios de Conclusão:** Instanciar um barco e colocá-lo em uma célula do mapa via código (hardcoded), alterando seus atributos básicos (pontuação, carga).
- **Dependências:** Fase 1.

#### Fase 3: Criação e Arquitetura Data-Driven
- **Objetivos:** Eliminar "números mágicos" do código implementando a leitura do `parametros.json` e o padrão Abstract Factory.
- **Entregáveis:** Arquivo JSON padronizado e um serviço (Factory) que lê o JSON, cria o grid dimensionado e espalha os elementos de forma pseudoaleatória válida.
- **Responsabilidades:** Desenvolvedor(es) Backend.
- **Critérios de Conclusão:** O sistema consegue imprimir no console (mesmo que de forma bruta) a matriz gerada puramente a partir do arquivo JSON.
- **Dependências:** Fase 2.

#### Fase 4: Inteligência Artificial (Padrão Strategy)
- **Objetivos:** Implementar os algoritmos de navegação desacoplados dos barcos (Princípio da Responsabilidade Única).
- **Entregáveis:** Interface IEstrategiaBusca, classes concretas EstrategiaBFS e EstrategiaDFS. Implementação do conceito de "Memória do Barco" e Recálculo Dinâmico.
- **Responsabilidades:** Especialista em IA / Algoritmos.
- **Critérios de Conclusão:** Dado um mapa estático com obstáculos conhecidos, as estratégias conseguem retornar uma lista explícita de coordenadas (a rota) do ponto A ao ponto B.
- **Dependências:** Fase 2.

#### Fase 5: Motor de Simulação e Controle (Game Loop)
- **Objetivos:** Orquestrar o turno a turno. Processar penalidades, cooldowns de pesca, multiplicadores de Distância de Manhattan e o avanço dos barcos.
- **Entregáveis:** Classe MotorSimulacao, exibição formal em Terminal (desenhando os ícones ASCII) e gerador de Relatório Final.
- **Responsabilidades:** Desenvolvedor(es) Fullstack/Backend.
- **Critérios de Conclusão:** Partidas completas rodando do turno 0 até o limite estipulado no JSON, exibindo a atualização visual turno a turno, culminando no relatório final.
- **Dependências:** Fases 2, 3 e 4 concluídas.

#### Fase 6: Implantação e Manutenção
- **Objetivos:** Empacotar a solução para entrega acadêmica e facilitar o uso por terceiros.
- **Entregáveis:** README.md detalhado e documentação via Docstrings.
- **Responsabilidades:** Líder Técnico / Toda a equipe.
- **Critérios de Conclusão:** Um usuário externo consegue configurar e executar o jogo lendo apenas o README.
- **Dependências:** Todas as fases anteriores.