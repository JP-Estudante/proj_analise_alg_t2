"""Rotinas de benchmark para tempo de execução e memória aproximada."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import statistics
import time
import tracemalloc
from typing import Callable

from caminho_minimo.algorithms import dijkstra_all_pairs, floyd_warshall
from caminho_minimo.graph import Graph, generate_connected_weighted_graph


@dataclass(frozen=True)
class BenchmarkResult:
    algorithm: str
    vertices: int
    edges: int
    density: float
    repetition: int
    time_seconds: float
    peak_memory_kb: float


def _measure(function: Callable[[], list[list[float]]]) -> tuple[list[list[float]], float, float]:
    """Mede tempo e pico aproximado de memória alocada durante uma execução."""

    tracemalloc.start()
    start = time.perf_counter()
    output = function()
    elapsed = time.perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return output, elapsed, peak / 1024


def compare_on_graph(graph: Graph, repetition: int = 1) -> list[BenchmarkResult]:
    """Executa os dois algoritmos no mesmo grafo e valida equivalência."""

    dijkstra_output, dijkstra_time, dijkstra_memory = _measure(
        lambda: dijkstra_all_pairs(graph.adjacency_list)
    )
    floyd_output, floyd_time, floyd_memory = _measure(
        lambda: floyd_warshall(graph.adjacency_matrix)
    )

    if dijkstra_output != floyd_output:
        raise AssertionError("Os algoritmos produziram matrizes de distâncias diferentes.")

    return [
        BenchmarkResult(
            algorithm="Dijkstra (todas as origens)",
            vertices=graph.vertices,
            edges=graph.edge_count,
            density=graph.density,
            repetition=repetition,
            time_seconds=dijkstra_time,
            peak_memory_kb=dijkstra_memory,
        ),
        BenchmarkResult(
            algorithm="Floyd-Warshall",
            vertices=graph.vertices,
            edges=graph.edge_count,
            density=graph.density,
            repetition=repetition,
            time_seconds=floyd_time,
            peak_memory_kb=floyd_memory,
        ),
    ]


def run_benchmarks(
    sizes: list[int],
    density: float,
    repetitions: int,
    seed: int,
) -> list[BenchmarkResult]:
    """Executa benchmarks para vários tamanhos de grafo."""

    results: list[BenchmarkResult] = []

    for vertices in sizes:
        for repetition in range(1, repetitions + 1):
            graph_seed = seed + vertices * 1000 + repetition
            graph = generate_connected_weighted_graph(
                vertices=vertices,
                density=density,
                seed=graph_seed,
            )
            results.extend(compare_on_graph(graph, repetition=repetition))

    return results


def summarize_results(results: list[BenchmarkResult]) -> list[dict[str, float | int | str]]:
    """Agrupa repetições para apresentar médias em tabelas e gráficos."""

    grouped: dict[tuple[str, int, int, float], list[BenchmarkResult]] = {}
    for result in results:
        key = (result.algorithm, result.vertices, result.edges, result.density)
        grouped.setdefault(key, []).append(result)

    summary: list[dict[str, float | int | str]] = []
    for (algorithm, vertices, edges, density), items in sorted(grouped.items(), key=lambda x: (x[0][1], x[0][0])):
        summary.append(
            {
                "algorithm": algorithm,
                "vertices": vertices,
                "edges": edges,
                "density": density,
                "repetitions": len(items),
                "avg_time_seconds": statistics.mean(item.time_seconds for item in items),
                "avg_peak_memory_kb": statistics.mean(item.peak_memory_kb for item in items),
            }
        )

    return summary


def results_to_dicts(results: list[BenchmarkResult]) -> list[dict[str, float | int | str]]:
    return [asdict(result) for result in results]
