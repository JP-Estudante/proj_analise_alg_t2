"""Entrada principal do app Streamlit."""

from __future__ import annotations

import streamlit as st


st.set_page_config(
    page_title="Comparação De Caminhos Mínimos",
    layout="wide",
    initial_sidebar_state="collapsed",
)

page = st.navigation(
    [
        st.Page(
            "app_pages/dashboard.py",
            title="Dashboard",
            icon=":material/analytics:",
            default=True,
        ),
        st.Page(
            "app_pages/dinamica.py",
            title="Dinâmica Da Turma",
            icon=":material/groups:",
            url_path="dinamica",
            visibility="hidden",
        ),
        st.Page(
            "app_pages/resultados_dinamica.py",
            title="Resultados Da Dinâmica",
            icon=":material/query_stats:",
            url_path="resultados-dinamica",
            visibility="hidden",
        ),
    ],
    position="hidden",
)

page.run()
