import unittest
from random import randint, shuffle
import os
import assets_io
from graph import Graph
from algorithms.dijkstra import dijkstra

class TestAssetsIO(unittest.TestCase):
    def setUp(self):
        self.map_name = "AR0413SR"
        

    def test_reading_map(self):
        ascii_map = assets_io.read_map(self.map_name)
        self.assertEqual(len(ascii_map),512)
        self.assertEqual(len(ascii_map[0]),512)

    def test_reading_with_wrong_filename(self):
        ascii_map = assets_io.read_map("not_found")
        self.assertEqual(len(ascii_map),0)

    def test_reading_map_into_graph(self):
        ascii_graph = Graph(assets_io.read_map(self.map_name))
        self.assertGreater(len(ascii_graph.nodes),0)

    def test_reading_scens(self):
        scens = assets_io.read_scenarios(self.map_name)
        self.assertEqual(len(scens),1530)
        self.assertEqual(scens[7]['shortest'], 2.41421356)

    def test_dijkstra_with_assets(self):
        graph = Graph(assets_io.read_map(self.map_name))
        scens = assets_io.read_scenarios(self.map_name)
        shuffle(scens)
        dijkstra(scens[0]['start'], scens[0]['goal'], graph)
        self.assertLessEqual(graph.visited[scens[0]['goal']][0],
                             scens[0]['shortest'])

    def test_drawing_found_path(self):
        graph = Graph(assets_io.read_map(self.map_name))
        scens = assets_io.read_scenarios(self.map_name)
        shuffle(scens)
        dijkstra(scens[0]['start'], scens[0]['goal'], graph)
        file_idx = randint(0,1000000)
        assets_io.draw_path_onto_map(self.map_name,file_idx,scens[0],graph.visited)
        file_formed = os.path.isfile(f'src/output/{self.map_name}_{file_idx}.png')
        self.assertEqual(file_formed,True)