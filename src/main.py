from ui.console_io import ConsoleIO
from ui.commandline_arguments_parser import parser
from services import assets_service, visualization_service, algorithms_service
from graph import Graph


def list_map_names(maps: list):
    prompt = "Testattavissa on seuraavat kartat:\n"
    for map_name in maps:
        prompt += map_name + "\n"
    return prompt


def init_map_and_scens(map_name: str, cl_args):
    scens = assets_service.read_scenarios(map_name)
    dimensions = (scens[0]["dimensions"][0], scens[0]["dimensions"][1])
    gifgen = visualization_service.GifGenerator(map_name, dimensions, cl_args.gif)
    graph = Graph(assets_service.read_map(map_name), cl_args.no_corner_cuts, gifgen)
    return graph, scens


def write_totals(io, totals, algorithms):
    if "dijkstra" in algorithms:
        io.write(
            f"Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan: \
{totals['dijkstra']} s."
        )
    if "a_star" in algorithms:
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
    maps = assets_service.get_available_maps()
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
    scen_idxs = cl_args.scenario
    scens_to_test = range(len(scens))
    all_chosen_scens_are_valid = scen_idxs is not None \
    and all(index in scens_to_test for index in scen_idxs)
    if choice == "1" and not all_chosen_scens_are_valid:
        prompt = f"Valitse skenaarion indeksi välillä 0-{len(scens)-1}:"
        scens_to_test = [scens[int(io.read(prompt, scens_to_test))]]
    elif choice == "1" and all_chosen_scens_are_valid:
        scens_to_test = [scen for scen in scens if scen["index"] in scen_idxs]
    elif choice == "2" and cl_args.amount not in range(1, len(scens)):
        prompt = "Kuinka monta skenaariota suoritetaan (1-10)?"
        n = int(io.read(prompt, [str(i) for i in range(1, 11)]))
        scens_to_test = assets_service.get_random_scens(scens, n, cl_args.shortest_range)
    else:
        scens_to_test = assets_service.get_random_scens(
            scens, cl_args.amount, cl_args.shortest_range)
    return scens_to_test


def main(io, cl_args):
    io.write("Tervetuloa polunetsintä algoritmien vertailu ohjelmaan!")
    map_name = check_commandline_argument_and_get_map_to_test(io, cl_args)
    graph, scens = init_map_and_scens(map_name, cl_args)
    scens_to_test = check_commandline_argument_select_test_type_and_scens_to_test(
        io, cl_args, scens
    )
    algorithms = algorithms_service.select_algorithms_to_test(cl_args)
    totals = algorithms_service.run_scenarios(
        io, map_name, scens_to_test, graph, algorithms, cl_args
    )
    write_totals(io, totals, [a.__name__ for a in algorithms])


if __name__ == "__main__":
    arguments = parser.parse_args()
    consoleio = ConsoleIO()
    main(consoleio, arguments)
