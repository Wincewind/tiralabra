import unittest
import os
from services import visualization_service, assets_service
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.jps import jps
from algorithms.a_star import a_star


class TestVisualizationService(unittest.TestCase):
    def setUp(self):
        self.map_name = "maze512-16-0"
        scens = assets_service.read_scenarios(self.map_name)
        self.scen = assets_service.get_random_scens(scens, 1,[0,9999])[0]
        self.graph = Graph(assets_service.read_map(self.map_name))
        self.graph.gifgen = visualization_service.GifGenerator(
            self.map_name, self.scen["dimensions"]
        )

    def test_drawing_dijkstra_found_path(self):
        dijkstra(self.scen["start"], self.scen["goal"], self.graph)
        visualization_service.draw_and_save_found_pathfinding(
            self.map_name, self.scen, "dijkstra", self.graph.nodes, self.graph.visited
        )
        file_formed = os.path.isfile(
            f'output/{self.map_name}_{self.scen["index"]}_dijkstra.png'
        )
        self.assertEqual(file_formed, True)

    def test_drawing_a_star_found_path(self):
        a_star(self.scen["start"], self.scen["goal"], self.graph)
        visualization_service.draw_and_save_found_pathfinding(
            self.map_name, self.scen, "A_star", self.graph.nodes, self.graph.visited
        )
        file_formed = os.path.isfile(
            f'output/{self.map_name}_{self.scen["index"]}_A_star.png'
        )
        self.assertEqual(file_formed, True)

    def test_drawing_jps_found_path(self):
        jps(self.scen["start"], self.scen["goal"], self.graph)
        visualization_service.draw_and_save_found_pathfinding(
            self.map_name, self.scen, "jps", self.graph.nodes, self.graph.visited
        )
        file_formed = os.path.isfile(
            f'output/{self.map_name}_{self.scen["index"]}_jps.png'
        )
        self.assertEqual(file_formed, True)

    def test_generating_gif_from_jps_pathfinding(self):
        self.graph.gifgen.generate_gif = True
        self.graph.gifgen.set_run_parameters(self.scen, "jps")
        jps(self.scen["start"], self.scen["goal"], self.graph)
        visualization_service.create_gif(
            self.graph.gifgen, self.graph.nodes, self.graph.visited
        )
        file_formed = os.path.isfile(
            f'output/{self.map_name}_{self.scen["index"]}_jps.gif'
        )
        self.assertEqual(file_formed, True)

    def test_calculating_circle_coords(self):
        origin = (10, 10)
        self.assertEqual(
            visualization_service.calculate_circle_coords_around_origin(origin, 2),
            {
                (8, 8),
                (10, 11),
                (11, 10),
                (10, 8),
                (12, 10),
                (8, 10),
                (11, 9),
                (10, 10),
                (8, 9),
                (9, 8),
                (8, 11),
                (9, 11),
                (11, 8),
                (11, 11),
            },
        )
