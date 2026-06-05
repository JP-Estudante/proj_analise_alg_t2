"""Interface Streamlit para demonstrar a comparação dos algoritmos."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from caminho_minimo.benchmark import run_benchmarks, summarize_results  # noqa: E402


st.set_page_config(
    page_title="Comparação De Caminhos Mínimos",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    :root {
        --cream: #FDEB9E;
        --mint: #7AE2CF;
        --primary: #111844;
        --primary-hover: #1D2A68;
        --gold: #C28A00;
        --ink: #111844;
        --bg: #FFF8DD;
        --panel: #FFFFFF;
        --panel-2: #FFFDF3;
        --line: #E6D99B;
        --accent-soft: #F1FFFB;
        --text: var(--ink);
        --muted: #7288AE;
    }

    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF3 48%, var(--bg) 100%);
        color: var(--text);
    }

    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1280px;
    }

    h1, h2, h3, p, label, span {
        letter-spacing: 0;
    }

    section[data-testid="stSidebar"] {
        background: #FFFDF3;
        border-right: 1px solid var(--line);
        box-shadow: 6px 0 24px rgba(6, 32, 43, 0.08);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: var(--text);
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        background: #FFFFFF;
        border: 1px solid var(--line);
        color: var(--text);
    }

    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stDownloadButton"] button {
        background: var(--primary);
        color: #FFFBEB !important;
        border: 0;
        border-radius: 8px;
        height: 2.8rem;
        font-size: 1rem;
        font-weight: 700;
        box-shadow: 0 10px 20px rgba(17, 24, 68, 0.24);
    }

    .stButton > button *,
    .stButton > button p,
    .stButton > button span,
    .stDownloadButton > button *,
    .stDownloadButton > button p,
    .stDownloadButton > button span,
    div[data-testid="stDownloadButton"] button *,
    div[data-testid="stDownloadButton"] button p,
    div[data-testid="stDownloadButton"] button span {
        color: #FFFBEB !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        border: 0;
        color: #FFFBEB !important;
        background: var(--primary-hover);
        filter: none;
    }

    .hero {
        padding: 22px 26px;
        border: 1px solid rgba(17, 24, 68, 0.20);
        border-radius: 10px;
        background: linear-gradient(135deg, #FFFFFF, var(--accent-soft));
        box-shadow: 0 18px 36px rgba(6, 32, 43, 0.08);
        margin-bottom: 18px;
    }

    .hero h1 {
        margin: 0;
        color: var(--text);
        font-size: clamp(1.9rem, 3.2vw, 2.8rem);
        line-height: 1.08;
        font-weight: 800;
    }

    .metric-card {
        min-height: 112px;
        padding: 18px 18px 16px 18px;
        border: 1px solid rgba(17, 24, 68, 0.18);
        border-radius: 10px;
        background: #FFFFFF;
        box-shadow: 0 12px 28px rgba(6, 32, 43, 0.07);
        margin-bottom: 10px;
    }

    .metric-label {
        color: var(--muted);
        font-size: 0.83rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        margin-bottom: 10px;
        white-space: nowrap;
    }

    .metric-value {
        color: var(--text);
        font-size: clamp(1.25rem, 2vw, 1.85rem);
        font-weight: 800;
        line-height: 1.15;
        overflow-wrap: anywhere;
    }

    .metric-detail {
        color: #7288AE;
        font-size: 0.86rem;
        margin-top: 8px;
    }

    .section-title {
        color: var(--text);
        font-size: 1.02rem;
        font-weight: 800;
        margin: 6px 0 12px 0;
    }

    div[data-testid="stTabs"] button {
        color: #7288AE;
        font-weight: 700;
    }

    div[data-testid="stTabs"] button[aria-selected="true"] {
        color: var(--primary);
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(17, 24, 68, 0.22);
        border-radius: 8px;
        overflow: hidden;
        background: rgba(17, 24, 68, 0.04);
        box-shadow: 0 10px 22px rgba(17, 24, 68, 0.08);
    }

    div[data-testid="stDataFrame"] [data-testid="stHeaderCell"],
    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: rgba(17, 24, 68, 0.10) !important;
        color: var(--primary) !important;
        font-weight: 800 !important;
    }

    div[data-testid="stDataFrame"] [data-testid="stHeaderCell"] *,
    div[data-testid="stDataFrame"] [role="columnheader"] * {
        color: var(--primary) !important;
    }

    hr {
        border-color: var(--line);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def parse_sizes(raw_sizes: str) -> list[int]:
    sizes = [int(item.strip()) for item in raw_sizes.split(",") if item.strip()]
    if not sizes or any(size < 2 for size in sizes):
        raise ValueError
    return sizes


@st.cache_data(show_spinner=False)
def cached_benchmark(sizes: tuple[int, ...], density: float, repetitions: int, seed: int) -> pd.DataFrame:
    results = run_benchmarks(list(sizes), density, repetitions, seed)
    return pd.DataFrame(summarize_results(results))


def short_algorithm_name(name: str) -> str:
    if name.startswith("Dijkstra"):
        return "Dijkstra"
    return name


def render_metric_card(label: str, value: str, detail: str = "") -> None:
    detail_html = f"<div class='metric-detail'>{detail}</div>" if detail else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {detail_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


COLOR_MAP = {
    "Dijkstra (todas as origens)": "#111844",
    "Floyd-Warshall": "#C28A00",
}


st.markdown(
    """
    <div class="hero">
        <h1>Dijkstra X Floyd-Warshall</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.header("Parâmetros")
    raw_sizes = st.text_input(
        "Quantidade De Vértices Por Teste",
        value="10,25,50",
        help="Informe os tamanhos dos grafos separados por vírgula. Exemplo: 10,25,50 cria três testes.",
    )
    density = st.slider(
        "Proporção De Arestas Do Grafo",
        min_value=0.05,
        max_value=1.0,
        value=0.35,
        step=0.05,
        help="Controla quão conectado o grafo será. Valores maiores geram mais arestas.",
    )
    repetitions = st.slider(
        "Execuções Por Tamanho",
        min_value=1,
        max_value=10,
        value=3,
        help="Define quantas vezes cada tamanho de grafo será testado para calcular médias mais estáveis.",
    )
    seed = st.number_input(
        "Semente De Geração Dos Grafos",
        min_value=0,
        value=42,
        step=1,
        help="Mantém os grafos reproduzíveis. Use o mesmo valor para repetir exatamente os mesmos testes.",
    )
    run_button = st.button("Executar Comparação", type="primary", use_container_width=True)

