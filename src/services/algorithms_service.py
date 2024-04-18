from time import time
from statistics import mean
from services import visualization_service
from graph import Graph
from algorithms.dijkstra import dijkstra
from algorithms.a_star import a_star
from algorithms.jps import jps


def select_algorithms_to_test(cl_args):
    base_algorithms = {"dijkstra": dijkstra, "A_star": a_star, "jps": jps}
    algorithms_to_run = {}
    for n, f in base_algorithms.items():
        if n in cl_args.algorithms:
            algorithms_to_run[n] = f
    return algorithms_to_run


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
        for algorithm in algorithms.items():
            io.write(f"Testataan skenaariota {i} algoritmilla {algorithm[0]}:")
            runs = run_scenario_for_algorithm(algorithm, graph, scen)
            totals = calculate_and_write_run_stats(
                io, runs, totals, scen, algorithm[0], cl_args, graph
            )
            if cl_args.images:
                visualization_service.draw_and_save_found_pathfinding(
                    map_name, scen, algorithm[0], graph.nodes, graph.visited
                )
                visualization_service.display_formed_img(map_name, i, algorithm[0])
            if cl_args.gif:
                visualization_service.create_gif(graph.gifgen, graph.nodes, graph.visited)
    return totals
