"""Interface Streamlit para demonstrar a comparação dos algoritmos."""

from __future__ import annotations

import math
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
        right: 1.15rem;
        top: 1.72rem;
        z-index: 30;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] button {
        align-items: center;
        background: rgba(255, 255, 255, 0.14) !important;
        border-radius: 8px !important;
        box-shadow: none;
        display: inline-flex;
        height: 2rem;
        justify-content: center;
        width: 2rem;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] button:hover {
        background: rgba(122, 226, 207, 0.18) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"] {
        color: transparent !important;
        font-size: 0 !important;
        position: relative;
    }

    section[data-testid="stSidebar"] div[data-testid="stSidebarCollapseButton"] span[data-testid="stIconMaterial"]::before {
        color: #FFFBEB;
        content: "close";
        font-family: "Material Symbols Rounded", "Material Icons";
        font-size: 1.2rem;
        font-variation-settings: "FILL" 0, "wght" 600, "GRAD" 0, "opsz" 24;
        line-height: 1;
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
        padding: 16px 52px 14px 16px;
        position: relative;
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
        overflow: visible;
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


def _estimate_pair_execution_seconds(vertices: int, density: float) -> float:
    """Estima o tempo de uma comparação no mesmo grafo.

    A estimativa é deliberadamente conservadora: combina o crescimento esperado
    de Dijkstra para todas as origens com Floyd-Warshall e inclui uma pequena
    margem para geração do grafo e medição de memória.
    """

    max_edges = vertices * (vertices - 1)
    edges = max(vertices, round(max_edges * density))
    dijkstra_cost = vertices * (vertices + edges) * math.log2(max(vertices, 2))
    floyd_cost = vertices**3

    return 0.015 + dijkstra_cost * 2.8e-8 + floyd_cost * 5.5e-9


def estimate_dashboard_execution_time(sizes: list[int], density: float, repetitions: int) -> float:
    """Estima o tempo total do botão Executar Comparação no dashboard."""

    main_seconds = sum(
        _estimate_pair_execution_seconds(vertices, density) * repetitions
        for vertices in sizes
    )

    density_vertices = min(max(sizes), DENSITY_SWEEP_MAX_VERTICES)
    density_repetitions = max(1, min(repetitions, 3))
    density_seconds = sum(
        _estimate_pair_execution_seconds(density_vertices, density_value) * density_repetitions
        for density_value in build_density_points(density)
    )

    return main_seconds + density_seconds


def format_estimated_time(seconds: float) -> str:
    """Formata a estimativa para caber no resumo lateral."""

    if seconds < 1:
        return "< 1 s"
    if seconds < 60:
        return f"~{seconds:.0f} s"

    minutes = seconds / 60
    if minutes < 10:
        return f"~{minutes:.1f} min"
    return f"~{minutes:.0f} min"


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
        <svg viewBox="0 0 92 92" aria-hidden="true">
            <path fill="currentColor" d="M81.3 19.6c.8.7 1.7 1 2.7 1 1.1 0 2.2-.4 3-1.3 1.5-1.6 1.4-4.2-.3-5.7l-5.2-4.7-5.2-4.7c-1.6-1.5-4.2-1.4-5.6.3-1.5 1.6-1.4 4.2.3 5.7l2.2 2-4 4.5c-4.6-3.4-9.9-5.9-15.7-7.2-.1-1.3-.6-2.7-1.6-4-1-1.4-3.1-3-6.9-3.2h-.2c-3.5 0-5.5 1.5-6.6 2.8-1.2 1.4-1.7 3.1-1.9 4.4C17.8 13.4 4 29.8 4 49.4c0 22.5 18.3 40.9 40.8 40.9 22.5 0 40.8-18.3 40.8-40.9 0-10.5-4-20.1-10.5-27.4l4-4.5 2.2 2.1zM44.8 82.2C26.7 82.2 12 67.5 12 49.4s14.7-32.8 32.8-32.8c18.1 0 32.8 14.7 32.8 32.8S62.9 82.2 44.8 82.2zm7-32.8c0 3.8-3.2 6.9-7 6.9S38 53.2 38 49.4c0-2.3 1-4.4 3-5.6V27.6c0-2.2 1.8-4 4-4s4 1.8 4 4v16.2c2 1.2 2.8 3.3 2.8 5.6z"/>
        </svg>
    """,
    "memory": """
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path fill="currentColor" d="M22,14.86a0,0,0,0,1,0,0v-.05a2.61,2.61,0,0,0-.1-.57L20.26,4.51a3,3,0,0,0-3-2.51H6.69A3,3,0,0,0,3.74,4.51L2.12,14.22a2.61,2.61,0,0,0-.1.57v.05a0,0,0,0,1,0,0C2,14.91,2,15,2,15v4a3,3,0,0,0,3,3H19a3,3,0,0,0,3-3V15C22,15,22,14.91,22,14.86ZM5.71,4.83a1,1,0,0,1,1-.83H17.31a1,1,0,0,1,1,.83l1.2,7.22A2.63,2.63,0,0,0,19,12H5a2.63,2.63,0,0,0-.49.05ZM20,19a1,1,0,0,1-1,1H5a1,1,0,0,1-1-1V15.08l.08-.46A1,1,0,0,1,5,14H19a1,1,0,0,1,.92.62l.08.46Zm-3-3a1,1,0,1,0,1,1A1,1,0,0,0,17,16Z"/>
        </svg>
    """,
    "comparison": """
        <svg viewBox="0 0 52 52" aria-hidden="true">
            <path fill="currentColor" d="M49.30195 49.30861c-2.40997 2.38995-6.26001 2.19995-8.41998-.26001l-8.26001-9.33002c3.0858-1.92774 5.6316-4.6288 7.08002-7.08997l9.33997 8.25995C51.75196 43.32856 51.45198 47.13856 49.30195 49.30861zM26.40199 19.21858V34.1186c3.0603-1.20237 5.71787-3.8247 6.79999-5.88v-9.02002H26.40199zM17.60194 10.09858v24.69c2.30296.5653 4.67377.53127 6.80005-.01001V10.09858H17.60194zM8.80195 24.37861v3.83997c1.48417 2.54061 3.86393 4.70809 6.79999 5.91003v-9.75H8.80195z"/>
            <path fill="currentColor" d="M6.85353,35.16493c-7.79688-7.79785-7.79785-20.49463,0-28.30273c7.81983-7.81781,20.47685-7.81767,28.30566-0.00098c7.65651,7.66882,7.92533,20.38294,0,28.3042C27.47855,42.84227,14.80152,43.12423,6.85353,35.16493z M9.56594,9.57356c-6.30362,6.31239-6.30362,16.5765,0,22.88055c6.36253,6.37259,16.60726,6.27374,22.88143-0.00044c6.43725-6.43725,6.16037-16.71031-0.00087-22.88055C26.12367,3.25755,15.8881,3.25231,9.56594,9.57356z"/>
        </svg>
    """,
    "complementary": """
        <svg viewBox="0 0 111 111" fill="none" aria-hidden="true">
            <path fill="currentColor" fill-rule="evenodd" clip-rule="evenodd" d="M61.6667 0V49.3333H111C111 36.2493 105.802 23.7012 96.5506 14.4494C87.2988 5.1976 74.7507 0 61.6667 0ZM49.3334 61.6667H98.6667C98.6667 71.4239 95.7733 80.962 90.3525 89.0748C84.9317 97.1876 77.2269 103.511 68.2124 107.245C59.1979 110.979 49.2786 111.956 39.7089 110.052C30.1392 108.149 21.3488 103.45 14.4494 96.5506C7.55003 89.6512 2.85149 80.8608 0.947948 71.2911C-0.955589 61.7214 0.0213752 51.8021 3.7553 42.7876C7.48922 33.7731 13.8124 26.0683 21.9252 20.6475C30.038 15.2267 39.5761 12.3333 49.3334 12.3333V61.6667Z"/>
        </svg>
    """,
    "algorithm": """
        <svg viewBox="0 0 96 96" fill="none" aria-hidden="true">
            <path stroke="currentColor" stroke-width="5" d="M46.1485 48.741C47.189 47.7626 48.811 47.7626 49.8515 48.741L58.1532 56.5473C64.9885 62.9746 69.3307 71.612 70.412 80.932C70.7252 83.6312 68.6153 86 65.898 86H30.102C27.3847 86 25.2748 83.6312 25.588 80.932C26.6693 71.612 31.0115 62.9746 37.8468 56.5473L46.1485 48.741zM49.7831 46.3664C48.7741 47.2908 47.2259 47.2908 46.217 46.3664L37.7371 38.597C30.9791 32.4053 26.6664 23.9946 25.5827 14.8932C25.2727 12.2898 27.306 10 29.9278 10L66.0722 10C68.694 10 70.7273 12.2898 70.4173 14.8932C69.3336 23.9946 65.0209 32.4052 58.2629 38.597L49.7831 46.3664z"/>
            <path fill="currentColor" d="M63.9735 81H34.524 31.8639C31.3942 81 31.0203 80.6064 31.0446 80.1373 31.4348 72.58 34.8349 65.4937 40.4857 60.4606L46.8399 54.8009C47.3564 54.3409 48.132 54.3292 48.6621 54.7734L53.6891 58.9856C59.9975 64.2715 64.0123 71.7961 64.8905 79.9793 64.949 80.5245 64.5218 81 63.9735 81zM34.7653 24L60.5962 24 61.5089 24C62.1926 24 62.6363 24.7208 62.3283 25.3312 60.5912 28.7738 58.2399 31.87 55.3902 34.4677L49.5301 39.8093C48.7841 40.4894 47.6482 40.5068 46.8816 39.8501L42.0951 35.7496C38.7464 32.8808 35.95 29.4245 33.8434 25.5508 33.4631 24.8515 33.9693 24 34.7653 24z"/>
        </svg>
    """,
    "ratio": """
        <svg viewBox="0 0 138 138" fill="none" aria-hidden="true">
            <path fill="currentColor" d="M135.11 56.3869C134.1 62.6309 128.166 66.9138 121.922 65.9046C120.9 65.7395 119.954 65.47 119.091 65.0394L95.6264 81.9241C95.7634 82.8782 95.7118 83.9183 95.5467 84.94C94.5374 91.184 88.603 95.467 82.359 94.4577C76.1151 93.4485 71.8321 87.5141 72.8413 81.2701C73.0065 80.2484 73.2851 79.245 73.7158 78.3826L61.5807 61.5684C60.6266 61.7055 59.5865 61.6538 58.5648 61.4887C57.543 61.3235 56.5396 61.0449 55.6773 60.6143L25.6663 82.3238C25.8033 83.2779 25.7609 84.2612 25.5957 85.283C24.5865 91.5269 18.6521 95.8099 12.4081 94.8007C6.16415 93.7914 1.88118 87.857 2.89041 81.613C3.89963 75.3691 9.83406 71.0861 16.078 72.0953C17.0998 72.2605 18.0464 72.53 18.9087 72.9606L48.9673 51.317C48.8303 50.3629 48.8819 49.3228 49.0471 48.3011C50.0563 42.0571 55.9907 37.7741 62.2347 38.7834C68.4786 39.7926 72.7616 45.727 71.7524 51.971C71.5872 52.9927 71.3086 53.9961 70.878 54.8585L83.013 71.6727C83.9671 71.5356 85.0072 71.5873 86.029 71.7524C87.0507 71.9176 88.0541 72.1962 88.9164 72.6268L112.334 55.6761C112.197 54.7221 112.239 53.7387 112.404 52.717C113.413 46.473 119.348 42.1901 125.592 43.1993C131.836 44.2085 136.119 50.1429 135.11 56.3869Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.1" d="M93.5 10.9502C98.9484 10.9561 104.172 13.123 108.024 16.9756C111.877 20.8282 114.044 26.0516 114.05 31.5C114.05 35.5644 112.845 39.5376 110.587 42.917C108.329 46.2964 105.119 48.93 101.364 50.4854C97.6093 52.0407 93.4774 52.4481 89.4912 51.6553C85.5049 50.8623 81.8427 48.9052 78.9688 46.0312C76.0948 43.1573 74.1377 39.4951 73.3447 35.5088C72.5519 31.5226 72.9593 27.3907 74.5146 23.6357C76.07 19.8808 78.7036 16.6711 82.083 14.4131C85.4624 12.1551 89.4356 10.9502 93.5 10.9502ZM100.019 15.7637C96.9061 14.4745 93.4809 14.1367 90.1768 14.7939C86.8727 15.4512 83.8382 17.0739 81.4561 19.4561C79.0739 21.8382 77.4512 24.8727 76.7939 28.1768C76.1367 31.4809 76.4745 34.9061 77.7637 38.0186C79.0529 41.1309 81.2361 43.7915 84.0371 45.6631C86.8381 47.5346 90.1313 48.5332 93.5 48.5332L93.9229 48.5273C98.2855 48.4144 102.446 46.6325 105.539 43.5391C108.732 40.3458 110.528 36.016 110.533 31.5C110.533 28.1313 109.535 24.8381 107.663 22.0371C105.791 19.2361 103.131 17.0529 100.019 15.7637Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.2" d="M90.9027 21.1504C91.3823 21.1504 91.8429 21.3406 92.182 21.6797C92.521 22.0187 92.7112 22.4786 92.7113 22.958V32.1836L100.374 36.7822C100.582 36.9022 100.765 37.0627 100.911 37.2539C101.056 37.445 101.162 37.664 101.222 37.8965C101.282 38.1288 101.295 38.3709 101.261 38.6084C101.227 38.8461 101.145 39.0744 101.021 39.2803C100.897 39.4861 100.734 39.6656 100.54 39.8076C100.347 39.9496 100.126 40.0514 99.8929 40.1074C99.6593 40.1634 99.4162 40.1725 99.1791 40.1338C98.9425 40.0951 98.7164 40.0089 98.5131 39.8818V39.8828L89.972 34.7578L89.9681 34.7559C89.7102 34.5868 89.496 34.3583 89.3441 34.0898C89.1923 33.8214 89.1072 33.5201 89.0951 33.2119V22.958C89.0952 22.4785 89.2853 22.0187 89.6244 21.6797C89.9634 21.3406 90.4232 21.1505 90.9027 21.1504Z"/>
        </svg>
    """,
    "edges": """
        <svg viewBox="0 0 113 113" fill="none" aria-hidden="true">
            <path d="M45 88.5C45 100.098 35.598 109.5 24 109.5C12.402 109.5 3 100.098 3 88.5C3 76.902 12.402 67.5 24 67.5M45 88.5C45 76.902 35.598 67.5 24 67.5M45 88.5H67.638M24 67.5L24.0001 56.25L24.0002 45M76.5002 71.361C71.1375 75.1657 67.638 81.4242 67.638 88.5C67.638 100.098 77.04 109.5 88.638 109.5C100.236 109.5 109.638 100.098 109.638 88.5C109.638 76.902 100.236 67.5 88.638 67.5C84.1159 67.5 79.9275 68.9294 76.5002 71.361ZM41.1963 36.057C37.3972 41.4653 31.1115 45 24.0002 45C12.4023 45 3.00024 35.598 3.00024 24C3.00024 12.402 12.4023 3 24.0002 3C35.5982 3 45.0002 12.402 45.0002 24C45.0002 28.4867 43.5932 32.6448 41.1963 36.057ZM76.5002 71.361C62.7132 57.5739 54.9833 49.8441 41.1963 36.057M78.5002 73L38.9844 34.5127M44.0002 88.5H69.0002M24.0002 69.5V43.5" stroke="currentColor" stroke-width="6"/>
        </svg>
    """,
    "trend": """
        <svg viewBox="0 0 133 113" fill="none" aria-hidden="true">
            <path fill="currentColor" d="M132.366 73.4869C131.357 79.7308 125.423 84.0138 119.179 83.0046C118.157 82.8394 117.21 82.5699 116.348 82.1393L92.8834 99.0241C93.0204 99.9782 92.9688 101.018 92.8036 102.04C91.7944 108.284 85.86 112.567 79.616 111.558C73.372 110.548 69.0891 104.614 70.0983 98.3701C70.2634 97.3483 70.5421 96.345 70.9727 95.4826L58.8376 78.6684C57.8836 78.8054 56.8435 78.7538 55.8217 78.5887C54.8 78.4235 53.7966 78.1448 52.9343 77.7142L22.9233 99.4238C23.0603 100.378 23.0178 101.361 22.8527 102.383C21.8435 108.627 15.909 112.91 9.66507 111.901C3.42111 110.891 -0.861862 104.957 0.147364 98.713C1.15659 92.4691 7.09102 88.1861 13.335 89.1953C14.3567 89.3605 15.3033 89.63 16.1657 90.0606L46.2243 68.417C46.0873 67.4629 46.1389 66.4228 46.304 65.401C47.3133 59.1571 53.2477 54.8741 59.4916 55.8833C65.7356 56.8926 70.0186 62.827 69.0093 69.071C68.8442 70.0927 68.5655 71.0961 68.1349 71.9584L80.27 88.7726C81.2241 88.6356 82.2642 88.6872 83.2859 88.8524C84.3076 89.0175 85.311 89.2962 86.1734 89.7268L109.591 72.7761C109.454 71.822 109.496 70.8387 109.661 69.817C110.67 63.573 116.605 59.29 122.849 60.2993C129.093 61.3085 133.376 67.2429 132.366 73.4869Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.1" d="M93.257 0.0501709C101.489 0.0590747 109.382 3.33262 115.203 9.15369C121.024 14.9748 124.298 22.8678 124.307 31.1C124.307 37.2409 122.486 43.2439 119.074 48.35C115.663 53.456 110.813 57.4364 105.14 59.7865C99.4661 62.1366 93.2224 62.7512 87.1993 61.5531C81.1763 60.355 75.6433 57.3984 71.3009 53.056C66.9585 48.7136 64.0019 43.1807 62.8038 37.1576C61.6058 31.1346 62.2205 24.8917 64.5704 19.2181C66.9205 13.5445 70.9008 8.69441 76.007 5.28259C81.113 1.87096 87.116 0.0501725 93.257 0.0501709ZM103.124 7.27966C98.4129 5.32818 93.2282 4.81703 88.2267 5.81189C83.2253 6.80677 78.6313 9.26271 75.0255 12.8685C71.4197 16.4744 68.9637 21.0683 67.9689 26.0697C66.974 31.0712 67.4852 36.2559 69.4366 40.9672C71.3881 45.6783 74.6928 49.7054 78.9327 52.5385C83.1727 55.3714 88.1576 56.8832 93.257 56.8832L93.8966 56.8744C100.501 56.7036 106.798 54.0063 111.481 49.3236C116.314 44.4899 119.033 37.9358 119.04 31.1C119.04 26.0007 117.528 21.0157 114.695 16.7758C111.862 12.5358 107.835 9.23116 103.124 7.27966Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.2" d="M88.965 16.0004C89.7077 16.0004 90.4213 16.2771 90.9484 16.7719C91.4756 17.2669 91.7735 17.9399 91.7736 18.6429V32.4047L103.948 39.265C104.271 39.4399 104.555 39.6742 104.781 39.9535C105.008 40.2328 105.173 40.5523 105.267 40.8929C105.361 41.2335 105.382 41.5886 105.328 41.9369C105.274 42.2851 105.147 42.6193 104.954 42.9203C104.762 43.2214 104.507 43.4837 104.206 43.6908C103.905 43.8977 103.564 44.0458 103.202 44.1273C102.84 44.2088 102.464 44.2218 102.097 44.1654C101.73 44.1091 101.378 43.9846 101.063 43.7992L87.5216 36.1703L87.5177 36.1683C87.1165 35.9215 86.784 35.5869 86.547 35.1937C86.3101 34.8006 86.1763 34.3598 86.1573 33.9076V18.6429C86.1574 17.9399 86.4544 17.2669 86.9816 16.7719C87.5086 16.277 88.2222 16.0004 88.965 16.0004Z"/>
        </svg>
    """,
    "edges_time": """
        <svg viewBox="0 0 138 138" fill="none" aria-hidden="true">
            <path fill="currentColor" d="M135.11 56.3869C134.1 62.6309 128.166 66.9138 121.922 65.9046C120.9 65.7395 119.954 65.47 119.091 65.0394L95.6264 81.9241C95.7634 82.8782 95.7118 83.9183 95.5467 84.94C94.5374 91.184 88.603 95.467 82.359 94.4577C76.1151 93.4485 71.8321 87.5141 72.8413 81.2701C73.0065 80.2484 73.2851 79.245 73.7158 78.3826L61.5807 61.5684C60.6266 61.7055 59.5865 61.6538 58.5648 61.4887C57.543 61.3235 56.5396 61.0449 55.6773 60.6143L25.6663 82.3238C25.8033 83.2779 25.7609 84.2612 25.5957 85.283C24.5865 91.5269 18.6521 95.8099 12.4081 94.8007C6.16415 93.7914 1.88118 87.857 2.89041 81.613C3.89963 75.3691 9.83406 71.0861 16.078 72.0953C17.0998 72.2605 18.0464 72.53 18.9087 72.9606L48.9673 51.317C48.8303 50.3629 48.8819 49.3228 49.0471 48.3011C50.0563 42.0571 55.9907 37.7741 62.2347 38.7834C68.4786 39.7926 72.7616 45.727 71.7524 51.971C71.5872 52.9927 71.3086 53.9961 70.878 54.8585L83.013 71.6727C83.9671 71.5356 85.0072 71.5873 86.029 71.7524C87.0507 71.9176 88.0541 72.1962 88.9164 72.6268L112.334 55.6761C112.197 54.7221 112.239 53.7387 112.404 52.717C113.413 46.473 119.348 42.1901 125.592 43.1993C131.836 44.2085 136.119 50.1429 135.11 56.3869Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.1" d="M93.5 10.9502C98.9484 10.9561 104.172 13.123 108.024 16.9756C111.877 20.8282 114.044 26.0516 114.05 31.5C114.05 35.5644 112.845 39.5376 110.587 42.917C108.329 46.2964 105.119 48.93 101.364 50.4854C97.6093 52.0407 93.4774 52.4481 89.4912 51.6553C85.5049 50.8623 81.8427 48.9052 78.9688 46.0312C76.0948 43.1573 74.1377 39.4951 73.3447 35.5088C72.5519 31.5226 72.9593 27.3907 74.5146 23.6357C76.07 19.8808 78.7036 16.6711 82.083 14.4131C85.4624 12.1551 89.4356 10.9502 93.5 10.9502ZM100.019 15.7637C96.9061 14.4745 93.4809 14.1367 90.1768 14.7939C86.8727 15.4512 83.8382 17.0739 81.4561 19.4561C79.0739 21.8382 77.4512 24.8727 76.7939 28.1768C76.1367 31.4809 76.4745 34.9061 77.7637 38.0186C79.0529 41.1309 81.2361 43.7915 84.0371 45.6631C86.8381 47.5346 90.1313 48.5332 93.5 48.5332L93.9229 48.5273C98.2855 48.4144 102.446 46.6325 105.539 43.5391C108.732 40.3458 110.528 36.016 110.533 31.5C110.533 28.1313 109.535 24.8381 107.663 22.0371C105.791 19.2361 103.131 17.0529 100.019 15.7637Z"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="0.2" d="M90.9027 21.1504C91.3823 21.1504 91.8429 21.3406 92.182 21.6797C92.521 22.0187 92.7112 22.4786 92.7113 22.958V32.1836L100.374 36.7822C100.582 36.9022 100.765 37.0627 100.911 37.2539C101.056 37.445 101.162 37.664 101.222 37.8965C101.282 38.1288 101.295 38.3709 101.261 38.6084C101.227 38.8461 101.145 39.0744 101.021 39.2803C100.897 39.4861 100.734 39.6656 100.54 39.8076C100.347 39.9496 100.126 40.0514 99.8929 40.1074C99.6593 40.1634 99.4162 40.1725 99.1791 40.1338C98.9425 40.0951 98.7164 40.0089 98.5131 39.8818V39.8828L89.972 34.7578L89.9681 34.7559C89.7102 34.5868 89.496 34.3583 89.3441 34.0898C89.1923 33.8214 89.1072 33.5201 89.0951 33.2119V22.958C89.0952 22.4785 89.2853 22.0187 89.6244 21.6797C89.9634 21.3406 90.4232 21.1505 90.9027 21.1504Z"/>
        </svg>
    """,
    "density": """
        <svg viewBox="0 0 123 115" fill="none" aria-hidden="true">
            <path d="M81.5 61.5C94.7548 61.5 105.5 50.7548 105.5 37.5C105.5 24.2452 94.7548 13.5 81.5 13.5C68.2452 13.5 57.5 24.2452 57.5 37.5C57.5 50.7548 68.2452 61.5 81.5 61.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M38 83.5C46.0081 83.5 52.5 77.0081 52.5 69C52.5 60.9919 46.0081 54.5 38 54.5C29.9919 54.5 23.5 60.9919 23.5 69C23.5 77.0081 29.9919 83.5 38 83.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M72 92.5C77.2467 92.5 81.5 88.2467 81.5 83C81.5 77.7533 77.2467 73.5 72 73.5C66.7533 73.5 62.5 77.7533 62.5 83C62.5 88.2467 66.7533 92.5 72 92.5Z" stroke="currentColor" stroke-width="7"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="3" fill-rule="evenodd" clip-rule="evenodd" d="M4.65789 1.5C6.40194 1.5 7.81579 2.8196 7.81579 4.44737V86.9737C7.81579 98.3682 17.7126 107.605 29.9211 107.605H118.342C120.086 107.605 121.5 108.925 121.5 110.553C121.5 112.18 120.086 113.5 118.342 113.5H29.9211C14.2246 113.5 2.84328 101.877 1.5 86.9737V4.44737C1.5 2.8196 2.91385 1.5 4.65789 1.5Z"/>
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
        sidebar_estimated_time = format_estimated_time(
            estimate_dashboard_execution_time(sidebar_sizes, density, repetitions)
        )
    except ValueError:
        sidebar_largest = "-"
        sidebar_total_executions = "-"
        sidebar_edges = "-"
        sidebar_sizes_text = "Inválido"
        sidebar_estimated_time = "-"

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
            <div class="sidebar-summary-row">
                <span class="sidebar-summary-label">Tempo Estimado</span>
                <span class="sidebar-summary-value">{sidebar_estimated_time}</span>
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
        <svg viewBox="0 0 137 137" fill="none">
            <path d="M86.5 68.5C86.5 78.4411 78.4411 86.5 68.5 86.5C58.5589 86.5 50.5 78.4411 50.5 68.5C50.5 58.5589 58.5589 50.5 68.5 50.5C78.4411 50.5 86.5 58.5589 86.5 68.5Z" fill="currentColor"/>
            <path d="M78.5 12C78.5 17.799 74.0228 22.5 68.5 22.5C62.9772 22.5 58.5 17.799 58.5 12C58.5 6.20101 62.9772 1.5 68.5 1.5C74.0228 1.5 78.5 6.20101 78.5 12Z" fill="currentColor"/>
            <path d="M119.5 28C119.5 33.799 114.799 38.5 109 38.5C103.201 38.5 98.5 33.799 98.5 28C98.5 22.201 103.201 17.5 109 17.5C114.799 17.5 119.5 22.201 119.5 28Z" fill="currentColor"/>
            <path d="M135.5 68.5C135.5 74.0228 130.799 78.5 125 78.5C119.201 78.5 114.5 74.0228 114.5 68.5C114.5 62.9772 119.201 58.5 125 58.5C130.799 58.5 135.5 62.9772 135.5 68.5Z" fill="currentColor"/>
            <path d="M119.5 109C119.5 114.799 114.799 119.5 109 119.5C103.201 119.5 98.5 114.799 98.5 109C98.5 103.201 103.201 98.5 109 98.5C114.799 98.5 119.5 103.201 119.5 109Z" fill="currentColor"/>
            <path d="M78.5 125C78.5 130.799 74.0228 135.5 68.5 135.5C62.9772 135.5 58.5 130.799 58.5 125C58.5 119.201 62.9772 114.5 68.5 114.5C74.0228 114.5 78.5 119.201 78.5 125Z" fill="currentColor"/>
            <path d="M38.5 109C38.5 114.799 33.799 119.5 28 119.5C22.201 119.5 17.5 114.799 17.5 109C17.5 103.201 22.201 98.5 28 98.5C33.799 98.5 38.5 103.201 38.5 109Z" fill="currentColor"/>
            <path d="M22.5 68.5C22.5 74.0228 17.799 78.5 12 78.5C6.20101 78.5 1.5 74.0228 1.5 68.5C1.5 62.9772 6.20101 58.5 12 58.5C17.799 58.5 22.5 62.9772 22.5 68.5Z" fill="currentColor"/>
            <path d="M38.5 28C38.5 33.799 33.799 38.5 28 38.5C22.201 38.5 17.5 33.799 17.5 28C17.5 22.201 22.201 17.5 28 17.5C33.799 17.5 38.5 22.201 38.5 28Z" fill="currentColor"/>
            <path d="M39.6206 39.0431L52.3274 52.1874M84.6724 51.3911L97.8167 38.6843M38.4656 97.598L51.6099 84.8912M84.8914 84.6724L97.5981 97.8167M68.5 45.5V26.5M68.5 110.5V91.5M91.5 68.5H110.5M25.5 68.5H44.5M86.5 68.5C86.5 78.4411 78.4411 86.5 68.5 86.5C58.5589 86.5 50.5 78.4411 50.5 68.5C50.5 58.5589 58.5589 50.5 68.5 50.5C78.4411 50.5 86.5 58.5589 86.5 68.5ZM78.5 12C78.5 17.799 74.0228 22.5 68.5 22.5C62.9772 22.5 58.5 17.799 58.5 12C58.5 6.20101 62.9772 1.5 68.5 1.5C74.0228 1.5 78.5 6.20101 78.5 12ZM119.5 28C119.5 33.799 114.799 38.5 109 38.5C103.201 38.5 98.5 33.799 98.5 28C98.5 22.201 103.201 17.5 109 17.5C114.799 17.5 119.5 22.201 119.5 28ZM135.5 68.5C135.5 74.0228 130.799 78.5 125 78.5C119.201 78.5 114.5 74.0228 114.5 68.5C114.5 62.9772 119.201 58.5 125 58.5C130.799 58.5 135.5 62.9772 135.5 68.5ZM119.5 109C119.5 114.799 114.799 119.5 109 119.5C103.201 119.5 98.5 114.799 98.5 109C98.5 103.201 103.201 98.5 109 98.5C114.799 98.5 119.5 103.201 119.5 109ZM78.5 125C78.5 130.799 74.0228 135.5 68.5 135.5C62.9772 135.5 58.5 130.799 58.5 125C58.5 119.201 62.9772 114.5 68.5 114.5C74.0228 114.5 78.5 119.201 78.5 125ZM38.5 109C38.5 114.799 33.799 119.5 28 119.5C22.201 119.5 17.5 114.799 17.5 109C17.5 103.201 22.201 98.5 28 98.5C33.799 98.5 38.5 103.201 38.5 109ZM22.5 68.5C22.5 74.0228 17.799 78.5 12 78.5C6.20101 78.5 1.5 74.0228 1.5 68.5C1.5 62.9772 6.20101 58.5 12 58.5C17.799 58.5 22.5 62.9772 22.5 68.5ZM38.5 28C38.5 33.799 33.799 38.5 28 38.5C22.201 38.5 17.5 33.799 17.5 28C17.5 22.201 22.201 17.5 28 17.5C33.799 17.5 38.5 22.201 38.5 28Z" stroke="currentColor" stroke-width="3" stroke-linecap="round"/>
        </svg>
    </span>
    """
    render_metric_card("Maior Grafo", f"{largest_size} Vértices", f"{int(largest_df['edges'].max())} Arestas", graph_icon)
with metric_cols[1]:
    density_icon = """
    <span class="graph-icon" aria-hidden="true">
        <svg viewBox="0 0 123 115" fill="none">
            <path d="M81.5 61.5C94.7548 61.5 105.5 50.7548 105.5 37.5C105.5 24.2452 94.7548 13.5 81.5 13.5C68.2452 13.5 57.5 24.2452 57.5 37.5C57.5 50.7548 68.2452 61.5 81.5 61.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M38 83.5C46.0081 83.5 52.5 77.0081 52.5 69C52.5 60.9919 46.0081 54.5 38 54.5C29.9919 54.5 23.5 60.9919 23.5 69C23.5 77.0081 29.9919 83.5 38 83.5Z" stroke="currentColor" stroke-width="7"/>
            <path d="M72 92.5C77.2467 92.5 81.5 88.2467 81.5 83C81.5 77.7533 77.2467 73.5 72 73.5C66.7533 73.5 62.5 77.7533 62.5 83C62.5 88.2467 66.7533 92.5 72 92.5Z" stroke="currentColor" stroke-width="7"/>
            <path fill="currentColor" stroke="currentColor" stroke-width="3" fill-rule="evenodd" clip-rule="evenodd" d="M4.65789 1.5C6.40194 1.5 7.81579 2.8196 7.81579 4.44737V86.9737C7.81579 98.3682 17.7126 107.605 29.9211 107.605H118.342C120.086 107.605 121.5 108.925 121.5 110.553C121.5 112.18 120.086 113.5 118.342 113.5H29.9211C14.2246 113.5 2.84328 101.877 1.5 86.9737V4.44737C1.5 2.8196 2.91385 1.5 4.65789 1.5Z"/>
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
        render_chart_title("Comparações Complementares", "complementary", featured=True)
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
            render_chart_title("Razão De Tempo", "trend")
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
            render_chart_title("Tempo Por Arestas", "trend")
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