try:
    sizes = parse_sizes(raw_sizes)
except ValueError:
    st.error("Informe tamanhos válidos, separados por vírgula, todos maiores ou iguais a 2.")
    st.stop()

if run_button or "benchmark_df" not in st.session_state:
    with st.spinner("Executando testes..."):
        st.session_state.benchmark_df = cached_benchmark(tuple(sizes), density, repetitions, int(seed))

df = st.session_state.benchmark_df

largest_size = int(df["vertices"].max())
largest_df = df[df["vertices"] == largest_size].copy()
fastest = largest_df.loc[largest_df["avg_time_seconds"].idxmin()]
lowest_memory = largest_df.loc[largest_df["avg_peak_memory_kb"].idxmin()]

metric_cols = st.columns(4)
with metric_cols[0]:
    render_metric_card("Maior Grafo", f"{largest_size} Vértices", f"{int(largest_df['edges'].max())} Arestas")
with metric_cols[1]:
    render_metric_card("Densidade", f"{float(df['density'].iloc[0]):.2f}", f"{int(df['repetitions'].iloc[0])} Repetições")
with metric_cols[2]:
    render_metric_card(
        "Mais Rápido",
        short_algorithm_name(str(fastest["algorithm"])),
        f"{float(fastest['avg_time_seconds']):.6f} s No Maior Grafo",
    )
with metric_cols[3]:
    render_metric_card(
        "Menor Memória",
        short_algorithm_name(str(lowest_memory["algorithm"])),
        f"{float(lowest_memory['avg_peak_memory_kb']):.2f} KB No Maior Grafo",
    )

tab_overview, tab_table = st.tabs(["Gráficos", "Tabela"])

