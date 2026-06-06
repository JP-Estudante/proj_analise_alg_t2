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


DENSITY_SWEEP_MAX_VERTICES = 80


ROUTE_ICON_SVG = """
<svg viewBox="0 0 470 496" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <path d="M440.988 29.5232C452.569 41.5931 458.996 57.6967 458.908 74.4232C458.96 91.5847 452.287 108.084 440.318 120.383L395.848 173.363L352.038 121.043C327.918 96.1432 328.148 55.2932 352.708 30.1832C358.49 24.1446 365.431 19.3344 373.115 16.0405C380.799 12.7466 389.068 11.0367 397.428 11.0132C405.562 11.0045 413.613 12.6396 421.098 15.8205C428.584 19.0013 435.349 23.6622 440.988 29.5232ZM427.448 71.2332C427.449 65.1149 425.636 59.1336 422.238 54.0458C418.839 48.958 414.009 44.9922 408.356 42.6499C402.704 40.3076 396.484 39.694 390.483 40.8867C384.482 42.0793 378.97 45.0247 374.643 49.3503C370.316 53.676 367.368 59.1876 366.174 65.1882C364.979 71.1888 365.591 77.4089 367.931 83.0619C370.272 88.7149 374.236 93.5469 379.323 96.947C384.409 100.347 390.39 102.162 396.508 102.163C400.571 102.164 404.594 101.364 408.347 99.8103C412.101 98.2563 415.511 95.9782 418.384 93.1061C421.257 90.234 423.536 86.8241 425.092 83.0712C426.647 79.3182 427.448 75.2957 427.448 71.2332Z" fill="#FFF8DD"/>
    <path d="M396.508 40.3032C402.626 40.3032 408.606 42.1172 413.692 45.5159C418.779 48.9145 422.743 53.7451 425.084 59.3968C427.425 65.0485 428.037 71.2675 426.844 77.2674C425.651 83.2672 422.705 88.7784 418.379 93.104C414.054 97.4297 408.542 100.375 402.543 101.569C396.543 102.762 390.324 102.15 384.672 99.8088C379.02 97.4678 374.19 93.5034 370.791 88.417C367.392 83.3306 365.578 77.3506 365.578 71.2332C365.58 63.0305 368.839 55.1641 374.639 49.3639C380.439 43.5637 388.306 40.3045 396.508 40.3032Z" fill="#D19600"/>
    <path d="M121.578 336.053C133.567 348.539 140.221 365.204 140.128 382.513C140.179 400.269 133.272 417.339 120.888 430.063L74.9284 484.813H74.8284L29.5484 430.743C4.59841 404.983 4.82841 362.723 30.2384 336.733C36.2206 330.486 43.4018 325.509 51.3522 322.102C59.3025 318.695 67.8587 316.926 76.5084 316.903C84.9236 316.894 93.2538 318.585 100.999 321.876C108.744 325.167 115.744 329.989 121.578 336.053ZM107.568 379.213C107.568 372.884 105.692 366.697 102.175 361.435C98.6592 356.173 93.6615 352.071 87.8143 349.649C81.967 347.227 75.5329 346.593 69.3255 347.828C63.1181 349.063 57.4163 352.111 52.941 356.586C48.4657 361.061 45.418 366.763 44.1833 372.97C42.9486 379.178 43.5823 385.612 46.0043 391.459C48.4263 397.306 52.5278 402.304 57.7902 405.82C63.0525 409.336 69.2394 411.213 75.5684 411.213C84.0549 411.212 92.1932 407.84 98.1941 401.839C104.195 395.838 107.567 387.7 107.568 379.213Z" fill="#FFF8DD"/>
    <path d="M75.5684 347.203C81.8984 347.202 88.0865 349.078 93.3502 352.594C98.614 356.11 102.717 361.108 105.14 366.956C107.564 372.804 108.198 379.239 106.964 385.447C105.73 391.656 102.683 397.359 98.2078 401.836C93.7326 406.312 88.0303 409.361 81.8221 410.597C75.614 411.833 69.1787 411.2 63.3302 408.779C57.4817 406.357 52.4825 402.256 48.965 396.993C45.4474 391.731 43.5693 385.543 43.5684 379.213C43.5673 370.725 46.9381 362.584 52.9392 356.581C58.9403 350.578 67.0802 347.205 75.5684 347.203Z" fill="#D19600"/>
    <path d="M67.1814 491.256C68.1156 492.398 69.2894 493.319 70.6195 493.957C71.9496 494.594 73.4036 494.931 74.8784 494.943C75.2424 494.943 75.6034 494.943 75.9604 494.943H163.278C175.104 494.909 186.436 490.201 194.806 481.847C203.175 473.493 207.903 462.169 207.958 450.343V275.643C207.943 272.393 208.573 269.172 209.811 266.166C211.048 263.161 212.87 260.43 215.17 258.133C217.47 255.836 220.202 254.018 223.209 252.784C226.216 251.55 229.438 250.924 232.688 250.943H233.638C247.39 250.943 258.958 261.891 258.958 275.643V402.003C258.958 413.938 263.7 425.384 272.139 433.823C280.578 442.262 292.024 447.003 303.958 447.003C315.893 447.003 327.339 442.262 335.778 433.823C344.217 425.384 348.958 413.938 348.958 402.003V208.153C348.912 204.981 349.498 201.832 350.683 198.889C351.869 195.947 353.629 193.27 355.86 191.016C358.092 188.761 360.751 186.975 363.682 185.76C366.613 184.546 369.786 182.928 372.958 182.943L395.848 182.943L395.958 183.358C395.906 183.224 395.868 183.085 395.842 182.943H395.848C397.294 182.982 398.73 182.701 400.054 182.12C401.378 181.539 402.558 180.673 403.507 179.582L447.742 126.987C461.401 112.887 468.999 94.001 468.908 74.3703C469.024 55.0506 461.583 36.4512 448.172 22.5433C441.61 15.7085 433.729 10.2755 425.008 6.57268C416.286 2.86988 406.904 0.974212 397.428 1.00026C387.733 1.00451 378.138 2.97229 369.224 6.78495C360.309 10.5976 352.259 16.1762 345.558 23.1843C317.325 52.0503 316.923 98.9933 344.594 127.852L374.708 163.943H372.928C367.131 163.931 361.388 165.068 356.032 167.289C350.676 169.509 345.814 172.769 341.725 176.88C337.636 180.991 334.403 185.871 332.212 191.239C330.021 196.607 328.915 202.356 328.958 208.153V402.003C328.921 405.296 328.235 408.549 326.938 411.576C325.641 414.603 323.76 417.344 321.401 419.642C319.103 421.964 316.366 423.805 313.35 425.058C310.333 426.311 307.097 426.952 303.83 426.942C297.225 426.932 290.895 424.299 286.231 419.623C281.567 414.946 278.951 408.608 278.958 402.003V275.643C278.958 250.863 258.418 230.943 233.638 230.943H232.688C226.812 230.927 220.991 232.072 215.559 234.312C210.127 236.553 205.19 239.844 201.034 243.998C196.878 248.151 193.583 253.085 191.339 258.516C189.095 263.947 187.946 269.767 187.958 275.643V450.343C187.908 456.866 185.29 463.106 180.67 467.711C176.05 472.316 169.801 474.915 163.278 474.943H96.3784L128.311 436.843C142.391 422.284 150.221 402.797 150.128 382.543C150.252 362.626 142.583 343.451 128.758 329.112C122.001 322.073 113.887 316.476 104.906 312.661C95.9246 308.845 86.2633 306.89 76.5054 306.912C66.5213 306.913 56.6408 308.936 47.4601 312.86C38.2794 316.784 29.9888 322.527 23.0884 329.743C-5.98858 359.484 -6.40058 407.708 22.1044 437.429L67.1814 491.256ZM359.221 114.086C338.756 92.9593 339.041 58.4583 359.888 37.1443C364.732 32.0594 370.555 28.0085 377.007 25.2361C383.459 22.4636 390.406 21.0271 397.428 21.0133C404.222 20.9984 410.948 22.3612 417.2 25.0191C423.451 27.677 429.1 31.5749 433.802 36.4773C443.594 46.6716 449.015 60.2885 448.908 74.4233C448.988 88.9763 443.333 102.975 433.169 113.391C432.992 113.572 432.821 113.76 432.659 113.954L395.859 157.797L359.705 114.623C359.551 114.437 359.389 114.258 359.221 114.086ZM37.4204 343.692C42.4634 338.398 48.527 334.181 55.2452 331.295C61.9634 328.41 69.1968 326.916 76.5084 326.903C83.5845 326.888 90.5901 328.308 97.1021 331.076C103.614 333.845 109.497 337.904 114.396 343.01C124.595 353.619 130.241 367.795 130.128 382.51C130.209 397.658 124.321 412.229 113.738 423.068C113.562 423.25 113.393 423.438 113.229 423.63L74.8874 469.308L37.2154 424.322C37.0601 424.138 36.8984 423.959 36.7304 423.785C15.4324 401.795 15.7274 365.88 37.4204 343.692Z" fill="#111844"/>
    <path d="M395.848 182.943L372.958 182.943C369.786 182.928 366.613 184.546 363.682 185.76C360.751 186.975 358.092 188.761 355.86 191.016C353.629 193.27 351.869 195.947 350.683 198.889C349.498 201.832 348.912 204.981 348.958 208.153V402.003C348.958 413.938 344.217 425.384 335.778 433.823C327.339 442.262 315.893 447.003 303.958 447.003C292.024 447.003 280.578 442.262 272.139 433.823C263.7 425.384 258.958 413.938 258.958 402.003V275.643C258.958 261.891 247.39 250.943 233.638 250.943H232.688C229.438 250.924 226.216 251.55 223.209 252.784C220.202 254.018 217.47 255.836 215.17 258.133C212.87 260.43 211.048 263.161 209.811 266.166C208.573 269.172 207.943 272.393 207.958 275.643V450.343C207.903 462.169 203.175 473.493 194.806 481.847C186.436 490.201 175.104 494.909 163.278 494.943H75.9604C75.6034 494.943 75.2424 494.943 74.8784 494.943C73.4036 494.931 71.9496 494.594 70.6195 493.957C69.2894 493.319 68.1156 492.398 67.1814 491.256L22.1044 437.429C-6.40058 407.708 -5.98858 359.484 23.0884 329.743C29.9888 322.527 38.2794 316.784 47.4601 312.86C56.6408 308.936 66.5213 306.913 76.5054 306.912C86.2633 306.89 95.9246 308.845 104.906 312.661C113.887 316.476 122.001 322.073 128.758 329.112C142.583 343.451 150.252 362.626 150.128 382.543C150.221 402.797 142.391 422.284 128.311 436.843L96.3784 474.943H163.278C169.801 474.915 176.05 472.316 180.67 467.711C185.29 463.106 187.908 456.866 187.958 450.343V275.643C187.946 269.767 189.095 263.947 191.339 258.516C193.583 253.085 196.878 248.151 201.034 243.998C205.19 239.844 210.127 236.553 215.559 234.312C220.991 232.072 226.812 230.927 232.688 230.943H233.638C258.418 230.943 278.958 250.863 278.958 275.643V402.003C278.951 408.608 281.567 414.946 286.231 419.623C290.895 424.299 297.225 426.932 303.83 426.942C307.097 426.952 310.333 426.311 313.35 425.058C316.366 423.805 319.103 421.964 321.401 419.642C323.76 417.344 325.641 414.603 326.938 411.576C328.235 408.549 328.921 405.296 328.958 402.003V208.153C328.915 202.356 330.021 196.607 332.212 191.239C334.403 185.871 337.636 180.991 341.725 176.88C345.814 172.769 350.676 169.509 356.032 167.289C361.388 165.068 367.131 163.931 372.928 163.943H374.708L344.594 127.852C316.923 98.9933 317.325 52.0503 345.558 23.1843C352.259 16.1762 360.309 10.5976 369.224 6.78495C378.138 2.97229 387.733 1.00451 397.428 1.00026C406.904 0.974212 416.286 2.86988 425.008 6.57268C433.729 10.2755 441.61 15.7085 448.172 22.5433C461.583 36.4512 469.024 55.0506 468.908 74.3703C468.999 94.001 461.401 112.887 447.742 126.987L403.507 179.582C402.558 180.673 401.378 181.539 400.054 182.12C398.73 182.701 397.294 182.982 395.848 182.943ZM395.848 182.943L395.958 183.358C395.906 183.224 395.868 183.085 395.842 182.943H395.848ZM359.221 114.086C338.756 92.9593 339.041 58.4583 359.888 37.1443C364.732 32.0594 370.555 28.0085 377.007 25.2361C383.459 22.4636 390.406 21.0271 397.428 21.0133C404.222 20.9984 410.948 22.3612 417.2 25.0191C423.451 27.677 429.1 31.5749 433.802 36.4773C443.594 46.6716 449.015 60.2885 448.908 74.4233C448.988 88.9763 443.333 102.975 433.169 113.391C432.992 113.572 432.821 113.76 432.659 113.954L395.859 157.797L359.705 114.623C359.551 114.437 359.389 114.258 359.221 114.086ZM37.4204 343.692C42.4634 338.398 48.527 334.181 55.2452 331.295C61.9634 328.41 69.1968 326.916 76.5084 326.903C83.5845 326.888 90.5901 328.308 97.1021 331.076C103.614 333.845 109.497 337.904 114.396 343.01C124.595 353.619 130.241 367.795 130.128 382.51C130.209 397.658 124.321 412.229 113.738 423.068C113.562 423.25 113.393 423.438 113.229 423.63L74.8874 469.308L37.2154 424.322C37.0601 424.138 36.8984 423.959 36.7304 423.785C15.4324 401.795 15.7274 365.88 37.4204 343.692Z" stroke="#7288AE" stroke-width="2"/>
    <path d="M75.5685 421.213C83.8767 421.214 91.9986 418.751 98.9071 414.136C105.816 409.521 111.2 402.961 114.38 395.285C117.56 387.61 118.392 379.163 116.772 371.015C115.151 362.866 111.15 355.381 105.275 349.506C99.4007 343.631 91.9157 339.631 83.767 338.01C75.6184 336.389 67.1722 337.222 59.4966 340.402C51.8209 343.582 45.2607 348.966 40.6455 355.875C36.0303 362.783 33.5675 370.905 33.5685 379.213C33.5809 390.349 38.0099 401.024 45.8837 408.898C53.7576 416.772 64.4332 421.201 75.5685 421.213ZM75.5685 357.203C79.9207 357.202 84.1754 358.492 87.7946 360.909C91.4139 363.326 94.2351 366.762 95.9015 370.783C97.568 374.803 98.0047 379.228 97.1566 383.496C96.3085 387.765 94.2137 391.686 91.1369 394.765C88.0601 397.843 84.1397 399.939 79.8713 400.789C75.603 401.639 71.1784 401.205 67.1572 399.54C63.1359 397.876 59.6985 395.056 57.2798 391.438C54.861 387.82 53.5695 383.565 53.5685 379.213C53.5735 373.379 55.8927 367.785 60.0171 363.659C64.1415 359.533 69.7343 357.211 75.5685 357.203ZM437.448 71.2332C437.449 63.1371 435.05 55.2224 430.552 48.4901C426.055 41.7578 419.663 36.5103 412.183 33.4111C404.704 30.312 396.473 29.5003 388.532 31.0788C380.592 32.6573 373.297 36.5551 367.572 42.2793C361.846 48.0034 357.946 55.2969 356.366 63.2373C354.786 71.1777 355.595 79.4085 358.693 86.8888C361.79 94.369 367.036 100.763 373.767 105.262C380.498 109.76 388.412 112.162 396.508 112.163C407.361 112.152 417.767 107.837 425.442 100.163C433.117 92.4903 437.435 82.0861 437.448 71.2332ZM375.578 71.2332C375.578 67.0923 376.805 63.044 379.105 59.6005C381.405 56.157 384.674 53.4729 388.5 51.8878C392.325 50.3026 396.535 49.8876 400.596 50.6952C404.658 51.5029 408.389 53.4968 411.317 56.425C414.245 59.3531 416.239 63.0838 417.046 67.1452C417.854 71.2067 417.439 75.4164 415.854 79.242C414.269 83.0676 411.585 86.3371 408.141 88.6371C404.698 90.9371 400.649 92.1642 396.508 92.1632C390.959 92.1569 385.64 89.9497 381.716 86.026C377.792 82.1022 375.585 76.7823 375.578 71.2332Z" fill="#083863"/>
</svg>
"""


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
        --accent: #7AE2CF;
        --accent-rgb: 122, 226, 207;
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

    div[data-testid="stToolbar"] {
        position: relative;
        min-height: 3.25rem;
        background: linear-gradient(90deg, #FFFFFF 0%, #FFF8DD 100%);
        border-bottom: 1px solid rgba(17, 24, 68, 0.10);
    }

    .toolbar-title-overlay {
        align-items: center;
        display: flex;
        gap: 0.55rem;
        height: 3.25rem;
        justify-content: center;
        left: 50%;
        max-width: calc(100vw - 18rem);
        pointer-events: none;
        position: fixed;
        top: 0;
        transform: translateX(-50%);
        z-index: 999999;
    }

    .toolbar-title-icon {
        align-items: center;
        display: inline-flex;
        height: 1.75rem;
        justify-content: center;
        width: 1.75rem;
    }

    .toolbar-title-icon svg {
        display: block;
        height: 100%;
        width: 100%;
    }

    .toolbar-title-text {
        color: var(--primary);
        font-size: 0.95rem;
        font-weight: 900;
        letter-spacing: 0.03em;
        line-height: 1;
        text-transform: uppercase;
        white-space: nowrap;
    }

    @media (max-width: 720px) {
        .toolbar-title-overlay {
            gap: 0.4rem;
            max-width: calc(100vw - 8.5rem);
        }

        .toolbar-title-icon {
            height: 1.45rem;
            width: 1.45rem;
        }

        .toolbar-title-text {
            font-size: 0.78rem;
            overflow: hidden;
            text-overflow: ellipsis;
        }
    }

    h1, h2, h3, p, label, span {
        letter-spacing: 0;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF8DD 100%);
        border-right: 1px solid rgba(17, 24, 68, 0.12);
        box-shadow: 8px 0 28px rgba(17, 24, 68, 0.10);
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarHeader"] {
        height: 0 !important;
        min-height: 0 !important;
        padding: 0 !important;
        position: relative;
        z-index: 20;
    }

    section[data-testid="stSidebar"] div[data-testid="stLogoSpacer"] {
        display: none !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] {
        position: absolute;
        right: 0.65rem;
        top: 0.55rem;
        z-index: 30;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] button {
        background: rgba(255, 255, 255, 0.86) !important;
        border-radius: 8px !important;
        box-shadow: 0 8px 18px rgba(17, 24, 68, 0.14);
    }

    section[data-testid="stSidebar"] > div:first-child,
    section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {
        padding-top: 0 !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarUserContent"] {
        padding-top: 0.15rem !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.85rem;
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span {
        color: var(--text);
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] {
        background: #FFFFFF;
        border: 1px solid rgba(17, 24, 68, 0.16);
        border-radius: 8px;
        box-shadow: 0 8px 18px rgba(17, 24, 68, 0.06);
        overflow: hidden;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within {
        border-color: #111844 !important;
        box-shadow: 0 0 0 2px rgba(17, 24, 68, 0.18);
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within *,
    section[data-testid="stSidebar"] div[data-baseweb="input"] input:focus {
        border-color: #111844 !important;
        outline-color: #111844 !important;
    }

    section[data-testid="stSidebar"] div[data-baseweb="input"] input {
        background: transparent;
        border: 0 !important;
        box-shadow: none !important;
        color: var(--text);
        outline: none !important;
    }

    .sidebar-title-card {
        background:
            linear-gradient(135deg, rgba(17, 24, 68, 0.96), rgba(29, 42, 104, 0.96)),
            #111844;
        border-radius: 12px;
        box-shadow: 0 16px 28px rgba(17, 24, 68, 0.22);
        margin: 0 0 0 0;
        padding: 16px 16px 14px 16px;
    }

    .sidebar-title-divider {
        align-items: center;
        display: flex;
        gap: 8px;
        margin: 0.72rem 0 0.9rem 0;
    }

    .sidebar-title-divider::before,
    .sidebar-title-divider::after {
        background: rgba(17, 24, 68, 0.12);
        content: "";
        flex: 1;
        height: 1px;
    }

    .sidebar-title-divider span {
        background: var(--accent);
        border-radius: 999px;
        box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.16);
        display: inline-block;
        height: 7px;
        width: 7px;
    }

    .sidebar-kicker {
        color: #7AE2CF;
        font-size: 0.72rem;
        font-weight: 900;
        letter-spacing: 0.06em;
        line-height: 1;
        margin-bottom: 8px;
        text-transform: uppercase;
    }

    .sidebar-title-card .sidebar-title {
        color: #FFFBEB !important;
        font-size: 1.08rem;
        font-weight: 900;
        line-height: 1.1;
    }

    .sidebar-summary {
        background: rgba(255, 255, 255, 0.66);
        border: 1px solid rgba(17, 24, 68, 0.14);
        border-radius: 12px;
        box-shadow: 0 14px 26px rgba(17, 24, 68, 0.08);
        margin-top: 0.25rem;
        padding: 12px;
    }

    .sidebar-summary-title {
        align-items: center;
        color: #111844;
        display: flex;
        font-size: 0.78rem;
        font-weight: 900;
        justify-content: space-between;
        letter-spacing: 0.04em;
        margin-bottom: 9px;
        text-transform: uppercase;
    }

    .sidebar-summary-title::after {
        background: var(--accent);
        border-radius: 999px;
        content: "";
        height: 6px;
        width: 36px;
    }

    .sidebar-summary-row {
        align-items: center;
        border-top: 1px solid rgba(17, 24, 68, 0.08);
        display: flex;
        justify-content: space-between;
        gap: 10px;
        padding: 8px 0;
    }

    .sidebar-summary-row:first-of-type {
        border-top: 0;
        padding-top: 0;
    }

    .sidebar-summary-label {
        color: #7288AE;
        font-size: 0.76rem;
        font-weight: 800;
    }

    .sidebar-summary-value {
        color: #111844;
        font-size: 0.82rem;
        font-weight: 900;
        text-align: right;
        white-space: nowrap;
    }

    .sidebar-status {
        align-items: center;
        background: rgba(122, 226, 207, 0.18);
        border: 1px solid rgba(17, 24, 68, 0.10);
        border-radius: 999px;
        color: #111844;
        display: flex;
        font-size: 0.76rem;
        font-weight: 800;
        gap: 6px;
        margin-top: 8px;
        padding: 8px 10px;
    }

    .sidebar-status-dot {
        background: var(--accent);
        border-radius: 999px;
        box-shadow: 0 0 0 4px rgba(var(--accent-rgb), 0.18);
        height: 7px;
        width: 7px;
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

    .hero-title {
        align-items: center;
        display: flex;
        gap: 0.85rem;
        margin: 0;
    }

    .hero-title-icon {
        align-items: center;
        display: inline-flex;
        flex: 0 0 auto;
        height: clamp(2.4rem, 4.5vw, 3.6rem);
        justify-content: center;
        width: clamp(2.25rem, 4.3vw, 3.4rem);
    }

    .hero-title-icon svg {
        display: block;
        height: 100%;
        width: 100%;
    }

    @media (max-width: 720px) {
        .hero-title {
            align-items: flex-start;
            gap: 0.65rem;
        }
    }

    .metric-card {
        min-height: 112px;
        padding: 18px 18px 16px 18px;
        border: 1px solid rgba(17, 24, 68, 0.16);
        border-top: 4px solid var(--accent);
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
        position: relative;
        width: 26px;
        height: 26px;
        border-radius: 8px;
        background: #111844;
        color: #FFFBEB;
        font-size: 0.86rem;
        font-weight: 900;
        line-height: 1;
    }

    .graph-icon {
        width: 18px;
        height: 18px;
        display: block;
        color: #FFFBEB;
    }

    .graph-icon svg {
        width: 100%;
        height: 100%;
        display: block;
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

    .st-key-main_charts_panel,
    .st-key-complementary_panel {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.60), rgba(255, 253, 243, 0.86)),
            rgba(122, 226, 207, 0.10);
        border: 1px solid rgba(17, 24, 68, 0.14);
        border-left: 6px solid var(--accent);
        border-radius: 12px;
        box-shadow: 0 18px 38px rgba(17, 24, 68, 0.10);
        margin-top: 26px;
        padding: 0 14px 16px 14px;
        overflow: hidden;
    }

    .st-key-main_charts_panel .chart-heading--featured,
    .st-key-complementary_panel .chart-heading--featured {
        border-left: 0;
        border-radius: 0;
        margin: 0 -14px 18px -14px;
    }

    div[data-testid="stPlotlyChart"] {
        background:
            linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(255, 253, 243, 0.98));
        border: 1px solid rgba(17, 24, 68, 0.12);
        border-radius: 12px;
        box-sizing: border-box;
        overflow: hidden;
        box-shadow: 0 16px 32px rgba(17, 24, 68, 0.10);
        padding: 10px 12px 2px 12px;
    }

    div[data-testid="stPlotlyChart"] > div,
    div[data-testid="stPlotlyChart"] .js-plotly-plot,
    div[data-testid="stPlotlyChart"] .plot-container,
    div[data-testid="stPlotlyChart"] .svg-container {
        max-width: 100%;
        overflow: hidden !important;
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


@st.cache_data(show_spinner=False)
def cached_density_benchmark(
    vertices: int,
    densities: tuple[float, ...],
    repetitions: int,
    seed: int,
) -> pd.DataFrame:
    rows = []
    for density_value in densities:
        results = run_benchmarks([vertices], density_value, repetitions, seed)
        rows.extend(summarize_results(results))
    return pd.DataFrame(rows)


def build_density_points(current_density: float) -> tuple[float, ...]:
    base_points = {0.15, 0.35, 0.55, 0.75, round(current_density, 2)}
    return tuple(sorted(point for point in base_points if 0.05 <= point <= 1.0))


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


CHART_ICONS = {
    "time": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="12" cy="12" r="8" stroke="currentColor" stroke-width="2"/>
            <path d="M12 7v5l3 2" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"/>
        </svg>
    """,
    "memory": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <rect x="6" y="5" width="12" height="14" rx="2" stroke="currentColor" stroke-width="2"/>
            <path d="M9 9h6M9 13h6M4 8h2M4 12h2M4 16h2M18 8h2M18 12h2M18 16h2" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
        </svg>
    """,
    "comparison": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M5 18V9M12 18V5M19 18v-6" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
            <path d="M4 19h16" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
        </svg>
    """,
    "algorithm": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M5 18V8M12 18V5M19 18v-7" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
            <path d="M3 18h18" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
        </svg>
    """,
    "ratio": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M6 7h12M6 17h12" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
            <circle cx="9" cy="12" r="1.4" fill="currentColor"/>
            <circle cx="15" cy="12" r="1.4" fill="currentColor"/>
        </svg>
    """,
    "edges": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <circle cx="6" cy="7" r="2.2" stroke="currentColor" stroke-width="2"/>
            <circle cx="18" cy="7" r="2.2" stroke="currentColor" stroke-width="2"/>
            <circle cx="12" cy="18" r="2.2" stroke="currentColor" stroke-width="2"/>
            <path d="M8 8l3 8M16 8l-3 8M8.2 7h7.6" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
        </svg>
    """,
    "density": """
        <svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
            <path d="M4 19V5M4 19h16" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
            <circle cx="8" cy="13" r="2" stroke="currentColor" stroke-width="2"/>
            <circle cx="16" cy="8" r="2" stroke="currentColor" stroke-width="2"/>
            <circle cx="16" cy="16" r="2" stroke="currentColor" stroke-width="2"/>
            <path d="M10 13.6l4 1.8M16.5 10l-.5 4" stroke="currentColor" stroke-linecap="round" stroke-width="2"/>
        </svg>
    """,
}


CHART_TOOLTIPS = {
    "Resultados Principais": "Reúne os dois gráficos centrais da comparação: tempo médio de execução e uso aproximado de memória.",
    "Tempo Médio De Execução": "Mostra quanto tempo, em média, cada algoritmo levou para resolver os grafos de cada tamanho.",
    "Uso Aproximado De Memória": "Mostra o pico médio de memória usado por cada algoritmo durante a execução.",
    "Comparações Complementares": "Reúne gráficos auxiliares para observar os resultados por outros pontos de vista.",
    "Tempo Por Algoritmo": "Compara, em barras, o tempo médio dos algoritmos em cada tamanho de grafo.",
    "Razão De Tempo": "Mostra quantas vezes o Floyd-Warshall foi mais lento ou mais rápido que o Dijkstra. Valor 1 significa empate.",
    "Distribuição De Arestas": "Mostra como o total de arestas está distribuído entre os tamanhos de grafo testados.",
    "Tempo Por Densidade": "Mostra como o tempo muda quando o grafo fica mais ou menos conectado.",
    "Tempo Por Arestas": "Mostra a relação entre a quantidade de arestas do grafo e o tempo médio de execução.",
}


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
        margin=dict(l=18, r=18, t=34, b=16),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFDF3",
        font=dict(color="#111844", family="Arial, sans-serif", size=12),
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
        linecolor="rgba(17, 24, 68, 0.32)",
        showline=True,
        tickfont=dict(color="#7288AE", size=11),
        title_font=dict(color="#7288AE", size=12),
        zeroline=False,
    )
    fig.update_yaxes(
        gridcolor="rgba(230, 217, 155, 0.68)",
        linecolor="rgba(17, 24, 68, 0.22)",
        showline=True,
        tickfont=dict(color="#7288AE", size=11),
        title_font=dict(color="#7288AE", size=12),
        zerolinecolor="#7AE2CF",
        zerolinewidth=1.2,
    )


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
    f"""
    <div class="toolbar-title-overlay">
        <span class="toolbar-title-text">Problema Do Caminho Mínimo</span>
    </div>
    <div class="hero">
        <h1 class="hero-title">
            <span class="hero-title-icon">{ROUTE_ICON_SVG}</span>
            <span>Dijkstra X Floyd-Warshall</span>
        </h1>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-title-card">
            <div class="sidebar-kicker">Configuração</div>
            <div class="sidebar-title">Parâmetros Dos Testes</div>
        </div>
        <div class="sidebar-title-divider"><span></span></div>
        """,
        unsafe_allow_html=True,
    )
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
        sidebar_sizes = parse_sizes(raw_sizes)
        sidebar_largest = max(sidebar_sizes)
        sidebar_total_executions = len(sidebar_sizes) * repetitions * 2
        sidebar_max_edges = sidebar_largest * (sidebar_largest - 1)
        sidebar_edges = max(sidebar_largest, round(sidebar_max_edges * density))
        sidebar_sizes_text = ", ".join(str(size) for size in sidebar_sizes)
    except ValueError:
        sidebar_largest = "-"
        sidebar_total_executions = "-"
        sidebar_edges = "-"
        sidebar_sizes_text = "Inválido"

    st.markdown(
        f"""
        <div class="sidebar-summary">
            <div class="sidebar-summary-title">Resumo</div>
            <div class="sidebar-summary-row">
                <span class="sidebar-summary-label">Vértices</span>
                <span class="sidebar-summary-value">{sidebar_sizes_text}</span>
            </div>
            <div class="sidebar-summary-row">
                <span class="sidebar-summary-label">Maior Grafo</span>
                <span class="sidebar-summary-value">{sidebar_largest}</span>
            </div>
            <div class="sidebar-summary-row">
                <span class="sidebar-summary-label">Arestas Previstas</span>
                <span class="sidebar-summary-value">{sidebar_edges}</span>
            </div>
            <div class="sidebar-summary-row">
                <span class="sidebar-summary-label">Execuções Totais</span>
                <span class="sidebar-summary-value">{sidebar_total_executions}</span>
            </div>
            <div class="sidebar-status">
                <span class="sidebar-status-dot"></span>
                <span>Dijkstra e Floyd-Warshall no mesmo grafo</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
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
density_analysis_size = min(largest_size, DENSITY_SWEEP_MAX_VERTICES)
density_points = build_density_points(density)
density_df = cached_density_benchmark(
    density_analysis_size,
    density_points,
    max(1, min(repetitions, 3)),
    int(seed) + 17000,
)

metric_cols = st.columns(4)
with metric_cols[0]:
    graph_icon = """
    <span class="graph-icon" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32">
            <path fill="currentColor" d="M29.08,11.01c-1.98-5.17-6.95-8.88-12.78-9-.1-.01-.2-.01-.3-.01s-.2,0-.3,.01c-5.83,.12-10.8,3.83-12.78,9-.59,1.55-.92,3.23-.92,4.99s.33,3.44,.92,4.99c1.98,5.17,6.95,8.88,12.78,9,.1,.01,.2,.01,.3,.01s.2,0,.3-.01c5.83-.12,10.8-3.83,12.78-9,.59-1.55,.92-3.23,.92-4.99s-.33-3.44-.92-4.99Zm-2.17-.01h-4.36c-.46-2.52-1.28-4.67-2.33-6.23,2.97,1.11,5.37,3.37,6.69,6.23Zm-5.91,5c0,1.05-.06,2.05-.16,3H11.17c-.11-.95-.17-1.95-.17-3s.06-2.05,.17-3h9.67c.1,.95,.16,1.95,.16,3ZM15.78,4.01c.07-.01,.15-.01,.22-.01s.15,0,.22,.01c1.7,.22,3.48,2.88,4.3,6.99H11.48c.82-4.11,2.6-6.77,4.3-6.99Zm-4,.76c-1.05,1.56-1.87,3.71-2.33,6.23H5.09c1.32-2.86,3.72-5.12,6.69-6.23Zm-7.78,11.23c0-1.03,.13-2.04,.38-3h4.78c-.11,.96-.16,1.97-.16,3s.05,2.04,.16,3H4.38c-.25-.96-.38-1.97-.38-3Zm1.09,5h4.36c.46,2.52,1.28,4.67,2.33,6.23-2.97-1.11-5.37-3.37-6.69-6.23Zm10.91,7c-.07,0-.15,0-.22-.01-1.7-.22-3.48-2.88-4.3-6.99h9.04c-.82,4.11-2.6,6.77-4.3,6.99-.07,.01-.15,.01-.22,.01Zm4.22-.77c1.05-1.56,1.87-3.71,2.33-6.23h4.36c-1.32,2.86-3.72,5.12-6.69,6.23Zm7.4-8.23h-4.78c.11-.96,.16-1.97,.16-3s-.05-2.04-.16-3h4.78c.25,.96,.38,1.97,.38,3s-.13,2.04-.38,3Z"/>
        </svg>
    </span>
    """
    render_metric_card("Maior Grafo", f"{largest_size} Vértices", f"{int(largest_df['edges'].max())} Arestas", graph_icon)
with metric_cols[1]:
    density_icon = """
    <span class="graph-icon" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none">
            <path d="M3.05273 0.75C3.49012 0.750054 3.85524 1.09764 3.85547 1.53906V16.6445C3.85547 18.5864 5.46954 20.1709 7.47363 20.1709H22.9473C23.3848 20.1709 23.75 20.5193 23.75 20.9609C23.7498 21.4024 23.3847 21.75 22.9473 21.75H7.47363C4.59441 21.75 2.25 19.4697 2.25 16.6445V1.53906C2.25023 1.0976 2.6153 0.75 3.05273 0.75Z" fill="currentColor" stroke="currentColor" stroke-width="0.5"/>
            <path d="M16 12.3496C17.4635 12.3496 18.6504 13.5365 18.6504 15C18.6504 16.4635 17.4635 17.6504 16 17.6504C14.5365 17.6504 13.3496 16.4635 13.3496 15C13.3496 13.5365 14.5365 12.3496 16 12.3496ZM16 13.6504C15.2544 13.6504 14.6504 14.2544 14.6504 15C14.6504 15.7456 15.2544 16.3496 16 16.3496C16.7456 16.3496 17.3496 15.7456 17.3496 15C17.3496 14.2544 16.7456 13.6504 16 13.6504ZM8 9.34961C9.46355 9.34961 10.6504 10.5365 10.6504 12C10.6504 13.4635 9.46355 14.6504 8 14.6504C6.53645 14.6504 5.34961 13.4635 5.34961 12C5.34961 10.5365 6.53645 9.34961 8 9.34961ZM8 10.6504C7.25441 10.6504 6.65039 11.2544 6.65039 12C6.65039 12.7456 7.25441 13.3496 8 13.3496C8.74559 13.3496 9.34961 12.7456 9.34961 12C9.34961 11.2544 8.74559 10.6504 8 10.6504ZM19 2.34961C20.4635 2.34961 21.6504 3.53645 21.6504 5C21.6504 6.46355 20.4635 7.65039 19 7.65039C17.5365 7.65039 16.3496 6.46355 16.3496 5C16.3496 3.53645 17.5365 2.34961 19 2.34961ZM19 3.65039C18.2544 3.65039 17.6504 4.25441 17.6504 5C17.6504 5.74559 18.2544 6.34961 19 6.34961C19.7456 6.34961 20.3496 5.74559 20.3496 5C20.3496 4.25441 19.7456 3.65039 19 3.65039Z" fill="currentColor" stroke="currentColor" stroke-width="0.3"/>
            <path d="M9.41882 12.7089C9.57951 12.3881 9.96995 12.2584 10.2909 12.4188L14.2909 14.4188C14.6118 14.5794 14.7414 14.9699 14.5809 15.2909C14.4203 15.6117 14.0298 15.7414 13.7089 15.5809L9.70886 13.5809C9.38816 13.4202 9.25837 13.0298 9.41882 12.7089ZM18.6581 6.36902C19.0062 6.45622 19.2177 6.80998 19.1307 7.15808L17.6307 13.1581C17.5435 13.5061 17.1906 13.7175 16.8427 13.6307C16.4945 13.5437 16.2823 13.1907 16.369 12.8427L17.869 6.84265C17.9561 6.49439 18.3098 6.28196 18.6581 6.36902Z" fill="currentColor" stroke="currentColor" stroke-width="0.3"/>
        </svg>
    </span>
    """
    render_metric_card("Densidade", f"{float(df['density'].iloc[0]):.2f}", f"{int(df['repetitions'].iloc[0])} Repetições", density_icon)
with metric_cols[2]:
    gauge_icon = """
    <span class="graph-icon" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20">
            <path fill="currentColor" d="M8.127 13.6c-.689 1.197-.225 2.18.732 2.732.956.553 2.041.465 2.732-.732.689-1.195 5.047-11.865 4.668-12.084-.379-.219-7.442 8.888-8.132 10.084zM10 6c.438 0 .864.037 1.281.109.438-.549.928-1.154 1.405-1.728A9.664 9.664 0 0 0 10 4C4.393 4 0 8.729 0 14.766c0 .371.016.742.049 1.103.049.551.54.955 1.084.908.551-.051.957-.535.908-1.086A10.462 10.462 0 0 1 2 14.766C2 9.85 5.514 6 10 6zm7.219 1.25c-.279.75-.574 1.514-.834 2.174C17.4 10.894 18 12.738 18 14.766c0 .316-.015.635-.043.943a1.001 1.001 0 0 0 1.992.182c.033-.37.051-.748.051-1.125 0-2.954-1.053-5.59-2.781-7.516z"/>
        </svg>
    </span>
    """
    render_metric_card(
        "Mais Rápido",
        short_algorithm_name(str(fastest["algorithm"])),
        f"{float(fastest['avg_time_seconds']):.6f} s No Maior Grafo",
        gauge_icon,
    )
with metric_cols[3]:
    memory_icon = """
    <span class="graph-icon" aria-hidden="true">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
            <path fill="currentColor" d="M22,14.86a0,0,0,0,1,0,0v-.05a2.61,2.61,0,0,0-.1-.57L20.26,4.51a3,3,0,0,0-3-2.51H6.69A3,3,0,0,0,3.74,4.51L2.12,14.22a2.61,2.61,0,0,0-.1.57v.05a0,0,0,0,1,0,0C2,14.91,2,15,2,15v4a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V15C22,15,22,14.91,22,14.86ZM5.71,4.83a1,1,0,0,1,1-.83H17.31a1,1,0,0,1,1,.83l1.2,7.22A2.63,2.63,0,0,0,19,12H5a2.63,2.63,0,0,0-.49.05ZM20,19a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V15.08l.08-.46A1,1,0,0,1,5,14H19a1,1,0,0,1,.92.62l.08.46Zm-3-3a1,1,0,1,0,1,1A1,1,0,0,0,17,16Z"/>
        </svg>
    </span>
    """
    render_metric_card(
        "Menor Memória",
        short_algorithm_name(str(lowest_memory["algorithm"])),
        f"{float(lowest_memory['avg_peak_memory_kb']):.2f} KB No Maior Grafo",
        memory_icon,
    )

tab_overview, tab_table = st.tabs(["Gráficos", "Tabela"])

with tab_overview:
    with st.container(key="main_charts_panel"):
        render_chart_title("Resultados Principais", "comparison", featured=True)
        col_time, col_memory = st.columns(2)

        with col_time:
            render_chart_title("Tempo Médio De Execução", "time")
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
            fig_time.update_traces(
                line_shape="spline",
                line_width=4,
                marker_size=10,
                marker_line_color="#FFFFFF",
                marker_line_width=2,
                hovertemplate="Vértices: %{x}<br>Tempo médio: %{y:.6f} s<extra>%{fullData.name}</extra>",
            )
            style_plotly_chart(fig_time, height=420)
            st.plotly_chart(fig_time, width="stretch", config={"displayModeBar": False})

        with col_memory:
            render_chart_title("Uso Aproximado De Memória", "memory")
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
            fig_memory.update_traces(
                line_shape="spline",
                line_width=4,
                marker_size=10,
                marker_line_color="#FFFFFF",
                marker_line_width=2,
                hovertemplate="Vértices: %{x}<br>Memória média: %{y:.2f} KB<extra>%{fullData.name}</extra>",
            )
            style_plotly_chart(fig_memory, height=420)
            st.plotly_chart(fig_memory, width="stretch", config={"displayModeBar": False})

    with st.container(key="complementary_panel"):
        render_chart_title("Comparações Complementares", "comparison", featured=True)
        col_time_bar, col_ratio, col_edges = st.columns(3)

        with col_time_bar:
            render_chart_title("Tempo Por Algoritmo", "algorithm")
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
            fig_time_bar.update_traces(
                marker_line_color="#FFFFFF",
                marker_line_width=1.2,
                opacity=0.94,
                hovertemplate="Vértices: %{x}<br>Tempo médio: %{y:.6f} s<extra>%{fullData.name}</extra>",
            )
            fig_time_bar.update_layout(bargap=0.28, bargroupgap=0.08)
            style_plotly_chart(fig_time_bar, height=340)
            st.plotly_chart(fig_time_bar, width="stretch", config={"displayModeBar": False})

        with col_ratio:
            render_chart_title("Razão De Tempo", "ratio")
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
                marker_color="#D19600",
                marker_line_color="#FFFFFF",
                marker_line_width=1.2,
                opacity=0.94,
                hovertemplate="Vértices: %{x}<br>Razão: %{y:.2f}x<extra></extra>",
            )
            fig_ratio.update_layout(bargap=0.36)
            style_plotly_chart(fig_ratio, height=340)
            fig_ratio.update_layout(showlegend=False)
            st.plotly_chart(fig_ratio, width="stretch", config={"displayModeBar": False})

        with col_edges:
            render_chart_title("Distribuição De Arestas", "edges")
            edges_df = df.drop_duplicates("vertices").sort_values("vertices")
            fig_edges = px.pie(
                edges_df,
                names="vertices",
                values="edges",
                hole=0.48,
                color_discrete_sequence=["#111844", "#7288AE", "#D19600", "#7AE2CF", "#5E7FB8"],
            )
            fig_edges.update_traces(
                textinfo="label+percent",
                texttemplate="%{label} vértices<br>%{percent}",
                textfont_color="#111844",
                textfont_size=12,
                marker=dict(line=dict(color="#FFFFFF", width=2)),
                hovertemplate="Vértices: %{label}<br>Arestas: %{value}<br>Participação: %{percent}<extra></extra>",
            )
            style_plotly_chart(fig_edges, height=340)
            fig_edges.update_layout(
                showlegend=True,
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
                margin=dict(l=18, r=18, t=34, b=16),
            )
            st.plotly_chart(fig_edges, width="stretch", config={"displayModeBar": False})

        col_density_time, col_edges_time = st.columns(2)

        with col_density_time:
            render_chart_title(
                f"Tempo Por Densidade ({density_analysis_size} Vértices)",
                "density",
                tooltip=CHART_TOOLTIPS["Tempo Por Densidade"],
            )
            fig_density_time = px.line(
                density_df,
                x="density",
                y="avg_time_seconds",
                color="algorithm",
                markers=True,
                color_discrete_map=COLOR_MAP,
                labels={
                    "density": "Densidade",
                    "avg_time_seconds": "Tempo Médio (s)",
                    "algorithm": "Algoritmo",
                },
            )
            fig_density_time.update_traces(
                line_shape="spline",
                line_width=3.6,
                marker_size=9,
                marker_line_color="#FFFFFF",
                marker_line_width=1.8,
                hovertemplate="Densidade: %{x:.2f}<br>Tempo médio: %{y:.6f} s<extra>%{fullData.name}</extra>",
            )
            style_plotly_chart(fig_density_time, height=360)
            st.plotly_chart(fig_density_time, width="stretch", config={"displayModeBar": False})

        with col_edges_time:
            render_chart_title("Tempo Por Arestas", "edges")
            edges_time_df = df.sort_values(["algorithm", "edges"])
            fig_edges_time = px.line(
                edges_time_df,
                x="edges",
                y="avg_time_seconds",
                color="algorithm",
                markers=True,
                color_discrete_map=COLOR_MAP,
                labels={
                    "edges": "Arestas",
                    "avg_time_seconds": "Tempo Médio (s)",
                    "algorithm": "Algoritmo",
                },
            )
            fig_edges_time.update_traces(
                line_shape="spline",
                line_width=3.6,
                marker_size=9,
                marker_line_color="#FFFFFF",
                marker_line_width=1.8,
                hovertemplate="Arestas: %{x}<br>Tempo médio: %{y:.6f} s<extra>%{fullData.name}</extra>",
            )
            style_plotly_chart(fig_edges_time, height=360)
            st.plotly_chart(fig_edges_time, width="stretch", config={"displayModeBar": False})

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
