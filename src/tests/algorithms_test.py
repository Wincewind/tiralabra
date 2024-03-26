import unittest
from math import sqrt
from graph import Graph
from algorithms.dijkstra import dijkstra
import algorithms.jps as jps

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.test_graph_1 = [['.','.','.'],
                             ['S','G','.'],
                             ['.','.','.']]
        
        self.test_graph_2 = [['.','@','.'],
                             ['S','G','.'],
                             ['.','.','.']]
        
        self.test_graph_3 = [['.','.','.'],
                             ['@','G','.'],
                             ['S','.','.']]
        
        self.test_graph_4 = [['.','.','.','.','.','.','.'],
                             ['.','.','.','.','.','.','.'],
                             ['@','.','.','.','.','@','G'],
                             ['S','.','.','.','.','.','.'],
                             ['@','.','.','.','.','.','.']]
        
        self.test_graph_5 = [['.','.','.','.','.','G','.'],
                             ['.','.','.','.','.','@','.'],
                             ['.','.','.','.','.','@','.'],
                             ['S','@','.','.','.','@','.'],
                             ['.','@','.','.','.','.','.']]
        
        self.test_graph_6 = [['@','@','.'],
                             ['.','G','@'],
                             ['S','@','.']]
        
        self.test_graph_7 = [['.','.','.','.','.','.','.'],
                             ['.','.','.','.','.','@','.'],
                             ['@','@','@','.','@','@','G'],
                             ['S','.','.','.','.','@','.'],
                             ['@','@','@','@','.','.','.']]

    def test_dijkstra_pathfinding_with_corner_cuts(self):
        self.graph.generate_graph(self.test_graph_5,False)
        dijkstra((0,3),(5,0),self.graph)
        self.assertAlmostEqual(self.graph.visited[(5,0)][0],sqrt(2)*3 +2)

        self.graph.generate_graph(self.test_graph_4,False)
        dijkstra((0,3),(6,2),self.graph)
        self.assertAlmostEqual(self.graph.visited[(6,2)][0],5 + sqrt(2))

        self.graph.generate_graph(self.test_graph_7,False)
        dijkstra((0,3),(6,2),self.graph)
        self.assertAlmostEqual(self.graph.visited[(6,2)][0],sqrt(2)*2 + 5)
        
    def test_dijkstra_pathfinding_without_corner_cuts(self):
        self.graph.generate_graph(self.test_graph_5, True)
        dijkstra((0,3),(5,0),self.graph)
        print(sqrt(2)*3 +2)
        self.assertAlmostEqual(self.graph.visited[(5,0)][0],4 + 2*sqrt(2))
        n = (5,0)
        while n != (0,3):
            print(n)
            n = self.graph.visited[n][1]

        self.graph.generate_graph(self.test_graph_4, True)
        dijkstra((0,3),(6,2),self.graph)
        self.assertAlmostEqual(self.graph.visited[(6,2)][0], 7)
        
        self.graph.generate_graph(self.test_graph_7, True)
        dijkstra((0,3),(6,2),self.graph)
        self.assertAlmostEqual(self.graph.visited[(6,2)][0], 9)

    def test_total_distance_calc(self):
        self.assertEqual(jps.calculate_total_dist((5,0),(7,5), 2), 7.385164807134504)
        self.assertEqual(jps.calculate_total_dist((0,0),(0,0), 0), 0)
        self.assertEqual(jps.calculate_total_dist((5,0),(0,0), 0), 5)

    def test_jps_straight_pruning_rules_graph1(self):
        self.graph.generate_graph(self.test_graph_1, False)
        n_to_check = self.graph.nodes[(0,1)][2]
        jps._prune((0,1),(2, n_to_check),self.graph)
        available_n = [n for _,n in self.graph.nodes[n_to_check.coords].items() if not n.pruned]
        self.assertEqual(len(available_n),1)

    def test_jps_straight_pruning_rules_graph2(self):
        self.graph.generate_graph(self.test_graph_2, False)
        n_to_check = self.graph.nodes[(0,1)][2]
        jps._prune((0,1),(2, n_to_check),self.graph)
        available_n = [n for _,n in self.graph.nodes[n_to_check.coords].items() if not n.pruned]
        self.assertEqual(len(available_n), 2)

        self.graph.generate_graph(self.test_graph_2, True)
        n_to_check = self.graph.nodes[(0,1)][2]
        jps._prune((0,1),(2, n_to_check),self.graph)
        available_n = [n for _,n in self.graph.nodes[n_to_check.coords].items() if not n.pruned]
        self.assertEqual(len(available_n), 1)

    def test_jps_diagonal_pruning_rules_graph1(self):
        self.graph.generate_graph(self.test_graph_1, False)
        n_to_check = self.graph.nodes[(0,2)][1]
        jps._prune((0,2),(1, n_to_check),self.graph)
        available_n = [n for _,n in self.graph.nodes[n_to_check.coords].items() if not n.pruned]
        self.assertEqual(len(available_n), 3)

    def test_jps_diagonal_pruning_rules_graph3(self):
        self.graph.generate_graph(self.test_graph_3, False)
        n_to_check = self.graph.nodes[(0,2)][1]
        jps._prune((0,2),(1, n_to_check),self.graph)
        available_n = [n for _,n in self.graph.nodes[n_to_check.coords].items() if not n.pruned]
        self.assertEqual(len(available_n), 4)