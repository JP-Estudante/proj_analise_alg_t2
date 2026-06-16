"""Página simples para a atividade dinâmica da turma."""

from __future__ import annotations

import random
import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from caminho_minimo.benchmark import run_benchmarks, summarize_results  # noqa: E402


DENSITY = 0.35
REPETITIONS = 5
MODE_LABEL = "Dinâmica Da Turma"
RANGES = (
    ("Pequeno", "Grafo Pequeno", 30, 45),
    ("Médio", "Grafo Médio", 46, 60),
    ("Grande", "Grafo Grande", 61, 75),
)


st.set_page_config(
    page_title="Dinâmica Da Turma",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def ensure_seed() -> int:
    if "dynamic_page_seed" not in st.session_state:
        st.session_state.dynamic_page_seed = random.SystemRandom().randint(1000, 999999)
    return int(st.session_state.dynamic_page_seed)


@st.cache_data(show_spinner=False)
def run_dynamic_benchmark(sizes: tuple[int, ...], seed: int) -> pd.DataFrame:
    results = run_benchmarks(list(sizes), DENSITY, REPETITIONS, seed)
    dataframe = pd.DataFrame(summarize_results(results))
    category_by_vertices = {
        vertices: category
        for vertices, (category, _, _, _) in zip(sizes, RANGES)
    }
    dataframe["category"] = dataframe["vertices"].map(category_by_vertices)
    dataframe["seed"] = seed
    dataframe["mode"] = MODE_LABEL
    return dataframe


def format_dynamic_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    formatted = dataframe.rename(
        columns={
            "algorithm": "Algoritmo",
            "vertices": "Vértices",
            "edges": "Arestas",
            "density": "Densidade",
            "repetitions": "Repetições",
            "seed": "Seed",
            "category": "Categoria Do Grafo",
            "mode": "Modo",
            "avg_time_seconds": "Tempo Médio (s)",
            "avg_peak_memory_kb": "Memória Média (KB)",
        }
    )
    return formatted[
        [
            "Modo",
            "Categoria Do Grafo",
            "Seed",
            "Algoritmo",
            "Vértices",
            "Arestas",
            "Densidade",
            "Repetições",
            "Tempo Médio (s)",
            "Memória Média (KB)",
        ]
    ]


def render_dynamic_table(dataframe: pd.DataFrame) -> str:
    html_table = dataframe.to_html(index=False, classes="dynamic-results-table", border=0)
    return f'<div class="dynamic-results-table-wrap">{html_table}</div>'


st.markdown(
    """
    <style>
    :root {
        --paper: #F5F5F5;
        --teal: #76ABAE;
        --ink: #303841;
        --ink-2: #222A31;
        --orange: #FF5722;
        --white: #FFFFFF;
        --muted: #607077;
        --line: rgba(48, 56, 65, 0.16);
    }

    .stApp {
        background:
            radial-gradient(circle at 10% 12%, rgba(118, 171, 174, 0.28), transparent 34%),
            radial-gradient(circle at 92% 4%, rgba(255, 87, 34, 0.16), transparent 30%),
            linear-gradient(180deg, #222A31 0%, #303841 54%, #263039 100%);
        color: var(--paper);
    }

    .main .block-container {
        max-width: 1180px;
        padding-top: 2.25rem;
        padding-bottom: 3rem;
    }

    div[data-testid="stToolbar"] {
        background: linear-gradient(90deg, rgba(34, 42, 49, 0.96), rgba(48, 56, 65, 0.96));
        border-bottom: 1px solid rgba(118, 171, 174, 0.24);
    }

    div[data-testid="stToolbar"] button[data-testid="stBaseButton-header"],
    div[data-testid="stToolbar"] button[data-testid="stMainMenuButton"] {
        color: var(--paper) !important;
    }

    div[data-testid="stToolbar"] button[data-testid="stBaseButton-header"] span,
    div[data-testid="stToolbar"] button[data-testid="stMainMenuButton"] span,
    div[data-testid="stToolbar"] button[data-testid="stMainMenuButton"] svg {
        color: var(--paper) !important;
        fill: var(--paper) !important;
    }

    div[data-testid="stToolbar"] button[data-testid="stBaseButton-header"]:hover,
    div[data-testid="stToolbar"] button[data-testid="stMainMenuButton"]:hover {
        background: rgba(118, 171, 174, 0.16) !important;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"],
    div[data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    div[data-testid="stAppViewContainer"] > .main {
        margin-left: 0;
    }

    h1, h3, p, label, span {
        letter-spacing: 0;
    }

    .dynamic-hero {
        background:
            linear-gradient(135deg, rgba(245,245,245,0.98), rgba(118,171,174,0.28)),
            var(--paper);
        border: 1px solid rgba(245, 245, 245, 0.28);
        border-left: 7px solid var(--teal);
        border-radius: 14px;
        box-shadow: 0 24px 54px rgba(48, 56, 65, 0.12);
        margin: 0 auto 1.25rem auto;
        max-width: 1120px;
        padding: 30px 34px;
    }

    .dynamic-hero h1 {
        color: var(--ink);
        font-size: clamp(2rem, 3vw, 3rem);
        font-weight: 900;
        line-height: 1.1;
        margin: 0 0 10px 0;
    }

    .dynamic-hero p {
        color: #4D6066;
        font-size: 1.08rem;
        font-weight: 800;
        margin: 0;
        max-width: 720px;
    }

    .dynamic-kicker {
        color: var(--orange);
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        margin-bottom: 10px;
        text-transform: uppercase;
    }

    .dynamic-panel,
    .st-key-dynamic_config_panel,
    .st-key-dynamic_results_panel {
        background: rgba(245, 245, 245, 0.94);
        border: 1px solid rgba(245, 245, 245, 0.22);
        border-radius: 14px;
        box-shadow: 0 20px 46px rgba(48, 56, 65, 0.10);
        padding: 20px;
    }

    .st-key-dynamic_results_panel {
        border-left: 7px solid var(--orange);
        margin-top: 1.35rem;
    }

    .panel-title {
        align-items: center;
        color: var(--ink);
        display: flex;
        font-size: 1.08rem;
        font-weight: 900;
        gap: 10px;
        margin-bottom: 16px;
    }

    .panel-title::before {
        background: var(--orange);
        border-radius: 999px;
        content: "";
        height: 10px;
        width: 10px;
    }

    .helper-card {
        background:
            linear-gradient(180deg, rgba(34,42,49,0.96), rgba(48,56,65,0.92)),
            var(--ink-2);
        border: 1px solid rgba(118, 171, 174, 0.32);
        border-radius: 14px;
        box-shadow: 0 22px 42px rgba(48, 56, 65, 0.22);
        color: var(--white);
        min-height: 100%;
        padding: 22px;
    }

    .helper-card h2 {
        color: var(--white);
        font-size: 1.28rem;
        font-weight: 900;
        line-height: 1.15;
        margin: 0 0 12px 0;
    }

    .helper-card p {
        color: rgba(245, 245, 245, 0.80);
        font-size: 0.96rem;
        font-weight: 700;
        line-height: 1.5;
        margin: 0 0 16px 0;
    }

    .helper-stat {
        align-items: center;
        border-top: 1px solid rgba(255,255,255,0.12);
        display: flex;
        justify-content: space-between;
        padding: 12px 0;
    }

    .helper-stat span:first-child {
        color: rgba(245,245,245,0.72);
        font-size: 0.82rem;
        font-weight: 800;
    }

    .helper-stat span:last-child {
        color: #FFFFFF;
        font-size: 0.98rem;
        font-weight: 900;
    }

    .range-grid {
        display: grid;
        gap: 10px;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        margin-top: 16px;
    }

    .range-card {
        background: rgba(255,255,255,0.86);
        border: 1px solid rgba(48, 56, 65, 0.14);
        border-radius: 10px;
        padding: 12px 14px;
    }

    .range-card strong {
        color: var(--ink);
        display: block;
        font-size: 0.92rem;
        font-weight: 900;
        margin-bottom: 4px;
    }

    .range-card span {
        color: var(--muted);
        font-size: 0.84rem;
        font-weight: 800;
    }

    .fixed-info {
        background: rgba(118, 171, 174, 0.14);
        border: 1px solid rgba(118, 171, 174, 0.42);
        border-left: 5px solid var(--teal);
        border-radius: 10px;
        color: var(--ink);
        font-weight: 800;
        margin: 1rem 0;
        padding: 15px 16px;
    }

    div[data-testid="stForm"] {
        background: transparent;
        border: 0;
        padding: 0;
    }

    .st-key-dynamic_config_panel div[data-testid="stHorizontalBlock"] {
        gap: 16px;
    }

    .st-key-dynamic_config_panel div[data-testid="stElementContainer"] {
        margin-bottom: 10px;
    }

    label,
    div[data-testid="stWidgetLabel"] p {
        color: var(--ink) !important;
        font-size: 0.95rem !important;
        font-weight: 850 !important;
    }

    div[data-testid="stWidgetLabel"] {
        margin-bottom: 0.35rem !important;
    }

    div[data-testid="stTooltipIcon"] button {
        align-items: center;
        background: rgba(118, 171, 174, 0.10) !important;
        border: 1px solid rgba(118, 171, 174, 0.28) !important;
        border-radius: 999px !important;
        color: #53676E !important;
        display: inline-flex;
        height: 1.4rem;
        justify-content: center;
        width: 1.4rem;
    }

    div[data-testid="stTooltipIcon"] button:hover {
        background: rgba(255, 87, 34, 0.10) !important;
        border-color: rgba(255, 87, 34, 0.28) !important;
        color: var(--orange) !important;
    }

    div[data-baseweb="select"],
    div[data-baseweb="input"] {
        background: var(--white);
        border: 1px solid rgba(48, 56, 65, 0.14);
        border-radius: 9px;
        box-shadow: 0 10px 22px rgba(48, 56, 65, 0.06);
        min-height: 48px;
    }

    div[data-baseweb="select"]:focus-within,
    div[data-baseweb="input"]:focus-within {
        border-color: var(--teal) !important;
        box-shadow: 0 0 0 3px rgba(118, 171, 174, 0.22);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        border: 0 !important;
        box-shadow: none !important;
    }

    .st-key-dynamic_config_panel .stSelectbox [role="combobox"] + div,
    .st-key-dynamic_config_panel .stSelectbox svg[data-baseweb="icon"] {
        color: var(--ink) !important;
        fill: var(--ink) !important;
    }

    .st-key-dynamic_config_panel .stSelectbox div[value],
    .st-key-dynamic_config_panel .stSelectbox [role="combobox"] {
        color: var(--ink) !important;
        font-size: 1rem !important;
        font-weight: 780 !important;
    }

    div[role="listbox"],
    div[role="listbox"] > div,
    div[role="listbox"] > div > div,
    div[role="listbox"] div[style*="overflow: auto"],
    div[role="listbox"] div[style*="position: relative"],
    div[role="listbox"] div[style*="height:"],
    div[role="listbox"] div[style*="width: 100%"] {
        background: #FFFFFF !important;
        border: 1px solid rgba(118, 171, 174, 0.26) !important;
        border-radius: 12px !important;
        box-shadow: 0 20px 42px rgba(48, 56, 65, 0.18) !important;
        padding: 4px !important;
    }

    li[role="option"] {
        background: #FFFFFF !important;
        border: 1px solid transparent !important;
        border-radius: 9px !important;
        color: var(--ink) !important;
        margin: 2px 0 !important;
    }

    li[role="option"] > div,
    li[role="option"] > div > div,
    li[role="option"] > div > div > div,
    li[role="option"] > div > div > div > div,
    li[role="option"] * {
        background: transparent !important;
        color: var(--ink) !important;
    }

    li[role="option"][aria-selected="true"] {
        background: rgba(118, 171, 174, 0.24) !important;
        border: 1px solid rgba(118, 171, 174, 0.34) !important;
    }

    li[role="option"][aria-selected="true"] > div,
    li[role="option"][aria-selected="true"] > div > div,
    li[role="option"][aria-selected="true"] > div > div > div,
    li[role="option"][aria-selected="true"] > div > div > div > div,
    li[role="option"][aria-selected="true"] * {
        color: var(--ink) !important;
        font-weight: 850 !important;
    }

    li[role="option"]:hover {
        background: rgba(255, 87, 34, 0.12) !important;
        border: 1px solid rgba(255, 87, 34, 0.20) !important;
    }

    div[data-baseweb="input"] input {
        color: var(--ink);
        font-size: 1rem;
        font-weight: 750;
    }

    div[data-testid="stNumberInputContainer"] {
        gap: 0.4rem;
    }

    button[data-testid="stNumberInputStepDown"],
    button[data-testid="stNumberInputStepUp"] {
        background: rgba(118, 171, 174, 0.10) !important;
        border: 1px solid rgba(118, 171, 174, 0.24) !important;
        border-radius: 10px !important;
        color: var(--ink) !important;
        height: 2.15rem !important;
        width: 2.15rem !important;
    }

    button[data-testid="stNumberInputStepDown"]:hover,
    button[data-testid="stNumberInputStepUp"]:hover {
        background: rgba(255, 87, 34, 0.10) !important;
        border-color: rgba(255, 87, 34, 0.30) !important;
        color: var(--orange) !important;
    }

    .stButton > button,
    .stDownloadButton > button,
    div[data-testid="stDownloadButton"] button,
    button[data-testid="stBaseButton-primary"],
    button[data-testid="stBaseButton-primaryFormSubmit"] {
        background: var(--ink);
        border: 0 !important;
        border-radius: 8px !important;
        box-shadow: 0 14px 24px rgba(48, 56, 65, 0.24);
        color: #FFFFFF !important;
        font-size: 1rem;
        font-weight: 800;
        height: 3rem;
    }

    .stButton > button *,
    .stDownloadButton > button *,
    div[data-testid="stDownloadButton"] button *,
    button[data-testid="stBaseButton-primary"] *,
    button[data-testid="stBaseButton-primaryFormSubmit"] * {
        color: #FFFFFF !important;
    }

    div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] {
        background:
            linear-gradient(135deg, #303841 0%, #222A31 100%) !important;
        border: 1px solid rgba(118, 171, 174, 0.24) !important;
        border-radius: 12px !important;
        box-shadow:
            0 18px 34px rgba(34, 42, 49, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.06);
        height: 3.35rem;
        padding: 0 1.1rem;
        transition:
            transform 160ms ease,
            box-shadow 160ms ease,
            background 160ms ease;
    }

    div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] > div {
        gap: 0.65rem;
    }

    div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] p {
        font-size: 1.02rem !important;
        font-weight: 850 !important;
        letter-spacing: 0.01em;
    }

    div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"] [data-testid="stIconMaterial"] {
        font-size: 1.08rem !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover,
    div[data-testid="stDownloadButton"] button:hover {
        background: var(--orange);
        border: 0;
        color: #FFFFFF !important;
    }

    div[data-testid="stForm"] button[data-testid="stBaseButton-primaryFormSubmit"]:hover {
        background:
            linear-gradient(135deg, #FF5722 0%, #E14A1A 100%) !important;
        border-color: rgba(255, 255, 255, 0.16);
        box-shadow:
            0 22px 40px rgba(255, 87, 34, 0.28),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transform: translateY(-1px);
    }

    div[data-testid="stDownloadButton"] button[data-testid="stBaseButton-primary"] {
        background:
            linear-gradient(135deg, #39424C 0%, #303841 100%) !important;
        border: 1px solid rgba(118, 171, 174, 0.20) !important;
        border-radius: 12px !important;
        box-shadow:
            0 18px 34px rgba(34, 42, 49, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
        height: 3.2rem;
        padding: 0 1rem;
    }

    div[data-testid="stDownloadButton"] button[data-testid="stBaseButton-primary"] > div {
        gap: 0.6rem;
    }

    div[data-testid="stDownloadButton"] button[data-testid="stBaseButton-primary"] p {
        font-size: 1rem !important;
        font-weight: 820 !important;
    }

    div[data-testid="stDownloadButton"] button[data-testid="stBaseButton-primary"]:hover {
        background:
            linear-gradient(135deg, #FF5722 0%, #E14A1A 100%) !important;
        border-color: rgba(255, 255, 255, 0.14) !important;
        box-shadow:
            0 22px 40px rgba(255, 87, 34, 0.26),
            inset 0 1px 0 rgba(255, 255, 255, 0.08);
        transform: translateY(-1px);
    }

    .results-panel {
        background: rgba(255,255,255,0.86);
        border: 1px solid var(--line);
        border-left: 7px solid var(--orange);
        border-radius: 14px;
        box-shadow: 0 22px 46px rgba(48, 56, 65, 0.10);
        margin-top: 1.35rem;
        padding: 20px;
    }

    .results-heading {
        color: var(--ink);
        font-size: 1.55rem;
        font-weight: 900;
        line-height: 1.1;
        margin: 0 0 14px 0;
    }

    .results-heading,
    .results-heading * {
        color: var(--ink) !important;
    }

    .dynamic-results-table-wrap {
        background: #FFFDF7;
        border: 1px solid rgba(48, 56, 65, 0.16);
        border-radius: 12px;
        box-shadow: 0 12px 26px rgba(48, 56, 65, 0.08);
        overflow-x: auto;
        overflow-y: hidden;
    }

    table.dynamic-results-table {
        border-collapse: collapse;
        min-width: 980px;
        width: 100%;
    }

    table.dynamic-results-table thead th {
        background: #D7E4E5;
        border-bottom: 1px solid rgba(48, 56, 65, 0.14);
        color: var(--ink);
        font-size: 0.95rem;
        font-weight: 900;
        padding: 0.9rem 0.85rem;
        text-align: left;
        white-space: nowrap;
    }

    table.dynamic-results-table tbody td {
        background: #FFF9E9;
        border-bottom: 1px solid rgba(48, 56, 65, 0.08);
        color: var(--ink);
        font-size: 0.94rem;
        font-weight: 700;
        padding: 0.82rem 0.85rem;
        white-space: nowrap;
    }

    table.dynamic-results-table tbody tr:nth-child(even) td {
        background: #FCF4D9;
    }

    table.dynamic-results-table tbody tr:hover td {
        background: rgba(118, 171, 174, 0.14);
    }

    @media (max-width: 760px) {
        .dynamic-hero,
        .dynamic-panel,
        .st-key-dynamic_config_panel,
        .st-key-dynamic_results_panel,
        .helper-card,
        .results-panel {
            border-radius: 10px;
            padding: 16px;
        }

        .range-grid {
            grid-template-columns: 1fr;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="dynamic-hero">
        <div class="dynamic-kicker">Atividade Individual</div>
        <h1>Missão Caminho Mínimo</h1>
        <p>Escolha um grafo de cada tamanho, execute a comparação e baixe o CSV para compor a análise coletiva.</p>
        <div class="range-grid">
            <div class="range-card"><strong>Grafo Pequeno</strong><span>30 a 45 vértices</span></div>
            <div class="range-card"><strong>Grafo Médio</strong><span>46 a 60 vértices</span></div>
            <div class="range-card"><strong>Grafo Grande</strong><span>61 a 75 vértices</span></div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

default_seed = ensure_seed()

form_column, helper_column = st.columns([2.25, 1], gap="large")

with form_column:
    with st.container(key="dynamic_config_panel"):
        st.markdown('<div class="panel-title">Configuração Da Simulação</div>', unsafe_allow_html=True)
        with st.form("dynamic_form"):
            columns = st.columns(3)
            selected_sizes: list[int] = []
            for column, (_, label, start, end) in zip(columns, RANGES):
                with column:
                    selected_sizes.append(
                        int(
                            st.selectbox(
                                label,
                                options=list(range(start, end + 1)),
                                index=(end - start) // 2,
                                help=f"Escolha um valor entre {start} e {end} vértices.",
                            )
                        )
                    )

            seed = int(
                st.number_input(
                    "Semente",
                    min_value=0,
                    value=default_seed,
                    step=1,
                    help="Use esta semente para identificar e reproduzir a sua simulação.",
                )
            )

            st.markdown(
                f"""
                <div class="fixed-info">
                    Proporção De Arestas Do Grafo: {DENSITY:.2f} &nbsp; | &nbsp;
                    Execuções Por Tamanho: {REPETITIONS}
                </div>
                """,
                unsafe_allow_html=True,
            )

            submitted = st.form_submit_button(
                "Executar E Gerar CSV",
                type="primary",
                icon=":material/play_arrow:",
                use_container_width=True,
            )

with helper_column:
    st.markdown(
        f"""
        <div class="helper-card">
            <h2>O Que Será Gerado</h2>
            <p>Um CSV com os resultados de Dijkstra e Floyd-Warshall para os três tamanhos de grafo escolhidos.</p>
            <div class="helper-stat"><span>Comparações</span><span>3 cenários</span></div>
            <div class="helper-stat"><span>Algoritmos</span><span>2 por cenário</span></div>
            <div class="helper-stat"><span>Densidade</span><span>{DENSITY:.2f}</span></div>
            <div class="helper-stat"><span>Repetições</span><span>{REPETITIONS}</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

if submitted or "dynamic_results" not in st.session_state:
    with st.spinner("Executando comparação da dinâmica..."):
        st.session_state.dynamic_results = run_dynamic_benchmark(tuple(selected_sizes), seed)

formatted_df = format_dynamic_dataframe(st.session_state.dynamic_results)

with st.container(key="dynamic_results_panel"):
    st.markdown('<h2 class="results-heading">Resultados Gerados</h2>', unsafe_allow_html=True)
    st.markdown(render_dynamic_table(formatted_df), unsafe_allow_html=True)

    st.download_button(
        "Baixar CSV Da Dinâmica",
        formatted_df.to_csv(index=False).encode("utf-8"),
        file_name="comparacao_caminho_minimo_dinamica.csv",
        mime="text/csv",
        type="primary",
        icon=":material/download:",
        use_container_width=True,
    )
