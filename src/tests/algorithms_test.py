import unittest
from math import sqrt
from graph import Graph
from algorithms.dijkstra import dijkstra

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
        
        self.test_graph_6 = [['.','@','.'],
                             ['@','G','@'],
                             ['S','@','.']]

    def test_dijkstra_pathfinding(self):
        self.graph.generate_graph(self.test_graph_5)
        dijkstra((0,3),(5,0),self.graph)
        self.assertAlmostEqual(self.graph.visited[(5,0)][0],sqrt(2)*3 +2)

        self.graph.generate_graph(self.test_graph_4)
        dijkstra((0,3),(6,2),self.graph)
        self.assertAlmostEqual(self.graph.visited[(6,2)][0],5 + sqrt(2))
