import unittest
from graph import Graph

class TestGraph(unittest.TestCase):
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

    def test_graph_generation(self):
        self.graph.generate_graph(self.test_graph_5)
        neighbours = self.graph.nodes[(4,2)]
        neighbours = [n for n in neighbours if n[0].obstacle]
        self.assertEqual(len(neighbours),3)

        self.graph.generate_graph(self.test_graph_6)
        neighbours = self.graph.nodes[(1,1)]
        neighbours = [n for n in neighbours if n[0].obstacle]
        self.assertEqual(len(neighbours),4)