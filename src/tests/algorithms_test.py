import unittest
from math import sqrt
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.jps import calculate_total_dist

class TestAlgorithms(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()
        self.test_graph_1 = [['.','.','.'],
                             ['S','G','.'],
                             ['S','.','.']]
        
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
        self.assertEqual(calculate_total_dist((5,0),(7,5), 2), 7.385164807134504)
        self.assertEqual(calculate_total_dist((0,0),(0,0), 0), 0)
        self.assertEqual(calculate_total_dist((1,0),(0,0), 1), 2)