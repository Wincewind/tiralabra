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
    img = plt.imread(f"output/{map_name}_{scen_index}_{algorithm}.png")
    plt.imshow(img)
    plt.pause(10)


def display_formed_gif(map_name: str, scen_index: int, algorithm: str):
    img = plt.imread(f"output/{map_name}_{scen_index}_{algorithm}.gif")
    plt.imshow(img)
    plt.pause(10)


def init_map_and_scens(map_name: str, cl_args):
    scens = assets_io.read_scenarios(map_name)
    dimensions = (scens[0]["dimensions"][0], scens[0]["dimensions"][1])
    gifgen = assets_io.GifGenerator(map_name, dimensions, cl_args.gif)
    graph = Graph(assets_io.read_map(map_name), cl_args.no_corner_cuts, gifgen)
    return graph, scens


def run_scenario_for_algorithm(algorithm: tuple, graph: Graph, scen: dict):
    runs = []
    limit = 1 if graph.gifgen.generate_gif else 4
    while len(runs) < limit:
        graph.gifgen.set_run_parameters(scen, algorithm[0])
        graph.reset_visited()
        graph.reset_pruned()
        start = time()
        algorithm[1](scen["start"], scen["goal"], graph)
        end = time()
        runs.append(end - start)
    return runs


def calculate_and_write_run_stats(
    io, runs, totals, scen, algorithm_name, cl_args, graph
):
    run_mean = mean(runs)
    if algorithm_name == "jps":
        totals["jps"] += run_mean
    elif algorithm_name == "A_star":
        totals["a_star"] += run_mean
    else:
        totals["dijkstra"] += run_mean
    io.write(
        f"Algoritmin {algorithm_name} keskiarvo skenaarion {scen['index']} \
ratkaisemiseen oli: {run_mean} s."
    )
    if cl_args.print_path_len:
        io.write(
            f"Skenaarion lyhyin polku on {scen['shortest']} ja \
algoritmin löytämä polku oli {graph.visited[scen['goal']][0]}."
        )
    return totals


def run_scenarios(
    io,
    map_name: str,
    scens_to_test: list,
    graph: Graph,
    scens: list,
    algorithms: dict,
    cl_args,
):
    totals = {}
    totals["dijkstra"] = 0
    totals["jps"] = 0
    totals["a_star"] = 0
    for i in scens_to_test:
        scen = scens[i]
        scen["index"] = i
        for algorithm in algorithms.items():
            io.write(f"Testataan skenaariota {i} algoritmilla {algorithm[0]}:")
            runs = run_scenario_for_algorithm(algorithm, graph, scen)
            totals = calculate_and_write_run_stats(
                io, runs, totals, scen, algorithm[0], cl_args, graph
            )
            if cl_args.images:
                assets_io.draw_and_save_found_pathfinding(
                    map_name, scen, algorithm[0], graph.nodes, graph.visited
                )
                display_formed_img(map_name, i, algorithm[0])
            if cl_args.gif:
                assets_io.create_gif(graph.gifgen, graph.nodes, graph.visited)
    return totals


def write_totals(io, totals, algorithms):
    if "dijkstra" in algorithms:
        io.write(
            f"Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan: \
{totals['dijkstra']} s."
        )
    if "A_star" in algorithms:
        io.write(
            f"A* algoritmilla kesti polunetsinnässä kokonaisuudessaan: \
{totals['a_star']} s."
        )
    if "jps" in algorithms:
        io.write(
            f"JPS algoritmilla kesti polunetsinnässä kokonaisuudessaan: \
{totals['jps']} s."
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
    if choice == "1" and (
        scens_to_test is None
        or not all(str(scen) in scen_idxs for scen in scens_to_test)
    ):
        prompt = f"Valitse skenaarion indeksi välillä 0-{len(scens)-1}:"
        scens_to_test = [int(io.read(prompt, scen_idxs))]
    elif choice == "1" and all(
        scen for scen in scens_to_test if str(scen) not in scen_idxs
    ):
        pass
    elif choice == "2" and cl_args.amount not in range(1, len(scens)):
        prompt = "Kuinka monta skenaariota suoritetaan (1-10)?"
        n = io.read(prompt, [str(i) for i in range(1, 11)])
        scens_to_test = choices(range(len(scens)), k=int(n))
    else:
        scens_to_test = choices(range(len(scens)), k=int(cl_args.amount))
    return scens_to_test


def select_algorithms_to_test(cl_args):
    base_algorithms = {"dijkstra": dijkstra, "A_star": a_star, "jps": jps}
    algorithms_to_run = {}
    for n, f in base_algorithms.items():
        if n in cl_args.algorithms:
            algorithms_to_run[n] = f
    return algorithms_to_run


def main(io, cl_args):
    io.write("Tervetuloa polunetsintä algoritmien vertailu ohjelmaan!")
    map_name = check_commandline_argument_and_get_map_to_test(io, cl_args)
    graph, scens = init_map_and_scens(map_name, cl_args)
    scens_to_test = check_commandline_argument_select_test_type_and_scens_to_test(
        io, cl_args, scens
    )
    algorithms = select_algorithms_to_test(cl_args)
    totals = run_scenarios(
        io, map_name, scens_to_test, graph, scens, algorithms, cl_args
    )
    write_totals(io, totals, algorithms)


if __name__ == "__main__":
    arguments = parser.parse_args()
    consoleio = ConsoleIO()
    main(consoleio, arguments)
