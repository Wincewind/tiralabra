import unittest
from math import sqrt
from graph import Graph
from algorithms.dijkstra import dijkstra
import algorithms.jps as jps
from algorithms.a_star import a_star


class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.test_graph_1 = [[".", ".", "."],
                             ["S", "G", "."],
                             [".", ".", "."]]

        self.test_graph_2 = [[".", "@", "."],
                             ["S", "G", "."],
                             [".", ".", "."]]

        self.test_graph_2_1 = [[".", ".", "."],
                               ["@", "G", "."],
                               [".", "S", "."]]

        self.test_graph_3 = [[".", ".", "."],
                             ["@", "G", "."],
                             ["S", ".", "."]]

        self.test_graph_4 = [
            [".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "."],
            ["@", ".", ".", ".", ".", "@", "G"],
            ["S", ".", ".", ".", ".", ".", "."],
            ["@", ".", ".", ".", ".", ".", "."],
        ]

        self.test_graph_4_1 = [
            [".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", "."],
            ["@", ".", ".", ".", "@", "@", "G"],
            ["S", ".", ".", ".", ".", ".", "."],
            ["@", ".", ".", ".", ".", ".", "."],
        ]

        self.test_graph_5 = [
            [".", ".", ".", ".", ".", "G", "."],
            [".", ".", ".", ".", ".", "@", "."],
            [".", ".", ".", ".", ".", "@", "."],
            ["S", "@", ".", ".", ".", "@", "."],
            [".", "@", ".", ".", ".", ".", "."],
        ]

        self.test_graph_6 = [["@", "@", "."], 
                             [".", "G", "@"], 
                             ["S", "@", "."]]

        self.test_graph_7 = [
            [".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", "@", "."],
            ["@", "@", "@", ".", "@", "@", "G"],
            ["S", ".", ".", ".", ".", "@", "."],
            ["@", "@", "@", "@", ".", ".", "."],
        ]

        self.test_graph_two_jump_points = [
            ["@", ".", ".", "."],
            ["@", "G", "@", "G"],
            ["S", ".", "@", "."],
            [".", "G", ".", "."],
            [".", ".", ".", "."],
        ]
        self.test_graph_jps = [
            ["S", ".", "@", ".", ".", ".", ".", ".", "."],
            [".", ".", "@", ".", "@", ".", ".", ".", "G"],
            [".", ".", "@", ".", "@", ".", "@", ".", "."],
            [".", ".", ".", ".", "@", ".", "@", ".", "."],
            [".", ".", ".", ".", ".", ".", "@", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", "."],
        ]

    def test_dijkstra_pathfinding_with_corner_cuts(self):
        self.graph.generate_graph(self.test_graph_5, False)
        dijkstra((0, 3), (5, 0), self.graph)
        self.assertAlmostEqual(self.graph.visited[(5, 0)][0], sqrt(2) * 3 + 2)

        self.graph.generate_graph(self.test_graph_4, False)
        dijkstra((0, 3), (6, 2), self.graph)
        self.assertAlmostEqual(self.graph.visited[(6, 2)][0], 5 + sqrt(2))

        self.graph.generate_graph(self.test_graph_7, False)
        dijkstra((0, 3), (6, 2), self.graph)
        self.assertAlmostEqual(self.graph.visited[(6, 2)][0], sqrt(2) * 2 + 5)

    def test_dijkstra_pathfinding_without_corner_cuts(self):
        self.graph.generate_graph(self.test_graph_5, True)
        dijkstra((0, 3), (5, 0), self.graph)
        print(sqrt(2) * 3 + 2)
        self.assertAlmostEqual(self.graph.visited[(5, 0)][0], 4 + 2 * sqrt(2))
        n = (5, 0)
        while n != (0, 3):
            print(n)
            n = self.graph.visited[n][1]

        self.graph.generate_graph(self.test_graph_4, True)
        dijkstra((0, 3), (6, 2), self.graph)
        self.assertAlmostEqual(self.graph.visited[(6, 2)][0], 7)

        self.graph.generate_graph(self.test_graph_7, True)
        dijkstra((0, 3), (6, 2), self.graph)
        self.assertAlmostEqual(self.graph.visited[(6, 2)][0], 9)

    def test_total_distance_calc(self):
        self.assertEqual(jps.calculate_total_dist((5, 0), (7, 5), 2), 7.385164807134504)
        self.assertEqual(jps.calculate_total_dist((0, 0), (0, 0), 0), 0)
        self.assertEqual(jps.calculate_total_dist((5, 0), (0, 0), 0), 5)

    def test_jps_straight_pruning_rules_graph1(self):
        self.graph.generate_graph(self.test_graph_1, False)
        n_to_check = self.graph.nodes[(0, 1)][2]
        jps._prune((0, 1), 2, self.graph)
        available_n = [
            n for _, n in self.graph.nodes[n_to_check.coords].items() if not n.pruned
        ]
        self.assertEqual(len(available_n), 1)

    def test_jps_straight_pruning_rules_graph2(self):
        self.graph.generate_graph(self.test_graph_2, False)
        n_to_check = self.graph.nodes[(0, 1)][2]
        jps._prune((0, 1), 2, self.graph)
        available_n = [n for _, n in self.graph.nodes[(1, 1)].items() if not n.pruned]
        self.assertEqual(len(available_n), 2)

        self.graph.generate_graph(self.test_graph_2, True)
        n_to_check = self.graph.nodes[(0, 1)][2]
        jps._prune((0, 1), 2, self.graph)
        available_n = [
            n for _, n in self.graph.nodes[n_to_check.coords].items() if not n.pruned
        ]
        self.assertEqual(len(available_n), 1)

    def test_jps_straight_pruning_rules_graph2_1(self):
        self.graph.generate_graph(self.test_graph_2_1, False)
        n_to_check = self.graph.nodes[(1, 2)][0]
        jps._prune((1, 2), 0, self.graph)
        available_n = [
            n for _, n in self.graph.nodes[n_to_check.coords].items() if not n.pruned
        ]
        self.assertEqual(len(available_n), 2)

    def test_jps_diagonal_pruning_rules_graph1(self):
        self.graph.generate_graph(self.test_graph_1, False)
        n_to_check = self.graph.nodes[(0, 2)][1]
        jps._prune((0, 2), 1, self.graph)
        available_n = [
            n for _, n in self.graph.nodes[n_to_check.coords].items() if not n.pruned
        ]
        self.assertEqual(len(available_n), 3)

    def test_jps_diagonal_pruning_rules_graph3(self):
        self.graph.generate_graph(self.test_graph_3, False)
        n_to_check = self.graph.nodes[(0, 2)][1]
        jps._prune((0, 2), 1, self.graph)
        available_n = [
            n for _, n in self.graph.nodes[n_to_check.coords].items() if not n.pruned
        ]
        self.assertEqual(len(available_n), 4)

    def test_jps_find_straight_jump_point(self):
        start = (0, 3)
        goal = (6, 2)
        self.graph.generate_graph(self.test_graph_4, False)
        jump_point = jps._jump(start, 2, goal, self.graph)[0]
        self.assertEqual(jump_point.coords, (5, 3))

    def test_jps_find_straight_jump_point_2(self):
        start = (0, 3)
        goal = (6, 2)
        self.graph.generate_graph(self.test_graph_4_1, False)
        jump_point = jps._jump(start, 2, goal, self.graph)[0]
        self.assertEqual(jump_point.coords, (5, 3))

    def test_jps_fail_to_find_straight_jump_point(self):
        start = (0, 3)
        goal = (5, 0)
        self.graph.generate_graph(self.test_graph_5, False)
        jump_point = jps._jump(start, 0, goal, self.graph)[0]
        self.assertEqual(jump_point, None)

    def test_jps_find_diagonal_jump_point(self):
        start = (1, 2)
        goal = (5, 0)
        self.graph.generate_graph(self.test_graph_5, False)
        jump_point = jps._jump(start, 1, goal, self.graph)[0]
        self.assertEqual(jump_point.coords, (3, 0))

    def test_jps_identifying_successors(self):
        start = (0, 2)
        goal = (3, 1)
        self.graph.generate_graph(self.test_graph_two_jump_points, False)
        successors = jps._identify_successors(start, goal, self.graph)
        self.assertEqual(len(successors), 2)
        self.assertEqual(sorted([s[0].coords for s in successors]), [(1, 1), (1, 3)])

    def test_compare_dijkstra_and_jps_pathfinding(self):
        start = (0, 3)
        goal = (5, 0)
        self.graph.generate_graph(self.test_graph_5, False)
        dijkstra(start, goal, self.graph)
        dijkstra_path_len = self.graph.visited[goal][0]
        self.graph.reset_visited()
        jps.jps(start, goal, self.graph)
        jps_path_len = self.graph.visited[goal][0]
        self.assertAlmostEqual(dijkstra_path_len, jps_path_len)

    def test_jps_total_found_successors_amount(self):
        self.graph.generate_graph(self.test_graph_jps, False)
        start = (0, 0)
        goal = (8, 1)
        jps.jps(start, goal, self.graph)
        self.assertEqual(len(self.graph.visited), 16)

    def test_compare_dijkstra_and_a_star_pathfinding(self):
        start = (0, 3)
        goal = (5, 0)
        self.graph.generate_graph(self.test_graph_5, False)
        dijkstra(start, goal, self.graph)
        dijkstra_path_len = self.graph.visited[goal][0]
        self.graph.reset_visited()
        a_star(start, goal, self.graph)
        a_star_path_len = self.graph.visited[goal][0]
        self.assertAlmostEqual(dijkstra_path_len, a_star_path_len)
