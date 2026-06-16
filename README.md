# Comparação de Caminhos Mínimos

Projeto acadêmico de Projeto e Análise de Algoritmos comparando duas abordagens para o Problema do Caminho Mínimo:

- **Dijkstra**: algoritmo guloso.
- **Floyd-Warshall**: programação dinâmica.

Os grafos gerados são direcionados, fortemente conexos e possuem apenas pesos positivos. Para uma comparação justa, Dijkstra é executado uma vez para cada vértice de origem, produzindo uma matriz de distâncias entre todos os pares, assim como Floyd-Warshall.

## Estrutura

```text
.
├── app.py                         # Interface Streamlit
├── pages/
│   ├── dinamica.py                # Geração de CSVs para a atividade da turma
│   └── resultados-dinamica.py     # Análise coletiva dos CSVs importados
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

Use o arquivo `executar.py`, localizado na raiz do projeto, para executar tudo de forma simples.

Para mostrar os resultados no terminal e, depois de pressionar Enter, abrir a interface Streamlit:

```bash
python executar.py
```

Para executar somente a comparação no terminal:

```bash
python executar.py --terminal
```

Para abrir somente a interface Streamlit:

```bash
python executar.py --streamlit
```

Esse é o fluxo recomendado para apresentação, pois primeiro mostra uma saída simples no terminal e depois abre o dashboard visual.

Antes de executar o projeto, instale as dependências:

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

Também é possível abrir a interface diretamente:

```bash
streamlit run app.py
```

A interface Streamlit foi organizada para apoiar a apresentação do trabalho. Ela possui:

- **Barra lateral de parâmetros**: quantidade de vértices por teste, proporção de arestas do grafo, execuções por tamanho e semente de geração dos grafos.
- **Resumo dos parâmetros**: maior grafo, arestas previstas, execuções totais e indicação de que Dijkstra e Floyd-Warshall usam o mesmo grafo.
- **Métricas principais**: maior grafo, densidade, algoritmo mais rápido e algoritmo com menor uso aproximado de memória.
- **Resultados principais**: gráficos de tempo médio de execução e uso aproximado de memória.
- **Comparações complementares**: gráficos auxiliares de tempo por algoritmo, razão de tempo, distribuição de arestas, tempo por densidade e tempo por arestas.
- **Tabela de resultados**: dados resumidos com opção de download em CSV.

O dashboard usa gráficos interativos para facilitar a comparação entre os algoritmos e a explicação dos resultados durante a apresentação.

### Páginas da atividade dinâmica

Além do dashboard principal, o projeto possui duas páginas diretas para a dinâmica da turma:

- `/dinamica`: página simples para cada aluno escolher um grafo pequeno, médio e grande, executar a comparação e baixar o CSV da dinâmica.
- `/resultados-dinamica`: página para o apresentador importar múltiplos CSVs da turma, consolidar os dados e visualizar gráficos agregados.

A página principal continua sendo apenas o dashboard normal. A atividade dinâmica fica separada para não misturar a apresentação geral com a coleta dos resultados da turma.

## Testes

```bash
PYTHONPATH=src pytest
```

Ou, sem instalar `pytest`:

```bash
PYTHONPATH=src python -m unittest
```

Os testes verificam resultados conhecidos e confirmam que Dijkstra para todas as origens e Floyd-Warshall produzem a mesma matriz de distâncias em um grafo gerado automaticamente.
