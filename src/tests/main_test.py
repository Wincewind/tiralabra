import unittest
from random import randint, choice
import os
from main import main
import assets_io
from graph import Graph
from algorithms.dijkstra import dijkstra


class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def read(self, *args):
        return self.inputs.pop(0)

    def write(self, test_input):
        self.outputs.append(test_input)


class TestMain(unittest.TestCase):

    def test_running_main_program_for_one_scen(self):
        io = StubIO(["AR0413SR", "1", "777"])
        main(io)
        self.assertTrue(io.outputs[2].startswith("Skenaarion 777 ratkaisemisessa kului Dijkstran algoritmilla:"))

    def test_running_main_program_for_ten_random_scens(self):
        io = StubIO(["AR0413SR", "2", "1"])
        main(io)
        print(io.outputs)
        self.assertTrue(io.outputs[-1].startswith("Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan:"))