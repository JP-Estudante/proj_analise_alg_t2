"""Página para consolidar os CSVs da atividade dinâmica."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st


REQUIRED_COLUMNS = [
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

CATEGORY_ORDER = ["Pequeno", "Médio", "Grande"]
COLOR_MAP = {
    "Dijkstra (todas as origens)": "#111844",
    "Floyd-Warshall": "#D19600",
}

CHART_ICONS = {
    "summary": """
        <svg viewBox="0 0 52 52" aria-hidden="true">
            <path fill="currentColor" d="M49.30195 49.30861c-2.40997 2.38995-6.26001 2.19995-8.41998-.26001l-8.26001-9.33002c3.0858-1.92774 5.6316-4.6288 7.08002-7.08997l9.33997 8.25995C51.75196 43.32856 51.45198 47.13856 49.30195 49.30861zM26.40199 19.21858V34.1186c3.0603-1.20237 5.71787-3.8247 6.79999-5.88v-9.02002H26.40199zM17.60194 10.09858v24.69c2.30296.5653 4.67377.53127 6.80005-.01001V10.09858H17.60194zM8.80195 24.37861v3.83997c1.48417 2.54061 3.86393 4.70809 6.79999 5.91003v-9.75H8.80195z"/>
            <path fill="currentColor" d="M6.85353,35.16493c-7.79688-7.79785-7.79785-20.49463,0-28.30273c7.81983-7.81781,20.47685-7.81767,28.30566-0.00098c7.65651,7.66882,7.92533,20.38294,0,28.3042C27.47855,42.84227,14.80152,43.12423,6.85353,35.16493z M9.56594,9.57356c-6.30362,6.31239-6.30362,16.5765,0,22.88055c6.36253,6.37259,16.60726,6.27374,22.88143-0.00044c6.43725-6.43725,6.16037-16.71031-0.00087-22.88055C26.12367,3.25755,15.8881,3.25231,9.56594,9.57356z"/>
        </svg>
    """,
    "time": """
        <svg viewBox="0 0 92 92" aria-hidden="true">
            <path fill="currentColor" d="M81.3 19.6c.8.7 1.7 1 2.7 1 1.1 0 2.2-.4 3-1.3 1.5-1.6 1.4-4.2-.3-5.7l-5.2-4.7-5.2-4.7c-1.6-1.5-4.2-1.4-5.6.3-1.5 1.6-1.4 4.2.3 5.7l2.2 2-4 4.5c-4.6-3.4-9.9-5.9-15.7-7.2-.1-1.3-.6-2.7-1.6-4-1-1.4-3.1-3-6.9-3.2h-.2c-3.5 0-5.5 1.5-6.6 2.8-1.2 1.4-1.7 3.1-1.9 4.4C17.8 13.4 4 29.8 4 49.4c0 22.5 18.3 40.9 40.8 40.9 22.5 0 40.8-18.3 40.8-40.9 0-10.5-4-20.1-10.5-27.4l4-4.5 2.2 2.1zM44.8 82.2C26.7 82.2 12 67.5 12 49.4s14.7-32.8 32.8-32.8c18.1 0 32.8 14.7 32.8 32.8S62.9 82.2 44.8 82.2zm7-32.8c0 3.8-3.2 6.9-7 6.9S38 53.2 38 49.4c0-2.3 1-4.4 3-5.6V27.6c0-2.2 1.8-4 4-4s4 1.8 4 4v16.2c2 1.2 2.8 3.3 2.8 5.6z"/>
        </svg>
    """,
    "memory": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M22,14.86a0,0,0,0,1,0,0v-.05a2.61,2.61,0,0,0-.1-.57L20.26,4.51a3,3,0,0,0-3-2.51H6.69A3,3,0,0,0,3.74,4.51L2.12,14.22a2.61,2.61,0,0,0-.1.57v.05a0,0,0,0,1,0,0C2,14.91,2,15,2,15v4a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V15C22,15,22,14.91,22,14.86ZM5.71,4.83a1,1,0,0,1,1-.83H17.31a1,1,0,0,1,1,.83l1.2,7.22A2.63,2.63,0,0,0,19,12H5a2.63,2.63,0,0,0-.49.05ZM20,19a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V15.08l.08-.46A1,1,0,0,1,5,14H19a1,1,0,0,1,.92.62l.08.46Zm-3-3a1,1,0,1,0,1,1A1,1,0,0,0,17,16Z"/>
        </svg>
    """,
    "scatter": """
        <svg viewBox="0 0 123 115" fill="none" aria-hidden="true">
            <path d="M81.5 61.5C94.7548 61.5 105.5 50.7548 105.5 37.5C105.5 24.2452 94.7548 13.5 81.5 13.5C68.2452 13.5 57.5 24.2452 57.5 37.5C57.5 50.7548 68.2452 61.5 81.5 61.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M38 83.5C46.0081 83.5 52.5 77.0081 52.5 69C52.5 60.9919 46.0081 54.5 38 54.5C29.9919 54.5 23.5 60.9919 23.5 69C23.5 77.0081 29.9919 83.5 38 83.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M72 92.5C77.2467 92.5 81.5 88.2467 81.5 83C81.5 77.7533 77.2467 73.5 72 73.5C66.7533 73.5 62.5 77.7533 62.5 83C62.5 88.2467 66.7533 92.5 72 92.5Z" stroke="currentColor" stroke-width="7"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="3" fill-rule="evenodd" clip-rule="evenodd" d="M4.65789 1.5C6.40194 1.5 7.81579 2.8196 7.81579 4.44737V86.9737C7.81579 98.3682 17.7126 107.605 29.9211 107.605H118.342C120.086 107.605 121.5 108.925 121.5 110.553C121.5 112.18 120.086 113.5 118.342 113.5H29.9211C14.2246 113.5 2.84328 101.877 1.5 86.9737V4.44737C1.5 2.8196 2.91385 1.5 4.65789 1.5Z"/>
        </svg>
    """,
    "ratio": """
        <svg viewBox="0 0 133 113" fill="none" aria-hidden="true">
            <path fill="currentColor" d="M132.366 73.4869C131.357 79.7308 125.423 84.0138 119.179 83.0046C118.157 82.8394 117.21 82.5699 116.348 82.1393L92.8834 99.0241C93.0204 99.9782 92.9688 101.018 92.8036 102.04C91.7944 108.284 85.86 112.567 79.616 111.558C73.372 110.548 69.0891 104.614 70.0983 98.3701C70.2634 97.3483 70.5421 96.345 70.9727 95.4826L58.8376 78.6684C57.8836 78.8054 56.8435 78.7538 55.8217 78.5887C54.8 78.4235 53.7966 78.1448 52.9343 77.7142L22.9233 99.4238C23.0603 100.378 23.0178 101.361 22.8527 102.383C21.8435 108.627 15.909 112.91 9.66507 111.901C3.42111 110.891 -0.861862 104.957 0.147364 98.713C1.15659 92.4691 7.09102 88.1861 13.335 89.1953C14.3567 89.3605 15.3033 89.63 16.1657 90.0606L46.2243 68.417C46.0873 67.4629 46.1389 66.4228 46.304 65.401C47.3133 59.1571 53.2477 54.8741 59.4916 55.8833C65.7356 56.8926 70.0186 62.827 69.0093 69.071C68.8442 70.0927 68.5655 71.0961 68.1349 71.9584L80.27 88.7726C81.2241 88.6356 82.2642 88.6872 83.2859 88.8524C84.3076 89.0175 85.311 89.2962 86.1734 89.7268L109.591 72.7761C109.454 71.822 109.496 70.8387 109.661 69.817C110.67 63.573 116.605 59.29 122.849 60.2993C129.093 61.3085 133.376 67.2429 132.366 73.4869Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.1" d="M93.257 0.0501709C101.489 0.0590747 109.382 3.33262 115.203 9.15369C121.024 14.9748 124.298 22.8678 124.307 31.1C124.307 37.2409 122.486 43.2439 119.074 48.35C115.663 53.456 110.813 57.4364 105.14 59.7865C99.4661 62.1366 93.2224 62.7512 87.1993 61.5531C81.1763 60.355 75.6433 57.3984 71.3009 53.056C66.9585 48.7136 64.0019 43.1807 62.8038 37.1576C61.6058 31.1346 62.2205 24.8917 64.5704 19.2181C66.9205 13.5445 70.9008 8.69441 76.007 5.28259C81.113 1.87096 87.116 0.0501725 93.257 0.0501709ZM103.124 7.27966C98.4129 5.32818 93.2282 4.81703 88.2267 5.81189C83.2253 6.80677 78.6313 9.26271 75.0255 12.8685C71.4197 16.4744 68.9637 21.0683 67.9689 26.0697C66.974 31.0712 67.4852 36.2559 69.4366 40.9672C71.3881 45.6783 74.6928 49.7054 78.9327 52.5385C83.1727 55.3714 88.1576 56.8832 93.257 56.8832L93.8966 56.8744C100.501 56.7036 106.798 54.0063 111.481 49.3236C116.314 44.4899 119.033 37.9358 119.04 31.1C119.04 26.0007 117.528 21.0157 114.695 16.7758C111.862 12.5358 107.835 9.23116 103.124 7.27966Z"/>
        </svg>
    """,
}

