"""Geração e representação de grafos ponderados com pesos positivos."""

from __future__ import annotations

from dataclasses import dataclass
import math
import random


INF = math.inf


@dataclass(frozen=True)
class Graph:
    """Grafo direcionado ponderado em duas representações equivalentes.

    A lista de adjacência favorece o Dijkstra. A matriz de adjacência favorece o
    Floyd-Warshall. Ambas são geradas a partir das mesmas arestas para garantir
    que os algoritmos recebam exatamente o mesmo grafo.
    """

    vertices: int
    adjacency_list: list[list[tuple[int, int]]]
    adjacency_matrix: list[list[float]]

    @property
    def edge_count(self) -> int:
        return sum(len(neighbors) for neighbors in self.adjacency_list)

    @property
    def density(self) -> float:
        max_edges = self.vertices * (self.vertices - 1)
        return 0.0 if max_edges == 0 else self.edge_count / max_edges


def generate_connected_weighted_graph(
    vertices: int,
    density: float,
    min_weight: int = 1,
    max_weight: int = 20,
    seed: int | None = None,
) -> Graph:
    """Gera um grafo direcionado fortemente conexo com pesos positivos.

    Primeiro criamos um ciclo que passa por todos os vértices, garantindo que há
    caminho entre qualquer par. Depois adicionamos arestas aleatórias até chegar
    perto da densidade desejada.
    """

    if vertices < 2:
        raise ValueError("O grafo precisa ter pelo menos 2 vértices.")
    if not 0 < density <= 1:
        raise ValueError("A densidade deve estar no intervalo (0, 1].")
    if min_weight <= 0 or max_weight < min_weight:
        raise ValueError("Os pesos devem ser positivos e max_weight >= min_weight.")

    rng = random.Random(seed)
    max_edges = vertices * (vertices - 1)
    target_edges = max(vertices, min(max_edges, round(max_edges * density)))

    edges: dict[tuple[int, int], int] = {}

    # Ciclo hamiltoniano direcionado: 0 -> 1 -> ... -> n-1 -> 0.
    for source in range(vertices):
        target = (source + 1) % vertices
        edges[(source, target)] = rng.randint(min_weight, max_weight)

    possible_edges = [
        (source, target)
        for source in range(vertices)
        for target in range(vertices)
        if source != target and (source, target) not in edges
    ]
    rng.shuffle(possible_edges)

    for source, target in possible_edges[: max(0, target_edges - len(edges))]:
        edges[(source, target)] = rng.randint(min_weight, max_weight)

    adjacency_list: list[list[tuple[int, int]]] = [[] for _ in range(vertices)]
    adjacency_matrix = [[INF] * vertices for _ in range(vertices)]

    for vertex in range(vertices):
        adjacency_matrix[vertex][vertex] = 0

    for (source, target), weight in edges.items():
        adjacency_list[source].append((target, weight))
        adjacency_matrix[source][target] = weight

    for neighbors in adjacency_list:
        neighbors.sort(key=lambda item: item[0])

    return Graph(
        vertices=vertices,
        adjacency_list=adjacency_list,
        adjacency_matrix=adjacency_matrix,
    )
