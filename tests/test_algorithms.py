import math
import unittest

from caminho_minimo.algorithms import dijkstra, dijkstra_all_pairs, floyd_warshall
from caminho_minimo.graph import generate_connected_weighted_graph


class TestShortestPathAlgorithms(unittest.TestCase):
    def test_dijkstra_known_graph(self):
        adjacency_list = [
            [(1, 4), (2, 1)],
            [(3, 1)],
            [(1, 2), (3, 5)],
            [],
        ]

        self.assertEqual(dijkstra(adjacency_list, 0), [0, 3, 1, 4])

    def test_floyd_warshall_known_graph(self):
        inf = math.inf
        adjacency_matrix = [
            [0, 4, 1, inf],
            [inf, 0, inf, 1],
            [inf, 2, 0, 5],
            [inf, inf, inf, 0],
        ]

        self.assertEqual(
            floyd_warshall(adjacency_matrix),
            [
                [0, 3, 1, 4],
                [inf, 0, inf, 1],
                [inf, 2, 0, 3],
                [inf, inf, inf, 0],
            ],
        )

    def test_dijkstra_all_pairs_matches_floyd_warshall_on_generated_graph(self):
        graph = generate_connected_weighted_graph(vertices=12, density=0.35, seed=7)

        self.assertEqual(
            dijkstra_all_pairs(graph.adjacency_list),
            floyd_warshall(graph.adjacency_matrix),
        )
        self.assertGreaterEqual(graph.edge_count, graph.vertices)
        self.assertTrue(all(weight > 0 for neighbors in graph.adjacency_list for _, weight in neighbors))


if __name__ == "__main__":
    unittest.main()
