"""Algoritmos de caminho mínimo usados na comparação."""

from __future__ import annotations

import heapq
import math


def dijkstra(adjacency_list: list[list[tuple[int, int]]], source: int) -> list[float]:
    """Calcula caminhos mínimos a partir de uma origem usando estratégia gulosa.

    O heap sempre escolhe o vértice mais promissor, isto é, aquele com a menor
    distância conhecida no momento.
    """

    vertices = len(adjacency_list)
    distances = [math.inf] * vertices
    distances[source] = 0
    priority_queue: list[tuple[float, int]] = [(0, source)]

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in adjacency_list[current_vertex]:
            candidate = current_distance + weight
            if candidate < distances[neighbor]:
                distances[neighbor] = candidate
                heapq.heappush(priority_queue, (candidate, neighbor))

    return distances


def dijkstra_all_pairs(adjacency_list: list[list[tuple[int, int]]]) -> list[list[float]]:
    """Executa Dijkstra uma vez para cada origem.

    Essa versão permite comparar o resultado com Floyd-Warshall, que naturalmente
    resolve todos os pares de vértices.
    """

    return [dijkstra(adjacency_list, source) for source in range(len(adjacency_list))]


def floyd_warshall(adjacency_matrix: list[list[float]]) -> list[list[float]]:
    """Calcula caminhos mínimos entre todos os pares por programação dinâmica.

    dist[i][j] representa a melhor distância conhecida de i até j. A cada etapa,
    o algoritmo decide se permitir o vértice k como intermediário melhora algum
    caminho.
    """

    vertices = len(adjacency_matrix)
    distances = [row[:] for row in adjacency_matrix]

    for intermediate in range(vertices):
        for source in range(vertices):
            source_to_intermediate = distances[source][intermediate]
            if source_to_intermediate == math.inf:
                continue

            for target in range(vertices):
                candidate = source_to_intermediate + distances[intermediate][target]
                if candidate < distances[source][target]:
                    distances[source][target] = candidate

    return distances
