# Comparação de Caminhos Mínimos

Projeto acadêmico de Projeto e Análise de Algoritmos comparando duas abordagens para o Problema do Caminho Mínimo:

- **Dijkstra**: algoritmo guloso.
- **Floyd-Warshall**: programação dinâmica.

Os grafos gerados são direcionados, fortemente conexos e possuem apenas pesos positivos. Para uma comparação justa, Dijkstra é executado uma vez para cada vértice de origem, produzindo uma matriz de distâncias entre todos os pares, assim como Floyd-Warshall.

## Estrutura

```text
.
├── app.py                         # Interface Streamlit
├── requirements.txt               # Dependências
├── pyproject.toml                 # Configuração do pacote
├── src/caminho_minimo/
│   ├── algorithms.py              # Dijkstra e Floyd-Warshall
│   ├── benchmark.py               # Medição de tempo e memória
│   ├── cli.py                     # Execução pelo terminal
│   ├── graph.py                   # Geração e representação dos grafos
│   └── visualization.py           # Exportação de tabelas e gráficos
├── tests/
│   └── test_algorithms.py         # Testes de corretude
└── results/                       # Saída gerada pelo CLI
```

## Complexidade

| Algoritmo | Estratégia | Tempo | Espaço adicional |
|---|---|---:|---:|
| Dijkstra com heap | Gulosa | O((V + E) log V) por origem | O(V + E) |
| Dijkstra para todos os pares | Gulosa repetida | O(V (V + E) log V) | O(V^2) para guardar a matriz final |
| Floyd-Warshall | Programação dinâmica | O(V^3) | O(V^2) |

Como Floyd-Warshall retorna caminhos mínimos entre todos os pares de vértices, a comparação experimental usa Dijkstra para todas as origens. Assim, os dois algoritmos produzem a mesma matriz final de distâncias.

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Opcionalmente, instale o projeto em modo editável:

```bash
pip install -e .
```

## Execução simplificada

Use sempre o arquivo `executar.py` na raiz do projeto.

Para rodar os resultados no terminal e, depois de pressionar Enter, abrir o Streamlit:

```bash
python executar.py
```

Para rodar somente os resultados no terminal:

```bash
python executar.py --terminal
```

Para abrir somente o Streamlit:

```bash
python executar.py --streamlit
```

Antes de usar o Streamlit, instale as dependências:

```bash
pip install -r requirements.txt
```

## Execução direta pelo terminal

Sem instalação editável:

```bash
PYTHONPATH=src python -m caminho_minimo.cli --sizes 10,25,50 --density 0.35 --repetitions 3
```

Com instalação editável:

```bash
caminho-minimo --sizes 10,25,50 --density 0.35 --repetitions 3
```

O terminal mostra uma tabela simples com tempo médio e pico médio de memória. Também são gerados:

- `results/resultados_resumo.csv`
- `results/grafico_tempo.svg`
- `results/grafico_memoria.svg`

## Interface Streamlit

Execute:

```bash
streamlit run app.py
```

A interface permite configurar tamanhos dos grafos, densidade, repetições e semente. Ela apresenta métricas, tabela, download em CSV e gráficos interativos de tempo e memória.

## Testes

```bash
PYTHONPATH=src pytest
```

Ou, sem instalar `pytest`:

```bash
PYTHONPATH=src python -m unittest
```

Os testes verificam resultados conhecidos e confirmam que Dijkstra para todas as origens e Floyd-Warshall produzem a mesma matriz de distâncias em um grafo gerado automaticamente.