with tab_overview:
    col_time, col_memory = st.columns(2)

    with col_time:
        st.markdown("<div class='section-title'>Tempo Médio De Execução</div>", unsafe_allow_html=True)
        fig_time = px.line(
            df,
            x="vertices",
            y="avg_time_seconds",
            color="algorithm",
            markers=True,
            color_discrete_map=COLOR_MAP,
            labels={
                "vertices": "Vértices",
                "avg_time_seconds": "Tempo Médio (s)",
                "algorithm": "Algoritmo",
            },
        )
        fig_time.update_traces(line_width=3, marker_size=8)
        fig_time.update_layout(
            template="plotly_white",
            legend_title_text="",
            hovermode="x unified",
            height=420,
            margin=dict(l=12, r=12, t=18, b=12),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#111844"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig_time.update_xaxes(gridcolor="#E8DFAF", zerolinecolor="#E6D99B")
        fig_time.update_yaxes(gridcolor="#E8DFAF", zerolinecolor="#E6D99B")
        st.plotly_chart(fig_time, use_container_width=True)

    with col_memory:
        st.markdown("<div class='section-title'>Uso Aproximado De Memória</div>", unsafe_allow_html=True)
        fig_memory = px.line(
            df,
            x="vertices",
            y="avg_peak_memory_kb",
            color="algorithm",
            markers=True,
            color_discrete_map=COLOR_MAP,
            labels={
                "vertices": "Vértices",
                "avg_peak_memory_kb": "Pico Médio De Memória (KB)",
                "algorithm": "Algoritmo",
            },
        )
        fig_memory.update_traces(line_width=3, marker_size=8)
        fig_memory.update_layout(
            template="plotly_white",
            legend_title_text="",
            hovermode="x unified",
            height=420,
            margin=dict(l=12, r=12, t=18, b=12),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="#FFFFFF",
            font=dict(color="#111844"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        )
        fig_memory.update_xaxes(gridcolor="#E8DFAF", zerolinecolor="#E6D99B")
        fig_memory.update_yaxes(gridcolor="#E8DFAF", zerolinecolor="#E6D99B")
        st.plotly_chart(fig_memory, use_container_width=True)

with tab_table:
    formatted_df = df.rename(
        columns={
            "algorithm": "Algoritmo",
            "vertices": "Vértices",
            "edges": "Arestas",
            "density": "Densidade",
            "repetitions": "Repetições",
            "avg_time_seconds": "Tempo Médio (s)",
            "avg_peak_memory_kb": "Memória Média (KB)",
        }
    )
    styled_df = (
        formatted_df.style.format(
            {
                "Densidade": "{:.2f}",
                "Tempo Médio (s)": "{:.6f}",
                "Memória Média (KB)": "{:.2f}",
            }
        )
        .set_table_styles(
            [
                {
                    "selector": "table",
                    "props": [
                        ("width", "100%"),
                        ("border-collapse", "separate"),
                        ("border-spacing", "0"),
                        ("border", "1px solid rgba(17, 24, 68, 0.22)"),
                        ("border-radius", "8px"),
                        ("overflow", "hidden"),
                        ("box-shadow", "0 10px 22px rgba(17, 24, 68, 0.08)"),
                    ],
                },
                {
                    "selector": "thead th",
                    "props": [
                        ("background-color", "#111844"),
                        ("color", "#FFFBEB"),
                        ("font-weight", "800"),
                        ("padding", "12px 14px"),
                        ("border-right", "1px solid rgba(255, 251, 235, 0.18)"),
                        ("text-align", "left"),
                    ],
                },
                {
                    "selector": "tbody td",
                    "props": [
                        ("background-color", "#F3E9BE"),
                        ("color", "#111844"),
                        ("padding", "11px 14px"),
                        ("border-top", "1px solid #DACD95"),
                        ("border-right", "1px solid rgba(17, 24, 68, 0.12)"),
                    ],
                },
                {
                    "selector": "tbody tr:nth-child(even) td",
                    "props": [
                        ("background-color", "#EEE2AD"),
                    ],
                },
                {
                    "selector": "tbody tr:hover td",
                    "props": [
                        ("background-color", "#E7D89F"),
                    ],
                },
            ]
        )
        .set_properties(
            subset=["Vértices", "Arestas", "Densidade", "Repetições", "Tempo Médio (s)", "Memória Média (KB)"],
            **{"text-align": "right"},
        )
        .set_properties(
            subset=["Algoritmo"],
            **{"text-align": "left", "font-weight": "600"},
        )
    )
    st.table(styled_df.hide(axis="index"))
    st.download_button(
        "Baixar CSV",
        formatted_df.to_csv(index=False).encode("utf-8"),
        file_name="comparacao_caminho_minimo.csv",
        mime="text/csv",
        type="primary",
        use_container_width=False,
    )
