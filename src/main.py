from time import time
from random import choices
import matplotlib.pyplot as plt
from console_io import ConsoleIO
import assets_io
from graph import Graph
from algorithms.dijkstra import dijkstra


def list_map_names(maps: list):
    prompt = "Testattavissa on seuraavat kartat:\n"
    for map_name in maps:
        prompt += map_name + "\n"
    return prompt


def display_formed_img(map_name: str, scen_index: int):
    img = plt.imread(f"src/output/{map_name}_{scen_index}.png")
    plt.imshow(img)
    plt.pause(10)


def init_map_and_scens(map_name: str):
    graph = Graph(assets_io.read_map(map_name))
    scens = assets_io.read_scenarios(map_name)
    return graph, scens


def run_scenarios(io, map_name: str, scens_to_test: list, graph: Graph, scens: list):
    dijkstra_total = 0
    for i in scens_to_test:
        graph.reset_visited()
        io.write(f"Testataan skenaariota {i}:")
        scen = scens[i]
        start = time()
        dijkstra(scen["start"], scen["goal"], graph)
        end = time()
        dijkstra_total += end - start
        io.write(
            f"Skenaarion {i} ratkaisemisessa kului Dijkstran algoritmilla: {end-start} s."
        )
        assets_io.draw_path_onto_map(map_name, i, scen, graph.visited)
        display_formed_img(map_name, i)
    return dijkstra_total


def main(io):
    io.write("Tervetuloa polunetsintä algoritmien vertailu ohjelmaan!")
    maps = assets_io.get_available_maps()
    prompt = list_map_names(maps)
    prompt += "Kirjoita kartan nimi, jolla haluat testata polunetsintä algoritmeja:"
    map_name = io.read(prompt, maps)
    graph, scens = init_map_and_scens(map_name)
    prompt = "Valitse tietty suoritettava skenaario (1) tai \
suorita 1-10 satunnaista skenaariota (2):"
    choice = io.read(prompt, ["1", "2"])
    if choice == "1":
        prompt = f"Valitse skenaarion indeksi välillä 0-{len(scens)}:"
        scen_idxs = [str(i) for i in range(len(scens))]
        scens_to_test = [int(io.read(prompt, scen_idxs))]
    else:
        prompt = "Kuinka monta skenaariota suoritetaan (1-10)?"
        n = io.read(prompt, [str(i) for i in range(1,11)])
        scens_to_test = choices(range(len(scens)), k=int(n))

    dijkstra_total = run_scenarios(io, map_name, scens_to_test, graph, scens)
    io.write(
        f"Dijkstran algoritmilla kesti polunetsinnässä kokonaisuudessaan: {dijkstra_total} s."
    )


if __name__ == "__main__":
    consoleio = ConsoleIO()
    main(consoleio)