CHART_TOOLTIPS = {
    "Resultados Coletivos": "Resumo visual dos CSVs enviados pela turma. Os gráficos mostram médias agregadas por categoria de grafo e algoritmo.",
    "Tempo Médio Por Categoria": "Compara o tempo médio dos algoritmos em grafos pequenos, médios e grandes. Barras maiores indicam maior tempo de execução.",
    "Memória Média Por Categoria": "Compara o uso aproximado de memória dos algoritmos por categoria de grafo. A medição usa o pico médio registrado no benchmark.",
    "Vértices X Tempo Médio": "Mostra cada execução consolidada. Ajuda a perceber se o tempo aumenta conforme cresce a quantidade de vértices.",
    "Razão Floyd / Dijkstra": "Mostra quantas vezes o Floyd-Warshall demorou em relação ao Dijkstra. Valor 1 significa empate; acima de 1 indica Floyd-Warshall mais lento.",
}


def style_chart(fig, height: int = 370) -> None:
    fig.update_layout(
        template="plotly_white",
        height=height,
        margin=dict(l=18, r=18, t=34, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFDF3",
        font=dict(color="#111844", family="Arial, sans-serif", size=12),
        legend_title_text="",
        hovermode="x unified",
        legend=dict(
            bgcolor="rgba(255,255,255,0.76)",
            bordercolor="rgba(17,24,68,0.10)",
            borderwidth=1,
            font=dict(size=11),
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        hoverlabel=dict(
            bgcolor="#111844",
            bordercolor="#7AE2CF",
            font=dict(color="#FFFBEB", size=12),
        ),
    )
    fig.update_xaxes(
        gridcolor="rgba(230, 217, 155, 0.36)",
        linecolor="rgba(17, 24, 68, 0.30)",
        showline=True,
        tickfont=dict(color="#7288AE", size=11),
        title_font=dict(color="#7288AE", size=12),
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="rgba(230, 217, 155, 0.62)",
        linecolor="rgba(17, 24, 68, 0.22)",
        showline=True,
        tickfont=dict(color="#7288AE", size=11),
        title_font=dict(color="#7288AE", size=12),
        zerolinecolor="#7AE2CF",
        zerolinewidth=1.2,
    )


def render_chart_title(title: str, icon_key: str, featured: bool = False, tooltip: str | None = None) -> None:
    class_name = "chart-heading chart-heading--featured" if featured else "chart-heading"
    tooltip_text = tooltip or CHART_TOOLTIPS.get(title, "")
    tooltip_html = (
        f'<span class="chart-heading-help" title="{tooltip_text}" aria-label="{tooltip_text}">?</span>'
        if tooltip_text
        else ""
    )
    st.markdown(
        f"""
        <div class="{class_name}">
            <span class="chart-heading-icon">{CHART_ICONS[icon_key]}</span>
            <span>{title}</span>
            {tooltip_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_summary_card(label: str, value: str, detail: str) -> None:
    st.markdown(
        f"""
        <div class="summary-card">
            <div class="summary-label">{label}</div>
            <div class="summary-value">{value}</div>
            <div class="summary-detail">{detail}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def read_uploaded_csv(uploaded_file) -> tuple[pd.DataFrame | None, str | None]:
    try:
        dataframe = pd.read_csv(uploaded_file)
    except Exception as exc:
        return None, f"{uploaded_file.name}: não foi possível ler o CSV ({exc})."

    missing = [column for column in REQUIRED_COLUMNS if column not in dataframe.columns]
    if missing:
        return None, f"{uploaded_file.name}: colunas ausentes: {', '.join(missing)}"

    dataframe = dataframe[REQUIRED_COLUMNS].copy()
    dataframe["Arquivo"] = uploaded_file.name
    numeric_columns = [
        "Seed",
        "Vértices",
        "Arestas",
        "Densidade",
        "Repetições",
        "Tempo Médio (s)",
        "Memória Média (KB)",
    ]
    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    if dataframe[numeric_columns].isna().any().any():
        return None, f"{uploaded_file.name}: existem valores numéricos inválidos."

    invalid_modes = dataframe[dataframe["Modo"] != "Dinâmica Da Turma"]
    if not invalid_modes.empty:
        return None, f"{uploaded_file.name}: o campo Modo deve ser 'Dinâmica Da Turma'."

    return dataframe, None


def build_ratio_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    keys = ["Arquivo", "Seed", "Categoria Do Grafo", "Vértices", "Arestas", "Densidade"]
    pivot = dataframe.pivot_table(
        index=keys,
        columns="Algoritmo",
        values="Tempo Médio (s)",
        aggfunc="mean",
    ).reset_index()

    dijkstra_column = "Dijkstra (todas as origens)"
    floyd_column = "Floyd-Warshall"
    if dijkstra_column not in pivot or floyd_column not in pivot:
        return pd.DataFrame(columns=["Categoria Do Grafo", "Razão Floyd / Dijkstra"])

    pivot["Razão Floyd / Dijkstra"] = pivot[floyd_column] / pivot[dijkstra_column]
    return pivot[["Categoria Do Grafo", "Razão Floyd / Dijkstra"]]


st.markdown(
    """
    <style>
    :root {
        --primary: #111844;
        --primary-hover: #1D2A68;
        --accent: #7AE2CF;
        --accent-rgb: 122, 226, 207;
        --gold: #D19600;
        --muted: #7288AE;
        --line: #E6D99B;
    }

    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF8DD 50%, #FDEB9E 100%);
        color: var(--primary);
    }

    .main .block-container {
        max-width: 1220px;
        padding-top: 2.4rem;
    }

    section[data-testid="stSidebar"] {
        display: none;
    }

    div[data-testid="stSidebarCollapsedControl"] {
        display: none;
    }

    div[data-testid="stAppViewContainer"] > .main {
        margin-left: 0;
    }

    h1, h2, h3, p, label, span {
        letter-spacing: 0;
    }

    .results-hero {
        background: linear-gradient(135deg, rgba(255,255,255,0.94), rgba(122,226,207,0.28));
        border: 1px solid rgba(17, 24, 68, 0.18);
        border-left: 5px solid var(--accent);
        border-radius: 12px;
        box-shadow: 0 18px 36px rgba(17, 24, 68, 0.10);
        margin-bottom: 1.2rem;
        padding: 22px 24px;
    }

    .results-hero h1 {
        color: var(--primary);
        font-size: 2rem;
        font-weight: 900;
        line-height: 1.1;
        margin: 0 0 8px 0;
    }

    .results-hero p {
        color: var(--muted);
        font-size: 1rem;
        font-weight: 700;
        margin: 0;
    }

    .summary-card {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFFDF3 100%);
        border: 1px solid rgba(17, 24, 68, 0.16);
        border-top: 4px solid var(--accent);
        border-radius: 10px;
        box-shadow: 0 14px 30px rgba(17, 24, 68, 0.10);
        min-height: 104px;
        padding: 16px 18px 14px 18px;
    }

    .summary-label {
        color: var(--muted);
        font-size: 0.78rem;
        font-weight: 900;
        letter-spacing: 0.04em;
        margin-bottom: 9px;
        text-transform: uppercase;
        white-space: nowrap;
    }

    .summary-value {
        color: var(--primary);
        font-size: clamp(1.25rem, 2vw, 1.75rem);
        font-weight: 900;
        line-height: 1.1;
    }

    .summary-detail {
        color: var(--muted);
        font-size: 0.84rem;
        font-weight: 700;
        margin-top: 8px;
    }

    .chart-heading {
        align-items: center;
        color: var(--primary);
        display: flex;
        font-size: 1rem;
        font-weight: 900;
        gap: 0.55rem;
        letter-spacing: 0;
        line-height: 1.1;
        margin: 10px 0 12px 0;
    }

    .chart-heading-icon {
        align-items: center;
        background: #111844;
        border-radius: 8px;
        box-shadow: 0 8px 18px rgba(17, 24, 68, 0.18);
        color: #FFFBEB;
        display: inline-flex;
        flex: 0 0 auto;
        height: 28px;
        justify-content: center;
        width: 28px;
    }

    .chart-heading-icon svg {
        display: block;
        height: 17px;
        overflow: visible;
        width: 17px;
    }

    .chart-heading-help {
        align-items: center;
        border: 1px solid rgba(17, 24, 68, 0.24);
        border-radius: 999px;
        color: #7288AE;
        cursor: help;
        display: inline-flex;
        flex: 0 0 auto;
        font-size: 0.72rem;
        font-weight: 900;
        height: 18px;
        justify-content: center;
        margin-left: 0.1rem;
        width: 18px;
    }

    .chart-heading--featured {
        background:
            linear-gradient(90deg, rgba(17, 24, 68, 0.08), rgba(var(--accent-rgb), 0.20)),
            rgba(255, 255, 255, 0.42);
        border: 1px solid rgba(17, 24, 68, 0.12);
        border-left: 4px solid var(--accent);
        border-radius: 10px;
        box-shadow: 0 10px 24px rgba(17, 24, 68, 0.08);
        font-size: 1.04rem;
        margin: 24px 0 18px 0;
        padding: 10px 12px;
    }

    .chart-heading--featured .chart-heading-icon {
        background: var(--accent);
        color: #111844;
    }

    .st-key-collective_charts_panel,
    .st-key-collective_table_panel {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.60), rgba(255, 253, 243, 0.86)),
            rgba(122, 226, 207, 0.10);
        border: 1px solid rgba(17, 24, 68, 0.14);
        border-left: 6px solid var(--accent);
        border-radius: 12px;
        box-shadow: 0 18px 38px rgba(17, 24, 68, 0.10);
        margin-top: 26px;
        overflow: hidden;
        padding: 0 14px 16px 14px;
    }

    .st-key-collective_charts_panel .chart-heading--featured,
    .st-key-collective_table_panel .chart-heading--featured {
        border-left: 0;
        border-radius: 0;
        margin: 0 -14px 18px -14px;
    }

    div[data-testid="stPlotlyChart"] {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(255, 253, 243, 0.98));
        border: 1px solid rgba(17, 24, 68, 0.12);
        border-radius: 12px;
        box-shadow: 0 16px 32px rgba(17, 24, 68, 0.10);
        box-sizing: border-box;
        overflow: hidden;
        padding: 10px 12px 2px 12px;
    }

    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        max-width: 100%;
        overflow: hidden !important;
    }

    div[data-testid="stDataFrame"] {
        background: rgba(17, 24, 68, 0.04);
        border: 1px solid rgba(17, 24, 68, 0.22);
        border-radius: 8px;
        box-shadow: 0 10px 22px rgba(17, 24, 68, 0.08);
        overflow: hidden;
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
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="results-hero">
        <h1>Resultados Da Dinâmica Da Turma</h1>
        <p>Análise agregada dos tempos, memória e comportamento dos algoritmos nos grafos da turma.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

uploaded_files = st.file_uploader(
    "Importar CSVs Da Turma",
    type=["csv"],
    accept_multiple_files=True,
    help="Selecione um ou mais arquivos baixados na página da dinâmica.",
)

if not uploaded_files:
    st.info("Importe os CSVs da turma para gerar a tabela consolidada e os gráficos.")
    st.stop()

frames: list[pd.DataFrame] = []
errors: list[str] = []
for uploaded_file in uploaded_files:
    dataframe, error = read_uploaded_csv(uploaded_file)
    if error:
        errors.append(error)
    elif dataframe is not None:
        frames.append(dataframe)

if errors:
    for error in errors:
        st.error(error)

if not frames:
    st.stop()

df = pd.concat(frames, ignore_index=True)
df["Categoria Do Grafo"] = pd.Categorical(
    df["Categoria Do Grafo"],
    categories=CATEGORY_ORDER,
    ordered=True,
)
df = df.sort_values(["Categoria Do Grafo", "Vértices", "Algoritmo", "Seed"])

summary_cols = st.columns(4)
with summary_cols[0]:
    render_summary_card("Arquivos Importados", str(len(frames)), "CSVs válidos da dinâmica")
with summary_cols[1]:
    render_summary_card("Participantes", str(df["Seed"].nunique()), "Seeds únicas importadas")
with summary_cols[2]:
    render_summary_card("Registros", str(len(df)), "Linhas consolidadas")
with summary_cols[3]:
    render_summary_card(
        "Categorias",
        str(df["Categoria Do Grafo"].nunique()),
        "Pequeno, médio e grande",
    )

with st.container(key="collective_charts_panel"):
    render_chart_title("Resultados Coletivos", "summary", featured=True)
    col_time, col_memory = st.columns(2)

    with col_time:
        render_chart_title("Tempo Médio Por Categoria", "time")
        time_group = (
            df.groupby(["Categoria Do Grafo", "Algoritmo"], observed=True)["Tempo Médio (s)"]
            .mean()
            .reset_index()
        )
        fig_time = px.bar(
            time_group,
            x="Categoria Do Grafo",
            y="Tempo Médio (s)",
            color="Algoritmo",
            barmode="group",
            category_orders={"Categoria Do Grafo": CATEGORY_ORDER},
            color_discrete_map=COLOR_MAP,
            labels={
                "Categoria Do Grafo": "Categoria Do Grafo",
                "Tempo Médio (s)": "Tempo Médio (s)",
                "Algoritmo": "Algoritmo",
            },
        )
        fig_time.update_traces(
            marker_line_color="#FFFFFF",
            marker_line_width=1.2,
            opacity=0.94,
            hovertemplate="Categoria: %{x}<br>Tempo médio: %{y:.6f} s<extra>%{fullData.name}</extra>",
        )
        fig_time.update_layout(bargap=0.28, bargroupgap=0.08)
        style_chart(fig_time, height=390)
        st.plotly_chart(fig_time, width="stretch", config={"displayModeBar": False})

    with col_memory:
        render_chart_title("Memória Média Por Categoria", "memory")
        memory_group = (
            df.groupby(["Categoria Do Grafo", "Algoritmo"], observed=True)["Memória Média (KB)"]
            .mean()
            .reset_index()
        )
        fig_memory = px.bar(
            memory_group,
            x="Categoria Do Grafo",
            y="Memória Média (KB)",
            color="Algoritmo",
            barmode="group",
            category_orders={"Categoria Do Grafo": CATEGORY_ORDER},
            color_discrete_map=COLOR_MAP,
            labels={
                "Categoria Do Grafo": "Categoria Do Grafo",
                "Memória Média (KB)": "Memória Média (KB)",
                "Algoritmo": "Algoritmo",
            },
        )
        fig_memory.update_traces(
            marker_line_color="#FFFFFF",
            marker_line_width=1.2,
            opacity=0.94,
            hovertemplate="Categoria: %{x}<br>Memória média: %{y:.2f} KB<extra>%{fullData.name}</extra>",
        )
        fig_memory.update_layout(bargap=0.28, bargroupgap=0.08)
        style_chart(fig_memory, height=390)
        st.plotly_chart(fig_memory, width="stretch", config={"displayModeBar": False})

    col_scatter, col_ratio = st.columns(2)

    with col_scatter:
        render_chart_title("Vértices X Tempo Médio", "scatter")
        fig_scatter = px.scatter(
            df,
            x="Vértices",
            y="Tempo Médio (s)",
            color="Algoritmo",
            symbol="Categoria Do Grafo",
            category_orders={"Categoria Do Grafo": CATEGORY_ORDER},
            color_discrete_map=COLOR_MAP,
            hover_data=["Arquivo", "Seed", "Categoria Do Grafo", "Arestas"],
            labels={
                "Vértices": "Vértices",
                "Tempo Médio (s)": "Tempo Médio (s)",
                "Algoritmo": "Algoritmo",
            },
        )
        fig_scatter.update_traces(
            marker=dict(size=10, line=dict(color="#FFFFFF", width=1.4)),
            hovertemplate=(
                "Vértices: %{x}<br>"
                "Tempo médio: %{y:.6f} s<br>"
                "Arquivo: %{customdata[0]}<br>"
                "Seed: %{customdata[1]}<br>"
                "Categoria: %{customdata[2]}<br>"
                "Arestas: %{customdata[3]}<extra>%{fullData.name}</extra>"
            ),
        )
        style_chart(fig_scatter, height=390)
        st.plotly_chart(fig_scatter, width="stretch", config={"displayModeBar": False})

    with col_ratio:
        render_chart_title("Razão Floyd / Dijkstra", "ratio")
        ratio_df = build_ratio_dataframe(df)
        ratio_group = (
            ratio_df.groupby("Categoria Do Grafo", observed=True)["Razão Floyd / Dijkstra"]
            .mean()
            .reset_index()
        )
        fig_ratio = px.bar(
            ratio_group,
            x="Categoria Do Grafo",
            y="Razão Floyd / Dijkstra",
            category_orders={"Categoria Do Grafo": CATEGORY_ORDER},
            color_discrete_sequence=["#D19600"],
            labels={
                "Categoria Do Grafo": "Categoria Do Grafo",
                "Razão Floyd / Dijkstra": "Floyd / Dijkstra",
            },
        )
        fig_ratio.add_hline(
            y=1,
            line_dash="dash",
            line_color="#7288AE",
            annotation_text="Mesmo tempo",
            annotation_position="top left",
        )
        fig_ratio.update_traces(
            marker_line_color="#FFFFFF",
            marker_line_width=1.2,
            opacity=0.94,
            hovertemplate="Categoria: %{x}<br>Razão: %{y:.2f}x<extra></extra>",
        )
        fig_ratio.update_layout(bargap=0.36, showlegend=False)
        style_chart(fig_ratio, height=390)
        st.plotly_chart(fig_ratio, width="stretch", config={"displayModeBar": False})

with st.container(key="collective_table_panel"):
    render_chart_title(
        "Tabela Consolidada",
        "summary",
        featured=True,
        tooltip="Reúne todos os CSVs importados em uma única tabela para conferência detalhada depois da análise gráfica.",
    )
    st.dataframe(
        df,
        width="stretch",
        hide_index=True,
        column_config={
            "Densidade": st.column_config.NumberColumn(format="%.2f"),
            "Tempo Médio (s)": st.column_config.NumberColumn(format="%.6f"),
            "Memória Média (KB)": st.column_config.NumberColumn(format="%.2f"),
        },
    )
