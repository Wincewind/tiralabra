import unittest
from main import main
from ui.commandline_arguments_parser import parser


class StubIO:
    def __init__(self, inputs):
        self.inputs = inputs
        self.outputs = []

    def read(self, *args):
        return self.inputs.pop(0)

    def write(self, test_input):
        self.outputs.append(test_input)

    def read_argument(self, argument: str, expected_values: list):
        if argument not in expected_values:
            return None
        return argument


class TestMain(unittest.TestCase):

    def test_running_main_program_for_one_scen(self):
        io = StubIO(["AR0413SR", "1", "777"])
        main(io,parser.parse_args(["-i"]))
        self.assertTrue(
            io.outputs[2].startswith(
                "Algoritmin dijkstra keskiarvo skenaarion 777 ratkaisemiseen oli:"
            )
        )

    def test_running_main_program_for_a_random_scen(self):
        io = StubIO(["AR0413SR", "2", "1"])
        main(io,parser.parse_args(["-i"]))
        print(io.outputs)
        self.assertTrue(
            io.outputs[-1].startswith(
                "JPS algoritmilla kesti polunetsinnässä kokonaisuudessaan:"
            )
        )
