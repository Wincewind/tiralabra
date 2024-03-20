from heapq import heappush, heappop
from math import sqrt
from graph import Graph, Node # noqa # pylint: disable=unused-import
# Node importataan tässä, jotta sen itellisense:iin päästään koodissa käsiksi.

def dijkstra(start: tuple, goal: tuple, graph: Graph):
    """
    Implementaatio Dijkstran algoritmista.
    Argumentteina annetaan lähtö ja maali x,y -koordinaatit ja Graph-olio.
    Löydetty reitti täytetään Graph-olion visited attribuuttiin.
    """
    queue = []
    heappush(queue, (0,start))
    while len(queue) > 0:
        distance, coords = heappop(queue)
        if goal == coords:
            break
        for neighbour,direction in graph.nodes[coords]:
            # Kuljettua matkaa täytetään vaaka tai pystysuunnassa
            # yhdellä ja diagonaalisessa suunnassa kahden neliöjuurella
            to_neighbour = distance + 1 if direction % 2 == 0 else distance + sqrt(2)
            if neighbour.obstacle or \
            (neighbour.coords in graph.visited and
             graph.visited[neighbour.coords][0] <= to_neighbour):
                continue
            graph.visited[neighbour.coords] = (to_neighbour, coords)
            heappush(queue, (to_neighbour, neighbour.coords))
