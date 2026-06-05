"""Interface de linha de comando para executar a comparação."""

from __future__ import annotations

import argparse
from pathlib import Path

from caminho_minimo.benchmark import run_benchmarks, summarize_results
from caminho_minimo.visualization import save_results


def _parse_sizes(value: str) -> list[int]:
    sizes = [int(item.strip()) for item in value.split(",") if item.strip()]
    if not sizes:
        raise argparse.ArgumentTypeError("Informe pelo menos um tamanho.")
    if any(size < 2 for size in sizes):
        raise argparse.ArgumentTypeError("Todos os tamanhos devem ser maiores ou iguais a 2.")
    return sizes


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Compara Dijkstra e Floyd-Warshall em grafos ponderados positivos."
    )
    parser.add_argument(
        "--sizes",
        type=_parse_sizes,
        default=[10, 25, 50],
        help="Tamanhos dos grafos separados por vírgula. Ex.: 10,25,50",
    )
    parser.add_argument("--density", type=float, default=0.35, help="Densidade do grafo no intervalo (0, 1].")
    parser.add_argument("--repetitions", type=int, default=3, help="Número de repetições por tamanho.")
    parser.add_argument("--seed", type=int, default=42, help="Semente para reprodutibilidade.")
    parser.add_argument("--output-dir", type=Path, default=Path("results"), help="Pasta para CSV e gráficos.")
    return parser


def main() -> None:
    args = build_parser().parse_args()

    if not 0 < args.density <= 1:
        raise SystemExit("Erro: --density deve estar no intervalo (0, 1].")
    if args.repetitions < 1:
        raise SystemExit("Erro: --repetitions deve ser pelo menos 1.")

    print("Comparação de caminhos mínimos")
    print(f"Tamanhos: {args.sizes} | densidade: {args.density:.2f} | repetições: {args.repetitions}")
    print("Comparação justa: Dijkstra é executado para todas as origens.\n")

    results = run_benchmarks(
        sizes=args.sizes,
        density=args.density,
        repetitions=args.repetitions,
        seed=args.seed,
    )
    summary = summarize_results(results)
    csv_path, time_plot_path, memory_plot_path = save_results(summary, args.output_dir)

    print(f"{'Algoritmo':<28} {'V':>5} {'A':>6} {'Tempo médio (s)':>17} {'Memória (KB)':>14}")
    print("-" * 74)
    for item in summary:
        print(
            f"{item['algorithm']:<28} "
            f"{item['vertices']:>5} "
            f"{item['edges']:>6} "
            f"{item['avg_time_seconds']:>17.6f} "
            f"{item['avg_peak_memory_kb']:>14.2f}"
        )

    print("\nArquivos gerados:")
    print(f"- {csv_path}")
    print(f"- {time_plot_path}")
    print(f"- {memory_plot_path}")


if __name__ == "__main__":
    main()
