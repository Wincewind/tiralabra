from time import time
from random import choices
from statistics import mean
import matplotlib.pyplot as plt
from ui.console_io import ConsoleIO
from ui.commandline_arguments_parser import parser
import assets_io
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.a_star import a_star
from algorithms.jps import jps


def list_map_names(maps: list):
    prompt = "Testattavissa on seuraavat kartat:\n"
    for map_name in maps:
        prompt += map_name + "\n"
    return prompt


def display_formed_img(map_name: str, scen_index: int, algorithm: str):
    img = plt.imread(f"src/output/{map_name}_{scen_index}_{algorithm}.png")
    plt.imshow(img)
    plt.pause(10)


def init_map_and_scens(map_name: str):
    graph = Graph(assets_io.read_map(map_name), False)
    scens = assets_io.read_scenarios(map_name)
    return graph, scens

def run_scenario_for_algorithm(algorithm: tuple, graph: Graph, scen: dict):
    runs = []
    while len(runs) < 4:
        graph.reset_visited()
        graph.reset_pruned()
        start = time()
        algorithm[1](scen["start"], scen["goal"], graph)
        end = time()
        runs.append(end - start)
    return runs

def run_scenarios(io, map_name: str, scens_to_test: list,
                  graph: Graph, scens: list, algorithms: dict, cl_args):
    dijkstra_total = 0
    jps_total = 0
    a_star_total = 0
    for i in scens_to_test:
        scen = scens[i]
        for algorithm in algorithms.items():
            io.write(f"Testataan skenaariota {i} algoritmilla {algorithm[0]}:")
            runs = run_scenario_for_algorithm(algorithm, graph, scen)
            run_mean = mean(runs)
            if algorithm[0] == "jps":
                jps_total += run_mean
            elif algorithm[0] == "A_star":
                a_star_total += run_mean
            else:
                dijkstra_total += run_mean
            io.write(
                f"Algoritmin {algorithm[0]} keskiarvo skenaarion {i} \
ratkaisemiseen oli: {run_mean} s."
            )
            if cl_args.images:
                assets_io.draw_path_onto_map(map_name, i, scen, algorithm[0], graph)
                display_formed_img(map_name, i, algorithm[0])
    return dijkstra_total, jps_total, a_star_total


def write_totals(io, dijkstra_total, a_star_total, jps_total, algorithms):
    if 'dijkststra' in algorithms:
        io.write(
            f"Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan: {dijkstra_total} s."
        )
    if 'A_star' in algorithms:
        io.write(
            f"A* algoritmilla kesti polunetsinnässä kokonaisuudessaan: {a_star_total} s."
        )
    if 'jps' in algorithms:
        io.write(
            f"JPS algoritmilla kesti polunetsinnässä kokonaisuudessaan: {jps_total} s."
        )

def check_commandline_argument_and_get_map_to_test(io, cl_args):
    maps = assets_io.get_available_maps()
    map_name = cl_args.map_name
    if map_name == "":
        prompt = list_map_names(maps)
        prompt += "Kirjoita kartan nimi, jolla haluat testata polunetsintä algoritmeja:"
        map_name = io.read(prompt, maps)
    return map_name


def check_commandline_argument_select_test_type_and_scens_to_test(io, cl_args, scens):
    if cl_args.test_type == -1:
        prompt = "Valitse tietty suoritettava skenaario (1) tai \
suorita 1-10 satunnaista skenaariota (2):"
        choice = io.read(prompt, ["1", "2"])
    else:
        choice = str(cl_args.test_type)
    scens_to_test = cl_args.scenario
    scen_idxs = [str(i) for i in range(len(scens))]
    if choice == "1" and (scens_to_test == -1 or
                          not all(scen for scen in scens_to_test if str(scen) not in scen_idxs)):
        prompt = f"Valitse skenaarion indeksi välillä 0-{len(scens)-1}:"
        scens_to_test = [int(io.read(prompt, scen_idxs))]
    elif choice == "1" and all(scen for scen in scens_to_test if str(scen) not in scen_idxs):
        pass
    elif choice == "2" and cl_args.amount not in range(1,len(scens)):
        prompt = "Kuinka monta skenaariota suoritetaan (1-10)?"
        n = io.read(prompt, [str(i) for i in range(1, 11)])
        scens_to_test = choices(range(len(scens)), k=int(n))
    else:
        scens_to_test = choices(range(len(scens)), k=int(cl_args.amount))
    return scens_to_test

def select_algorithms_to_test(cl_args):
    base_algorithms = {"dijkstra":dijkstra, "A_star":a_star, "jps":jps}
    algorithms_to_run = {}
    for n,f in base_algorithms.items():
        if n in cl_args.algorithms:
            algorithms_to_run[n] = f
    return algorithms_to_run

def main(io, cl_args):
    io.write("Tervetuloa polunetsintä algoritmien vertailu ohjelmaan!")
    map_name = check_commandline_argument_and_get_map_to_test(io, cl_args)
    graph, scens = init_map_and_scens(map_name)
    scens_to_test = check_commandline_argument_select_test_type_and_scens_to_test(
        io, cl_args, scens)
    algorithms = select_algorithms_to_test(cl_args)
    dijkstra_total, jps_total, a_star_total = run_scenarios(
        io, map_name, scens_to_test, graph, scens, algorithms,
        cl_args
    )
    write_totals(io, dijkstra_total, a_star_total, jps_total, algorithms)


if __name__ == "__main__":
    arguments = parser.parse_args()
    consoleio = ConsoleIO()
    main(consoleio,arguments)
