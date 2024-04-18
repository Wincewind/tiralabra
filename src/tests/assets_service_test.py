import unittest
from random import randint, choice, choices
import os
from services import assets_service
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.jps import jps
from algorithms.a_star import a_star

class TestAssetsService(unittest.TestCase):
    def setUp(self):
        self.map_name = "AR0413SR"

    def test_reading_map(self):
        ascii_map = assets_service.read_map(self.map_name)
        self.assertEqual(len(ascii_map),512)
        self.assertEqual(len(ascii_map[0]),512)

    def test_reading_with_wrong_filename(self):
        ascii_map = assets_service.read_map("not_found")
        self.assertEqual(len(ascii_map),0)

    def test_reading_map_into_graph(self):
        ascii_graph = Graph(assets_service.read_map(self.map_name))
        self.assertGreater(len(ascii_graph.nodes),0)

    def test_reading_scens(self):
        scens = assets_service.read_scenarios(self.map_name)
        self.assertEqual(len(scens),1530)
        self.assertEqual(scens[7]['shortest'], 2.41421356)

    # 6 desimaalin tarkkuudella ovat etäisyydet kaikkiin skenaarioihin
    # verrattuna yhtä pitkät AR0413SR kartalla, kunhan kulmia ei leikata.
    def test_dijkstra_with_assets(self):
        graph = Graph(assets_service.read_map(self.map_name), True)
        scen = choice(assets_service.read_scenarios(self.map_name))
        graph.reset_visited()
        dijkstra(scen['start'], scen['goal'], graph)
        result = round(graph.visited[scen['goal']][0], 8)
        self.assertAlmostEqual(result, scen['shortest'], 6)

    def test_get_available_maps(self):
        maps = assets_service.get_available_maps()
        self.assertEqual(len(maps),3)

    def test_compare_dijkstra_a_star_and_jps_using_assets(self):
        graph = Graph(assets_service.read_map("London_1_512"), True)
        scens = choices(assets_service.read_scenarios("London_1_512"), k=10)
        for scen in scens:
            for algorithm in {"dijkstra":dijkstra, "A_star":a_star, "jps":jps}.items():
                graph.reset_visited()
                graph.reset_pruned()
                algorithm[1](scen['start'], scen['goal'], graph)
                if algorithm[0] == "dijkstra":
                    dijkstra_total = round(graph.visited[scen['goal']][0], 8)
                    self.assertAlmostEqual(dijkstra_total, scen['shortest'], 3)
                else:
                    comparison_total = round(graph.visited[scen['goal']][0], 8)
                    self.assertAlmostEqual(dijkstra_total, comparison_total)