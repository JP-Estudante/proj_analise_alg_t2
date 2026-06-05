"""Arquivo único para executar o projeto.

Uso principal:
    python executar.py

Atalhos:
    python executar.py --terminal
    python executar.py --streamlit
"""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
APP_FILE = PROJECT_ROOT / "app.py"


def build_environment() -> dict[str, str]:
    """Garante que os módulos em src sejam encontrados sem instalação editável."""

    env = os.environ.copy()
    current_pythonpath = env.get("PYTHONPATH", "")
    paths = [str(SRC_DIR)]
    if current_pythonpath:
        paths.append(current_pythonpath)
    env["PYTHONPATH"] = os.pathsep.join(paths)
    return env


def run_terminal_results() -> int:
    """Executa a comparação no terminal usando os parâmetros padrão do projeto."""

    print("\n=== Resultados no terminal ===\n", flush=True)
    command = [sys.executable, "-m", "caminho_minimo.cli"]
    return subprocess.run(command, cwd=PROJECT_ROOT, env=build_environment(), check=False).returncode


def run_streamlit() -> int:
    """Abre a interface Streamlit."""

    print("\n=== Abrindo interface Streamlit ===\n", flush=True)
    command = [sys.executable, "-m", "streamlit", "run", str(APP_FILE)]
    completed = subprocess.run(command, cwd=PROJECT_ROOT, env=build_environment(), check=False)

    if completed.returncode != 0:
        print("\nNão foi possível iniciar o Streamlit.")
        print("Instale as dependências com: pip install -r requirements.txt")

    return completed.returncode


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Executa a comparação entre Dijkstra e Floyd-Warshall."
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--terminal",
        action="store_true",
        help="Roda somente a comparação no terminal.",
    )
    mode.add_argument(
        "--streamlit",
        action="store_true",
        help="Abre somente a interface Streamlit.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if args.terminal:
        raise SystemExit(run_terminal_results())

    if args.streamlit:
        raise SystemExit(run_streamlit())

    terminal_status = run_terminal_results()
    if terminal_status != 0:
        raise SystemExit(terminal_status)

    input("\nPressione Enter para abrir a interface Streamlit...")
    raise SystemExit(run_streamlit())


if __name__ == "__main__":
    main()
