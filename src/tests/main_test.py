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


    def test_running_main_program_with_several_cl_args(self):
        io = StubIO("")
        main(io,parser.parse_args(["-p","-g","-m","maze512-16-0","-i","-a","jps","-t 1","-s 200"]))
        print(io.outputs)
        self.assertTrue("algoritmin löytämä polku oli" in io.outputs[-2])
        self.assertTrue(
            io.outputs[-1].startswith(
                "JPS algoritmilla kesti polunetsinnässä kokonaisuudessaan:"
            )
        )

    def test_running_main_program_with_several_cl_args_2(self):
            io = StubIO("")
            main(io,parser.parse_args(["-p","-m","AR0413SR","-i","-a","dijkstra","-t 2","-c 1000","-r 611"]))
            print(io.outputs)
            self.assertTrue("algoritmin löytämä polku oli" in io.outputs[-2])
            self.assertTrue(
                io.outputs[-1].startswith(
                    "Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan:"
                )
            )