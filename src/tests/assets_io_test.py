import unittest
from random import randint, choice
import os
import assets_io
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.jps import jps

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

    # 6 desimaalin tarkkuudella ovat etäisyydet kaikkiin skenaarioihin
    # verrattuna yhtä pitkät AR0413SR kartalla, kunhan kulmia ei leikata.
    def test_dijkstra_with_assets(self):
        graph = Graph(assets_io.read_map(self.map_name), True)
        scen = choice(assets_io.read_scenarios(self.map_name))
        graph.reset_visited()
        dijkstra(scen['start'], scen['goal'], graph)
        result = round(graph.visited[scen['goal']][0], 8)
        self.assertAlmostEqual(result, scen['shortest'], 6)

    def test_drawing_dijkstra_found_path(self):
        graph = Graph(assets_io.read_map(self.map_name))
        scen = choice(assets_io.read_scenarios(self.map_name))
        dijkstra(scen['start'], scen['goal'], graph)
        file_idx = randint(0,1000000)
        assets_io.draw_path_onto_map(self.map_name,file_idx,scen,'dijkstra',graph)
        file_formed = os.path.isfile(f'src/output/{self.map_name}_{file_idx}_dijkstra.png')
        self.assertEqual(file_formed,True)

    def test_get_available_maps(self):
        maps = assets_io.get_available_maps()
        self.assertEqual(len(maps),3)

    def test_drawing_jps_found_path(self):
        graph = Graph(assets_io.read_map(self.map_name),False)
        scen = choice(assets_io.read_scenarios(self.map_name))
        jps(scen['start'], scen['goal'], graph)
        file_idx = randint(0,1000000)
        assets_io.draw_path_onto_map(self.map_name,file_idx,scen,'jps',graph)
        file_formed = os.path.isfile(f'src/output/{self.map_name}_{file_idx}_jps.png')
        self.assertEqual(file_formed,True)
