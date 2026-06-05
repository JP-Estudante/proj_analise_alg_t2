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
        --gold: #D19600;
        --gold-soft: #FFE08A;
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
        background:
            linear-gradient(180deg, #FFFFFF 0%, #FFF8DD 46%, #FDEB9E 100%);
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
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF8DD 100%);
        border-right: 1px solid rgba(17, 24, 68, 0.12);
        box-shadow: 8px 0 28px rgba(17, 24, 68, 0.10);
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
        border: 1px solid #D19600;
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
        box-shadow: 0 14px 24px rgba(17, 24, 68, 0.28);
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
        padding: 26px 28px;
        border: 1px solid rgba(17, 24, 68, 0.22);
        border-radius: 10px;
        background:
            linear-gradient(135deg, rgba(255, 255, 255, 0.96), rgba(122, 226, 207, 0.38)),
            linear-gradient(90deg, rgba(253, 235, 158, 0.48), rgba(255, 255, 255, 0));
        box-shadow: 0 20px 42px rgba(17, 24, 68, 0.12);
        margin-bottom: 18px;
    }

    .hero h1 {
        margin: 0;
        color: var(--text);
        font-size: clamp(1.9rem, 3.2vw, 2.8rem);
        line-height: 1.08;
        font-weight: 800;
    }

    .hero-kicker {
        color: #D19600;
        font-size: 0.92rem;
        font-weight: 800;
        letter-spacing: 0.04em;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .metric-card {
        min-height: 112px;
        padding: 18px 18px 16px 18px;
        border: 1px solid rgba(17, 24, 68, 0.16);
        border-top: 4px solid #D19600;
        border-radius: 10px;
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF3 100%);
        box-shadow: 0 14px 30px rgba(17, 24, 68, 0.10);
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

    .metric-heading {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 10px;
    }

    .metric-icon {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: #111844;
        color: #FFFBEB;
        font-size: 0.86rem;
        font-weight: 900;
        line-height: 1;
    }

    .metric-heading .metric-label {
        margin-bottom: 0;
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


def render_metric_card(label: str, value: str, detail: str = "", icon: str = "•") -> None:
    detail_html = f"<div class='metric-detail'>{detail}</div>" if detail else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-heading">
                <span class="metric-icon">{icon}</span>
                <div class="metric-label">{label}</div>
            </div>
            <div class="metric-value">{value}</div>
            {detail_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


COLOR_MAP = {
    "Dijkstra (todas as origens)": "#111844",
    "Floyd-Warshall": "#D19600",
}


def style_plotly_chart(fig, height: int = 380) -> None:
    fig.update_layout(
        template="plotly_white",
        legend_title_text="",
        hovermode="x unified",
        height=height,
        margin=dict(l=12, r=12, t=18, b=12),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFEF8",
        font=dict(color="#111844"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    fig.update_xaxes(gridcolor="#E6D99B", zerolinecolor="#D19600")
    fig.update_yaxes(gridcolor="#E6D99B", zerolinecolor="#D19600")


def build_time_ratio_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    pivot = dataframe.pivot(index="vertices", columns="algorithm", values="avg_time_seconds").reset_index()
    dijkstra_column = "Dijkstra (todas as origens)"
    floyd_column = "Floyd-Warshall"

    if dijkstra_column not in pivot or floyd_column not in pivot:
        return pd.DataFrame(columns=["vertices", "ratio"])

    return pd.DataFrame(
        {
            "vertices": pivot["vertices"],
            "ratio": pivot[floyd_column] / pivot[dijkstra_column],
        }
    )


st.markdown(
    """
    <div class="hero">
        <div class="hero-kicker">Problema Do Caminho Mínimo</div>
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
    run_button = st.button(
        "Executar Comparação",
        type="primary",
        icon=":material/play_arrow:",
        use_container_width=True,
    )

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
    render_metric_card("Maior Grafo", f"{largest_size} Vértices", f"{int(largest_df['edges'].max())} Arestas", "V")
with metric_cols[1]:
    render_metric_card("Densidade", f"{float(df['density'].iloc[0]):.2f}", f"{int(df['repetitions'].iloc[0])} Repetições", "%")
with metric_cols[2]:
    render_metric_card(
        "Mais Rápido",
        short_algorithm_name(str(fastest["algorithm"])),
        f"{float(fastest['avg_time_seconds']):.6f} s No Maior Grafo",
        "T",
    )
with metric_cols[3]:
    render_metric_card(
        "Menor Memória",
        short_algorithm_name(str(lowest_memory["algorithm"])),
        f"{float(lowest_memory['avg_peak_memory_kb']):.2f} KB No Maior Grafo",
        "M",
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
        fig_time.update_traces(line_width=3.5, marker_size=9)
        style_plotly_chart(fig_time, height=420)
        st.plotly_chart(fig_time, use_container_width=True, config={"displayModeBar": False})

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
        fig_memory.update_traces(line_width=3.5, marker_size=9)
        style_plotly_chart(fig_memory, height=420)
        st.plotly_chart(fig_memory, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div class='section-title'>Comparações Complementares</div>", unsafe_allow_html=True)
    col_time_bar, col_ratio, col_edges = st.columns(3)

    with col_time_bar:
        st.markdown("<div class='section-title'>Tempo Por Algoritmo</div>", unsafe_allow_html=True)
        fig_time_bar = px.bar(
            df,
            x="vertices",
            y="avg_time_seconds",
            color="algorithm",
            barmode="group",
            color_discrete_map=COLOR_MAP,
            labels={
                "vertices": "Vértices",
                "avg_time_seconds": "Tempo Médio (s)",
                "algorithm": "Algoritmo",
            },
        )
        fig_time_bar.update_traces(marker_line_width=0, opacity=0.96)
        style_plotly_chart(fig_time_bar, height=340)
        st.plotly_chart(fig_time_bar, use_container_width=True, config={"displayModeBar": False})

    with col_ratio:
        st.markdown("<div class='section-title'>Razão De Tempo</div>", unsafe_allow_html=True)
        ratio_df = build_time_ratio_dataframe(df)
        fig_ratio = px.bar(
            ratio_df,
            x="vertices",
            y="ratio",
            labels={
                "vertices": "Vértices",
                "ratio": "Floyd / Dijkstra",
            },
            color_discrete_sequence=["#D19600"],
        )
        fig_ratio.add_hline(
            y=1,
            line_dash="dash",
            line_color="#7288AE",
            annotation_text="Mesmo tempo",
            annotation_position="top left",
        )
        fig_ratio.update_traces(
            marker_line_width=0,
            opacity=0.96,
            hovertemplate="Vértices: %{x}<br>Razão: %{y:.2f}x<extra></extra>",
        )
        style_plotly_chart(fig_ratio, height=340)
        fig_ratio.update_layout(showlegend=False)
        st.plotly_chart(fig_ratio, use_container_width=True, config={"displayModeBar": False})

    with col_edges:
        st.markdown("<div class='section-title'>Arestas Por Tamanho</div>", unsafe_allow_html=True)
        edges_df = df.drop_duplicates("vertices").sort_values("vertices")
        fig_edges = px.bar(
            edges_df,
            x="vertices",
            y="edges",
            labels={
                "vertices": "Vértices",
                "edges": "Arestas",
            },
            color_discrete_sequence=["#5E7FB8"],
        )
        fig_edges.update_traces(
            marker_line_width=0,
            opacity=0.96,
            hovertemplate="Vértices: %{x}<br>Arestas: %{y}<extra></extra>",
        )
        style_plotly_chart(fig_edges, height=340)
        fig_edges.update_layout(showlegend=False)
        st.plotly_chart(fig_edges, use_container_width=True, config={"displayModeBar": False})

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
                        ("background-color", "#F8EDBA"),
                        ("color", "#111844"),
                        ("padding", "11px 14px"),
                        ("border-top", "1px solid #DACD95"),
                        ("border-right", "1px solid rgba(17, 24, 68, 0.12)"),
                    ],
                },
                {
                    "selector": "tbody tr:nth-child(even) td",
                    "props": [
                        ("background-color", "#F1DF9E"),
                    ],
                },
                {
                    "selector": "tbody tr:hover td",
                    "props": [
                        ("background-color", "#FDEB9E"),
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
        icon=":material/download:",
        use_container_width=False,
    )
